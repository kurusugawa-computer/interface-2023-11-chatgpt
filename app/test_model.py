import cv2
import numpy as np

# モデルの読み込みと推論部分の関数を定義したコードをここに追加する（load_modelとperform_inference関数）
from model import load_model, perform_inference, focalnet_dino_dir

# def visualize_detection(image_path, model, postprocessors, confidence_threshold=0.5, device='cuda'):
def visualize_detection(image_path, model, postprocessors, id2name,confidence_threshold=0.5, device='cuda'):  # ChatGPT生成コードを修正
    # 物体検出を実行して結果を取得
    # results = perform_inference(model, postprocessors, image_path, confidence_threshold, device)
    results = perform_inference(model, postprocessors, image_path, id2name, confidence_threshold, device)  # ChatGPT生成コードを修正

    # 画像を読み込んでOpenCVの形式に変換
    image = cv2.imread(image_path)

    # 検出結果を画像上に描画
    for result in results:
        label = result["label"]
        score = result["score"]
        box = result["box"]

        xmin, ymin, xmax, ymax = box
        xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)

        # 枠の色を設定（ランダム）
        color = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))

        # 枠の描画
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 2)

        # ラベルと確信度の表示
        label_text = f"{label}: {score:.2f}"
        cv2.putText(image, label_text, (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # 可視化結果を画像として表示
    cv2.imshow("Object Detection", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 動作確認用の画像パスを指定
image_path = "images/idea.jpg"

# モデルの読み込み
model_config_path = f"{focalnet_dino_dir}/config/DINO/DINO_5scale_focalnet_large_fl4.py"
model_checkpoint_path = "./models/focalnet_large_fl4_o365_finetuned_on_coco.pth"
model, postprocessors, id2name = load_model(model_config_path, model_checkpoint_path)

# 可視化を実行
# visualize_detection(image_path, model, postprocessors, confidence_threshold=0.5, device='cuda')
visualize_detection(image_path, model, postprocessors, id2name, confidence_threshold=0.5, device='cuda')  # ChatGPT生成コードを修正
