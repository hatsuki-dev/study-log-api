from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLiteデータベースの場所
SQLALCHEMY_DATABASE_URL = "sqlite:///./study_logs.db"

# DBエンジン作成
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# セッション作成
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# モデルのベース
Base = declarative_base()
