from pydantic import BaseModel, UUID4
from datetime import datetime

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID4: lambda v: str(v),
        }

class IDSchema(BaseSchema):
    id: UUID4