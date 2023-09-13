import json
import os
import sys
import time

import cv2
import numpy as np
import torch
from torchvision.transforms import functional as T
from PIL import Image

focalnet_dino_dir = "/vendor/FocalNet-DINO/"
sys.path.append(focalnet_dino_dir)  # noqa

import datasets.transforms as T  # noqa
from main import build_model_main  # noqa
from util.slconfig import SLConfig  # noqa
from datasets import build_dataset  # noqa

def load_model(model_config_path, model_checkpoint_path, device='cuda'):
    args = SLConfig.fromfile(model_config_path)
    args.device = device
    model, criterion, postprocessors = build_model_main(args)

    checkpoint = torch.load(model_checkpoint_path, map_location='cpu')
    model.load_state_dict({k.split(".", 1)[1]: v for k, v in checkpoint['model'].items()})
    model.eval()

    # Load coco names
    with open(f"{focalnet_dino_dir}/util/coco_id2name.json") as f:
        id2name = json.load(f)
        id2name = {int(k): v for k, v in id2name.items()}

    return model, postprocessors, id2name


# def perform_inference(model, postprocessors, image_path, confidence_threshold=0.5, device='cuda'):
def perform_inference(model, postprocessors, image_path, id2name, confidence_threshold=0.5, device='cuda'):  # ChatGPT生成コードを修正
    image = Image.open(image_path).convert("RGB")
    size = [image.height, image.width]
    # transform = Compose([
    transform = T.Compose([  # ChatGPT生成コードを修正
        T.RandomResize([800], max_size=1333),
        T.ToTensor(),
        T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    input_, _ = transform(image, None)
    model = model.to(device)
    with torch.no_grad():
        output = postprocessors["bbox"](model([input_.to(device)]), torch.Tensor([size]).to(device))[0]

    # Convert tensors to numpy arrays
    scores = output["scores"].cpu().numpy()
    labels = output["labels"].cpu().numpy()
    boxes = output["boxes"].cpu().numpy()

    # Filter results based on confidence threshold
    mask = scores >= confidence_threshold
    scores = scores[mask]
    labels = labels[mask]
    boxes = boxes[mask]

    # Convert label indices to label names
    label_names = [id2name[label] for label in labels]

    # Organize results in the requested format
    results = []
    for label_name, score, box in zip(label_names, scores, boxes):
        result = {
            "label": label_name,
            # "score": score,
            "score": float(score),  # ChatGPT生成コードを修正
            "box": box.tolist()
        }
        results.append(result)

    return results
