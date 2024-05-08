from datetime import datetime
from pydantic import BaseModel


class MessageSchema(BaseModel):
    id: str | int | None
    user_id: str
    name: str | None
    text: str
    created_at: datetime