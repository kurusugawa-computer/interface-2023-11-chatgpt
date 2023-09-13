#!/bin/bash
echo "Downloading models..."
cd "$(dirname "$0")" || exit 1
if [[ ! -e focalnet_large_lrf_384_fl4.pth ]]; then
  curl -OL https://github.com/microsoft/FocalNet/releases/download/v1.0.0/focalnet_large_lrf_384_fl4.pth
fi
mkdir -p models
cd models || exit 1
if [[ ! -e focalnet_large_fl4_o365_finetuned_on_coco.pth ]]; then
  curl -OL https://huggingface.co/microsoft/focalnet-large-fl4-dino-o365-cocoft/resolve/main/focalnet_large_fl4_o365_finetuned_on_coco.pth
fi
