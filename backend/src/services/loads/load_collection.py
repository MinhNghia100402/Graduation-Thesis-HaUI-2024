from langchain_qdrant import QdrantVectorStore, RetrievalMode


class Load_collection():
    def __init__(self,hf_embeddings,collection_path_dir,collection_name):
        self.hf_embeddings = hf_embeddings
        self.collection_name = collection_name
        self.collection_path_dir = collection_path_dir

    def load(self):
        qdrant = QdrantVectorStore.from_existing_collection(
            embedding=self.hf_embeddings,
            collection_name=self.collection_name,
            path=self.collection_path_dir
        )
        return qdrant