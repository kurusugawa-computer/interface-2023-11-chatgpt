FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu22.04

RUN export DEBIAN_FRONTEND=noninteractive \
  && rm -f /etc/apt/sources.list.d/cuda* \
  && apt update \
  && apt install -y --no-install-recommends \
    language-pack-ja-base \
    language-pack-ja \
    tzdata \
    python3.10 \
    python3.10-dev \
    python3-pip \
    python3-tk \
    tk-dev \
    libgl1-mesa-dev \
    libopencv-dev \
    curl \
    zip \
    unzip \
    git \
    jq \
  && apt clean \
  && rm -rf /var/lib/apt/lists/*

RUN update-locale LANG=ja_JP.UTF-8 LANGUAGE=ja_JP:ja \
  && ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime \
  && echo "Asia/Tokyo" > /etc/timezone

ENV LANG=ja_JP.UTF-8 \
  LC_ALL=ja_JP.UTF-8 \
  LC_CTYPE=ja_JP.UTF-8

RUN ln -sf "$(which python3)" "/usr/bin/python"

WORKDIR /
COPY ./requirements.txt .

WORKDIR /vendor
RUN git clone https://github.com/FocalNet/FocalNet-DINO.git \
  && cd FocalNet-DINO \
  && git checkout 23901e021dc6ec8f66bad47983f45a25574452cc

WORKDIR /
RUN pip install -U pip setuptools \
  && pip install -r requirements.txt

RUN echo "cd /vendor/FocalNet-DINO/models/dino/ops && pip install ." > /setup.sh \
  && chmod +x /setup.sh

WORKDIR /workspace
