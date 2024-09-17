from fastapi import APIRouter, Depends, Request
from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from fastapi.responses import StreamingResponse
import os
import torch
import gc
from fastapi import FastAPI,Request
from pydantic import BaseModel
from dotenv import load_dotenv

from src.services.loads.embeddings import HF_Embeddings
from src.services.loads.llms import Llama3_loader
from src.services.loads.load_collection import Load_collection
from src.services.loads.reranker import Reranker_loader
from src.routers.promt import create_messages

load_dotenv()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

router = APIRouter()

# define model 
model_llm_id = os.environ.get('LLM_MODEL')
model_embedding_path = os.environ.get('EMBEDDING_MODEL')
model_reranker_path = os.environ.get('BGE_RERANKER_MODEL')
path_vector_store = os.environ.get('PATH_VECTOR_STORE')
qdrant_fast_embedding = os.environ.get('QDRANT_FAST_EMBEDDING')
collection_name = os.environ.get('COLLECTION_NAME')

#get function class
llm = Llama3_loader(model_id = model_llm_id)
hf_embedding_model = HF_Embeddings(model_path = model_embedding_path)
hf_embedding = hf_embedding_model.load_embeddings()

qdrant_collection = Load_collection(
                            hf_embeddings = hf_embedding,
                            collection_path_dir = path_vector_store,
                            collection_name = collection_name
                            )
qdrant = qdrant_collection.load()

reranker = Reranker_loader(path_model=model_reranker_path)
# reranker = reranker_model.reranker


@router.post("/query")
async def create_item(request: Request):
    # Receive data from POST request
    body = await request.body()
    body_text = body.decode('utf-8')
    query = body_text

    # Perform search and data processing
    found_docs = qdrant.max_marginal_relevance_search(query, k=10, fetch_k=10)
    scores = reranker.reranking(query, found_docs)

    #create promt 
    new_query, system_content = create_messages(
                                            scores=scores,
                                            found_docs=found_docs,
                                            query=query
                                            )
    messages = llm.prompt(new_query,system_content)
    
    answer = llm.generator(messages = messages)
    if isinstance(answer, str):
        response = answer.encode('utf-8')

    # Create a generator for streaming the response
    def generate():
        chunk_size = 1024  # Size of each chunk
        for i in range(0, len(response), chunk_size):
            yield response[i:i+chunk_size]

    return StreamingResponse(generate(), media_type='text/plain')




