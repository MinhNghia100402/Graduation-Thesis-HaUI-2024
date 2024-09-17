from pydantic import BaseModel

class InputChat(BaseModel):
    query: str