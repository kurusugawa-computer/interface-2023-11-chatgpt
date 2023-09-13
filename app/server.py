# 必要なライブラリをインポート
import os
import uuid
from datetime import datetime
from pathlib import Path  # ChatGPT生成コードから追加
from fastapi import FastAPI, UploadFile, File
from sqlalchemy import create_engine, Column, String, Integer, JSON, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Path("uploaded_images").mkdir(parents=True, exist_ok=True)  # ChatGPT生成コードから追加

# FastAPIアプリの初期化
app = FastAPI()

# データベースの初期化
DATABASE_URL = "sqlite:///./inference_server.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 推論待ちテーブルのモデル定義
class InferenceQueue(Base):
    __tablename__ = "inference_queue"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String(36), unique=True, index=True)
    # file_path = Column(String(255), unique=True, index=True)
    file_path = Column(String(), unique=True, index=True)  # ChatGPT生成コードを修正
    request_time = Column(DateTime, index=True)

# 推論結果テーブルのモデル定義
class InferenceResult(Base):
    __tablename__ = "inference_result"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String(36), unique=True, index=True)
    result = Column(JSON)
    # processed = Column(Boolean, default=False)  # ChatGPT生成コードを修正

# テーブルの作成
Base.metadata.create_all(bind=engine)

# 推論APIのエンドポイント
@app.post("/inference/")
async def inference(file: UploadFile = File(...)):
    # ファイルの保存とリクエストIDの生成
    request_id = str(uuid.uuid4())
    file_path = os.path.join("uploaded_images", request_id + "_" + file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    request_time = datetime.now()

    # データベースにリクエストを追加
    db = SessionLocal()
    db.add(InferenceQueue(request_id=request_id, file_path=file_path, request_time=request_time))
    db.commit()
    db.close()

    return {"request_id": request_id}

# 結果取得APIのエンドポイント
@app.get("/result/{request_id}/")
async def get_result(request_id: str):
    db = SessionLocal()

    # 推論結果テーブルを検索
    result = db.query(InferenceResult).filter_by(request_id=request_id).first()

    if result is not None:
        # 推論結果がある場合は結果を返す
        db.close()
        return result.result
    else:
        # 推論結果がない場合は推論待ちテーブルを検索
        queued = db.query(InferenceQueue).filter_by(request_id=request_id).first()
        db.close()
        if queued is not None:
            return {"status": "queued"}
        else:
            return {"status": "not_found"}

# キューイング情報取得APIのエンドポイント
@app.get("/queue_info/")
async def get_queue_info():
    db = SessionLocal()
    count = db.query(InferenceQueue).count()
    db.close()
    return {"queued_images": count}
