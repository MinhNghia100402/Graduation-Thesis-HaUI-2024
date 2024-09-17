from typing import List
from pydantic import BaseModel

class RequestChat(BaseModel):
    input_text: str
    max_lengt = 8192