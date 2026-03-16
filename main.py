from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from datetime import date, timedelta

import models
import schemas
from database import SessionLocal, engine

# DB作成
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------
# DBセッション
# ----------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------
# Create（学習ログ作成）
# ----------------------
@app.post("/logs", response_model=schemas.StudyLog)
def create_log(log: schemas.StudyLogCreate, db: Session = Depends(get_db)):
    db_log = models.StudyLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


# ----------------------
# Read（一覧取得）
# ----------------------
@app.get("/logs", response_model=List[schemas.StudyLog])
def read_logs(tag: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.StudyLog)

    if tag:
        query = query.filter(models.StudyLog.tag == tag)

    logs = query.all()

    return logs


# ----------------------
# 合計学習時間
# ----------------------
@app.get("/logs/total-time")
def get_total_time(db: Session = Depends(get_db)):
    total = db.query(func.sum(models.StudyLog.study_time)).scalar()

    if total is None:
        total = 0

    return {"total_time": total}


# ----------------------
# 過去7日間ログ
# ----------------------
@app.get("/logs/weekly", response_model=List[schemas.StudyLog])
def get_weekly_logs(db: Session = Depends(get_db)):

    today = date.today()
    week_ago = today - timedelta(days=7)

    logs = db.query(models.StudyLog).filter(
        models.StudyLog.date >= week_ago
    ).all()

    return logs


# ----------------------
# 学習統計
# ----------------------
@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):

    logs = db.query(models.StudyLog).all()

    total_time = sum(log.study_time for log in logs)
    log_count = len(logs)

    today = date.today()
    week_ago = today - timedelta(days=7)

    weekly_logs = db.query(models.StudyLog).filter(
        models.StudyLog.date >= week_ago
    ).all()

    weekly_time = sum(log.study_time for log in weekly_logs)

    return {
        "total_time": total_time,
        "weekly_time": weekly_time,
        "log_count": log_count
    }


# ----------------------
# タグ別学習時間
# ----------------------
@app.get("/stats/tags")
def tag_stats(db: Session = Depends(get_db)):

    logs = db.query(models.StudyLog).all()

    result = {}

    for log in logs:
        if log.tag in result:
            result[log.tag] += log.study_time
        else:
            result[log.tag] = log.study_time

    return result


# ----------------------
# 学習ランキング
# ----------------------
@app.get("/stats/ranking")
def tag_ranking(db: Session = Depends(get_db)):

    logs = db.query(models.StudyLog).all()

    result = {}

    for log in logs:
        if log.tag in result:
            result[log.tag] += log.study_time
        else:
            result[log.tag] = log.study_time

    ranking = sorted(result.items(), key=lambda x: x[1], reverse=True)

    return ranking


# ----------------------
# Read（1件取得）
# ----------------------
@app.get("/logs/{log_id}", response_model=schemas.StudyLog)
def read_log(log_id: int, db: Session = Depends(get_db)):

    log = db.query(models.StudyLog).filter(models.StudyLog.id == log_id).first()

    if log is None:
        raise HTTPException(status_code=404, detail="Log not found")

    return log


# ----------------------
# Update（編集）
# ----------------------
@app.put("/logs/{log_id}", response_model=schemas.StudyLog)
def update_log(log_id: int, log: schemas.StudyLogCreate, db: Session = Depends(get_db)):

    db_log = db.query(models.StudyLog).filter(models.StudyLog.id == log_id).first()

    if db_log is None:
        raise HTTPException(status_code=404, detail="Log not found")

    db_log.date = log.date
    db_log.title = log.title
    db_log.content = log.content
    db_log.study_time = log.study_time

    db.commit()
    db.refresh(db_log)

    return db_log


# ----------------------
# Delete（削除）
# ----------------------
@app.delete("/logs/{log_id}")
def delete_log(log_id: int, db: Session = Depends(get_db)):

    db_log = db.query(models.StudyLog).filter(models.StudyLog.id == log_id).first()

    if db_log is None:
        raise HTTPException(status_code=404, detail="Log not found")

    db.delete(db_log)
    db.commit()

    return {"message": "deleted"}


# ----------------------
# AIアドバイス
# ----------------------
@app.get("/ai/advice")
def get_ai_advice(db: Session = Depends(get_db)):

    logs = db.query(models.StudyLog).all()

    if not logs:
        return {"advice": "まだ学習ログがありません。"}

    tag_time = {}

    for log in logs:
        if log.tag in tag_time:
            tag_time[log.tag] += log.study_time
        else:
            tag_time[log.tag] = log.study_time

    most_tag = max(tag_time, key=tag_time.get)

    advice = f"{most_tag}の学習が多いです。他の分野も少しずつ勉強するとバランスが良くなります。"

    return {"advice": advice}
