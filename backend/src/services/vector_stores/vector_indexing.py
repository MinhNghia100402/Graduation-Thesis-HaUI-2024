from langchain.indexes import SQLRecordManager, index
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_qdrant.fastembed_sparse import FastEmbedSparse
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore, RetrievalMode
from langchain_experimental.text_splitter import SemanticChunker
import os


class Vector_store():
    def __init__(self,path_model_embedding):
        self.path_model_embedding = path_model_embedding
        self.sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")
        self.hf_embeddings = HuggingFaceEmbeddings(model_name=path_model_embedding)
        self.regex = r'\n\n'
        self.text_splitter = SemanticChunker(self.hf_embeddings,breakpoint_threshold_type="standard_deviation",breakpoint_threshold_amount=0.8,sentence_split_regex=self.regex)
    
    def save_vector(self,path_store_vector,db_url,collection_name,index_name,documents_value,documents):
        name_col = collection_name
        namespace = f"qdrant/{name_col}"
        record_manager = SQLRecordManager(
            namespace, db_url= db_url
            # namespace, db_url=f"sqlite:///./../../databases/custom_haui.sql"
        )
        record_manager.create_schema()
        
        vectorstore = QdrantVectorStore.from_documents(
                    documents=documents,
                    index_name=index_name,
                    embedding=self.hf_embeddings,
                    path=path_store_vector, 
                    collection_name=collection_name,
                    )
        index(documents_value, record_manager, vectorstore, cleanup="incremental", source_id_key="source")
        print("Vector storage done!")

        
    

# model_name = '/hdd-6tb/nghiavm/DATN/model/fine-tune/bge-large-finetune'

# hf_embeddings = HuggingFaceEmbeddings(
#     model_name=model_name,
# )
# sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")

# root_data = '/hdd-6tb/nghiavm/DATN/data_QA'
# regex = r'(?<=[A-Za-z])(?=[.?!])(?=\s)'
# text_splitter = SemanticChunker(hf_embeddings,breakpoint_threshold_type="standard_deviation",breakpoint_threshold_amount=0.8,sentence_split_regex=regex)

# docs = []
# document = [] 
# len_documen = 0
# for folder in os.listdir(root_data):
#     new_root = os.path.join(root_data,folder)
#     for khoa in os.listdir(new_root):
#         new_khoa  = os.path.join(new_root,khoa)
#         for file_txt in os.listdir(new_khoa):

#             file_name = os.path.join(new_khoa,file_txt)
#             with open(file_name,'r') as file:
#                 data_txt = file.readlines()
#                 file.close()
#             content_pages = data_txt[0].strip()+ ' ' +data_txt[1].strip()
#             doc = Document(page_content=f'{khoa}', metadata={"source": f'{file_name}'})
#             docs.append(doc)
#             with open(file_name,'r') as file_data:
#                 data = file_data.read()
#                 len_documen+=len([data])
#                 document.append(text_splitter.create_documents([data]))
#             file_data.close()
        
# collection_name = "datn"
# namespace = f"qdrant/{collection_name}"
# record_manager = SQLRecordManager(
#     namespace, db_url="sqlite:///./../database/custom_haui.sql"
# )
# record_manager.create_schema()

# document_text = []

# for doc in document:
#     for page in doc:
#         document_text.append(page)
# vectorstore = QdrantVectorStore.from_documents(
#     documents=document_text,
#     index_name='datn_final',
#     embedding=hf_embeddings,
#     path="/hdd-6tb/nghiavm/DATN/vector_store", 
#     collection_name="datn_final",
# )


# # index(docs, record_manager, vectorstore, cleanup="incremental", source_id_key="source")