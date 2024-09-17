from src.services.vector_stores.vector_indexing import Vector_store
from src.services.utils.extract_data import ExtratData
import json 
import os
from tqdm import tqdm
from dotenv import load_dotenv
load_dotenv()


link_json_file = os.environ.get('LINK_FILE_JSON')
path_model_embedding = os.environ.get('EMBEDDING_MODEL')
path_file_data = os.environ.get('PATH_FILE_DATA')

extract_data = ExtratData()

def dataloader(path_file_data):
    file_loader = []
    for path_folder in os.listdir(path_file_data):
        new_path = os.path.join(path_file_data, path_folder)
        
        for index, file_name in enumerate(tqdm(os.listdir(new_path), desc='Processing file loader')):
            file_path = os.path.join(new_path, file_name)
            loader, known_type = extract_data.file_loader(file_path)
            file_loader.append(loader)
            
    # documents_loader = websites_loader + file_loader
    return file_loader

document_loader = dataloader(path_file_data)

documents_value = [doc.load() for doc in document_loader]
# vector store 
vector_store = Vector_store(path_model_embedding)

path_store_vector = os.environ.get('PATH_VECTOR_STORE')
db_url = os.environ.get('DB_URL')
collection_name = os.environ.get('COLLECTION_NAME')
index_name =os.environ.get('INDEX_NAME')
text_splitter=vector_store.text_splitter 
print('================ crawl done ============')

# documents = [text_splitter.create_documents([doc.load()[0].page_content]) for doc in documents_value]
documents = []
for index,doc in enumerate(tqdm(documents_value,desc='processing create document :')):
    # data = str(doc.load()[0].page_content)
    
    documents.append(text_splitter.create_documents([doc[0].page_content]))
#create segmantic chunker
documents = [doc[0] for doc in documents]
documents_value = [doc[0] for doc in documents_value]
print('================ create document done  ============')

vector_store.save_vector(path_store_vector,db_url,collection_name,index_name,documents_value,documents)
print('Vectors store done !') 