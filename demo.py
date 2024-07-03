from langchain_qdrant import Qdrant
# from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv()

QDRANDT_URL = os.getenv('QDRANDT_URL')
API_KEY = os.getenv('API_KEY')


docs ="aaaaa"

# qdrant_client = QdrantClient(
#     QDRANDT_URL,
#     api_key=API_KEY
# )

embeddings = HuggingFaceEmbeddings(
    model_name="dangvantuan/vietnamese-embedding"
)

text_splitter = SemanticChunker(
    embeddings, breakpoint_threshold_type="standard_deviation"
)

qdrant = Qdrant.from_documents(
    docs,
    embeddings,
    url=QDRANDT_URL,
    prefer_grpc=True,
    api_key=API_KEY,
    collection_name="my_documents",
)
print('okela')