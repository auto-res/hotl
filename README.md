# AutoRes自動研究


## 開発者向け
- [フォルダー構成](https://github.com/auto-res/Mockup_python/blob/develop/docs/folder.md)
- [環境構築](https://github.com/auto-res/Mockup_python/blob/develop/docs/environment_building)
- [開発ルール](https://github.com/auto-res/Mockup_python/blob/develop/docs/development_rule.md)


## リポジトリの説明





## 使い方
※整備中です

- Creator



- Coder
    - インスタンス化
```python
coder = Coder(
    llm_name = llm_name,
    save_dir="/Users/tanakatouma/vscode/Mockup_python/data/"
    )
```

    - 実行

```python
base_code_path = "/Users/tanakatouma/vscode/Mockup_python/data/base_model.txt"
new_method_path = "/Users/tanakatouma/vscode/Mockup_python/data/new_method.txt"
file_name = 'exec_code.py'

exec_code_path = coder.exec(base_code_path, new_method_path, file_name)
```

- Evaluator

```python
eval = Evaluator(
    llm_name=llm_name,
    dataset_name='cifar10',
    params=params,
    valuation_index='accuracy',
    datasave_path='../../data',
    n_trials=10,
    )
```

```python
result = eval.exec(exec_code_path)
```

