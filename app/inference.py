import os
import time
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from model import load_model, perform_inference, focalnet_dino_dir
from server import InferenceQueue, InferenceResult, engine, SessionLocal

# モデルのロード（最初に一回だけ実行）
model_config_path = f"{focalnet_dino_dir}/config/DINO/DINO_5scale_focalnet_large_fl4.py"
model_checkpoint_path = "./models/focalnet_large_fl4_o365_finetuned_on_coco.pth"
model, postprocessors, id2name = load_model(model_config_path, model_checkpoint_path)

def inference_loop():
    session = SessionLocal()
    while True:
        # 推論待ちの画像を取得
        inference_request = session.query(InferenceQueue).order_by(InferenceQueue.request_time).first()
        if inference_request:
            try:
                # 推論実行
                result = perform_inference(model, postprocessors, inference_request.file_path, id2name)

                # 推論結果をデータベースに保存
                inference_result = InferenceResult(request_id=inference_request.request_id, result=result)
                session.add(inference_result)
                session.commit()

                # 推論待ちテーブルからレコードを削除
                session.delete(inference_request)
                session.commit()

                # 画像を削除
                os.remove(inference_request.file_path)
            except Exception as e:
                print(f"Error occurred while processing inference request: {e}")

        else:
            # 推論待ちの画像がない場合は0.01秒間隔で確認
            time.sleep(0.01)

if __name__ == "__main__":
    inference_loop()
