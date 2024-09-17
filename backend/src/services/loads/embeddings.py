from langchain_huggingface.embeddings import HuggingFaceEmbeddings

class HF_Embeddings():
    def __init__(self,model_path):
        self.model_path = model_path

    def load_embeddings(self):
        hf_embeddings = HuggingFaceEmbeddings(model_name=self.model_path)
        return hf_embeddings