from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    filename: str
    num_chars: int
