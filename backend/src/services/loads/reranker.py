
from FlagEmbedding import FlagReranker
class Reranker_loader():
    def __init__(self,path_model,device='cuda'):
        self.path_model =path_model
        self.device = device
        self.reranker = self.load_model_reranker()

    def load_model_reranker(self):
        reranker = FlagReranker(
                model_name_or_path=self.path_model, 
                use_fp16=True,
                device= self.device,
            ) 
        return reranker
    
    def reranking(self,query, found_docs):
        scores = []
        for index, doc in enumerate(found_docs):
            score = self.reranker.compute_score([query,doc.page_content])
            scores.append((index, score)) 
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

        return sorted_scores
