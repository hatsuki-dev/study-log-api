from sqlalchemy import Column, Integer, String, Date
from database import Base


class StudyLog(Base):
    __tablename__ = "study_logs"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    title = Column(String)
    content = Column(String)
    study_time = Column(Integer)
    tag=Column(String)
