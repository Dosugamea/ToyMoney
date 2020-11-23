# Pythonイメージの取得
FROM python:3.8.6-slim-buster AS compile-image
RUN apt-get update && apt-get install -y gcc libmariadb-dev && apt-get -y clean && rm -rf /var/lib/apt/lists/*
COPY requirements.txt requirements.txt
RUN python -m venv /opt/venv
RUN pip install --user -r requirements.txt

# 必要なファイルだけコピー
FROM python:3.8.6-slim-buster AS build-image
RUN apt-get update && apt-get install -y libmariadb-dev && apt-get -y clean && rm -rf /var/lib/apt/lists/*
COPY --from=compile-image /root/.local /root/.local
WORKDIR /usr/local/app
ENV PATH=/root/.local/bin:$PATH
COPY . .
# 起動環境設定
EXPOSE 5000
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]