import transformers
import torch

class Llama3_loader():
    def __init__(self,model_id,device_map="auto",torch_dtype=torch.bfloat16):
        # self.path_model_llm = path_model_llm
        self.model_id = model_id
        self.device_map = device_map
        self.torch_dtype = torch_dtype
        
        self.pipeline = self.load_llm()

    def load_llm(self):

        model_id = self.model_id
        pipeline = transformers.pipeline(
            "text-generation",
            model=model_id,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device_map=self.device_map,
        )
        return pipeline 
    
    def prompt(self,query,system_content):
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": query},
        ]
        return messages

    def generator(self, messages, max_new_tokens=1024):
        outputs = self.pipeline(
            messages,
            max_new_tokens=max_new_tokens,
        )
        return outputs[0]['generated_text'][-1]['content']