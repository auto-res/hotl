# streamlitがサポートしているのはpython3.7〜3.9
FROM python:3.9.13-slim
USER root

RUN apt-get update && apt-get install -y \
    locales \
    tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    
RUN locale-gen ja_JP.UTF-8

# environment
ENV LANG="ja_JP.UTF-8" \
    LANGUAGE="ja_JP:ja" \
    LC_ALL="ja_JP.UTF-8" \
    TZ="Asia/Tokyo"

#COPY . ~/streamlit

# Poetryをインストール
#RUN pip install poetry

# ワーキングディレクトリの設定
#WORKDIR /root

# pyproject.toml と poetry.lock ファイルをコピー
#COPY pyproject.toml poetry.lock ./
#COPY /root/pyproject.toml /root/poetry.lock ./

# 依存関係のインストール
#RUN poetry config virtualenvs.create false
#RUN poetry update
#RUN poetry install --no-dev

WORKDIR root/src/webui
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8080

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]
