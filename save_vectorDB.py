from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient(url="https://af7379dc-7638-49c6-b92e-94efb24c5e7a.us-east4-0.gcp.cloud.qdrant.io")

client.recreate_collection(
    collection_name="startups",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)