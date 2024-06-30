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

http://57.181.31.178:8080


## コンテナ環境に入る
```bash
# 起動中のコンテナの確認
docker ps

# コンテナ何に入る
docker exec -it autores-demo /bin/bash
```

## Coderの実行
```
base_file_path = "/home/ec2-user/Mockup_python/src/test/base_model.py"
new_method_path = "/home/ec2-user/Mockup_python/src/test/new_method.txt"
save_file_path="/home/ec2-user/Mockup_python/src/test/exec_code.py"
```
