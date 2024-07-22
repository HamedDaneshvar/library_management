from pydantic import BaseModel


class Status(BaseModel):
    title: str


class StatusCreate(Status):
    pass


class StatusUpdate(Status):
    pass
