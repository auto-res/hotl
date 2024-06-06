# webUI関連



## Streamlitの起動
```bash
コンテナの起動
bash run.sh up

# イメージのビルドとコンテナの起動
bash run.sh force

# コンテナの停止
bash run.sh down

# コンテナの停止とイメージの削除
bash run.sh rm
```

## WebUIへのアクセス
 
http://13.231.244.48:8080


## コンテナ環境に入る
```bash
# 起動中のコンテナの確認
docker ps

# コンテナ何に入る
docker exec -it autores-demo /bin/bash
```
