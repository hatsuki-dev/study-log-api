from pydantic import BaseModel
from datetime import date


class StudyLogBase(BaseModel):
    date: date
    title: str
    content: str
    study_time: int
    tag:str


class StudyLogCreate(StudyLogBase):
    pass


class StudyLog(StudyLogBase):
    id: int

    class Config:
        orm_mode = True
