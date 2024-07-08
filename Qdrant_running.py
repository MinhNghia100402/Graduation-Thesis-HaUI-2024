import getpass
import os

from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings

from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import Qdrant
from sentence_transformers import SentenceTransformer
from pyvi.ViTokenizer import tokenize

loader = TextLoader("./../Graduation-Thesis-HaUI-2024/data_proces.txt")

documents = loader.load()
text_splitter = SemanticChunker(OpenAIEmbeddings())

docs = text_splitter.split_documents(documents)



model = SentenceTransformer('dangvantuan/vietnamese-embedding')
embeddings = model.encode(tokenizer_sent)



qdrant = Qdrant.from_documents(
    docs,
    embeddings,
    location=":memory:",  # Local mode with in-memory storage only
    collection_name="my_documents",
)

