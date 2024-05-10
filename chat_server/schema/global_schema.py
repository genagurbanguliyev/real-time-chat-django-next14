from datetime import datetime
from pydantic import BaseModel

class UserSchema(BaseModel):
    id: str
    name: str | None


class MessageSchema(BaseModel):
    id: str | int | None
    user: UserSchema
    text: str
    created_at: datetime