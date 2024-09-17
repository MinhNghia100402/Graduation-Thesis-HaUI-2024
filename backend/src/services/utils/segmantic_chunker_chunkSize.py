import re
from FlagEmbedding import FlagModel
import numpy as np
from tqdm import tqdm
from langchain_experimental.text_splitter import SemanticChunker
from sklearn.metrics.pairwise import cosine_similarity
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore, RetrievalMode
import os


def split_document(document):
    # single_sentences_list = re.split('(?<=[.?!])\\s+', document) =======\
    single_sentences_list = re.split('=======', document)
    sentences = [{'sentence': x, 'index' : i} for i, x in enumerate(single_sentences_list)]
    return sentences
#=====================
def combine_sentences(sentences, buffer_size=1):
    # Go through each sentence dict
    for i in tqdm(range(len(sentences)), desc="Processing sentences"):
        # Create a string that will hold the sentences which are joined
        combined_sentence = ''

        # Add sentences before the current one, based on the buffer size.
        for j in range(i - buffer_size, i):
            # Check if the index j is not negative (to avoid index out of range like on the first one)
            if j >= 0:
                # Add the sentence at index j to the combined_sentence string
                combined_sentence += sentences[j]['sentence'] + ' '

        # Add the current sentence
        combined_sentence += sentences[i]['sentence']

        # Add sentences after the current one, based on the buffer size
        for j in range(i + 1, i + 1 + buffer_size):
            # Check if the index j is within the range of the sentences list
            if j < len(sentences):
                # Add the sentence at index j to the combined_sentence string
                combined_sentence += ' ' + sentences[j]['sentence']

        # Then add the whole thing to your dict
        # Store the combined sentence in the current sentence dict
        sentences[i]['combined_sentence'] = combined_sentence

    return sentences


def add_combined_sentence_embedding(sentences,model_embedding):
    
    embeddings = [model_embedding.encode(x['combined_sentence']) for x in sentences]
    for i, sentence in enumerate(sentences):
        sentence['combined_sentence_embedding'] = embeddings[i]
    return sentences


def calculate_cosine_distances(sentences):
    distances = []
    for i in range(len(sentences) - 1):
        embedding_current = sentences[i]['combined_sentence_embedding']
        embedding_next = sentences[i + 1]['combined_sentence_embedding']
        # Calculate cosine similarity
        similarity = cosine_similarity([embedding_current], [embedding_next])[0][0]
        # Convert to cosine distance
        distance = 1 - similarity
        # Append cosine distance to the list
        distances.append(distance)
        # Store distance in the dictionary
        sentences[i]['distance_to_next'] = distance

    # Optionally handle the last sentence
    # sentences[-1]['distance_to_next'] = None  # or a default value
    return distances, sentences

# Create a list to hold the grouped sentences
def create_chunks(sentences,indices_above_thresh):
    chunks = []
    start_index = 0
    # Iterate through the breakpoints to slice the sentences
    for index in indices_above_thresh:
        # The end index is the current breakpoint
        end_index = index
        # Slice the sentence_dicts from the current start index to the end index
        group = sentences[start_index:end_index + 1]
        combined_text = ' '.join([d['sentence'] for d in group])
        chunks.append(combined_text)
        # Update the start index for the next group
        start_index = index + 1
    # The last group, if any sentences remain
    if start_index < len(sentences):
        combined_text = ' '.join([d['sentence'] for d in sentences[start_index:]])
        chunks.append(combined_text)
    return chunks

def embedding(model,chunks):
    text_splitter = SemanticChunker(model)
    docs = text_splitter.create_documents(chunks)
    return docs

def doc2langchain_document(document):
    chunks = []
    sentences = split_document(document)
    sentences = combine_sentences(sentences)
    sentences = add_combined_sentence_embedding(sentences,model)
    distances, sentences = calculate_cosine_distances(sentences)
    #==================================
    if len(distances) > 0:
        breakpoint_percentile_threshold = 95
        breakpoint_distance_threshold = np.percentile(distances, breakpoint_percentile_threshold)
        indices_above_thresh = [i for i, x in enumerate(distances) if x > breakpoint_distance_threshold]

    # #==================================
        # Initialize the start index
        chunks = create_chunks(sentences,indices_above_thresh)
    else:
        for segment in sentences:
            chunks.append(segment['sentence'])
    return chunks


model = FlagModel('BAAI/bge-large-zh-v1.5', 
                  query_instruction_for_retrieval="为这个句子生成表示以用于检索相关文章：",
                  use_fp16=True) 

model_name = '/hdd-6tb/nghiavm/DATN/model/bge-large-en'
hf_embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
)

chunkings = []
root_dir = '/hdd-6tb/nghiavm/DATN/data_extract/data_haui'
for document_file in tqdm(os.listdir(root_dir), desc="Processing Files"):
    file_name = os.path.join(root_dir, document_file)
    with open(file_name, 'r', encoding='utf-8') as data_file:
        document = data_file.read()
        # document = document.replace('\n=======\n','')
        data_file.close()
    chunkings.append(doc2langchain_document(document))
    
    
chunks = [element for sublist in chunkings for element in sublist]
docs = embedding(hf_embeddings,chunks)

vectorstore = QdrantVectorStore.from_documents(
    documents=docs,
    index_name='datn_haui',
    embedding=hf_embeddings,
    path="/hdd-6tb/nghiavm/DATN/vector_store", 
    collection_name="datn_haui",
)
