# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 23:31:33 2024

@author: Yz
"""


from openai import OpenAI
import json
import os
from src.AplusB import AplusB
from src.gen_code import PRO
import subprocess
from autoresevaluator import AutoResEvaluator


class main_loop():
    def __init__(self,api_key,GPT_id,M_pseudocode,Ad_pseudocode,M_name,A_name,reference_python):
        self.api_key = api_key
        self.GPT_id = GPT_id
        self.M_pseudocode = M_pseudocode
        self.Ad_pseudocode = Ad_pseudocode
        self.client = OpenAI(
            api_key = api_key,
            )
        self.M_name = M_name
        self.A_name = A_name
        self.reference_python = reference_python
        self.mix_python = ""
        self.program2 = ""
        self.think = ""
        self.think2 = ""
        self.python2_1 = ""
        self.python2_2 = ""

    def main_loop(self):
        default_message = """貴方は研究者です．あなたのタスクは2つの手法を組み合わせることによって新規手法を生み出し，その結果を考察することです．
研究の流れは以下の流れで行われます．
1. 新規手法の擬似アルゴリズムの作成
2. 新規手法の検証のためのプログラム生成
3. 新規手法の有効性の証明
4. 研究完了

上記に示した流れはそれぞれ事前に準備したPythonプログラムを実行することによって行うことができます．
1.を実行する際には出力フォーマットの研究の流れに"Creation of pseudo-algorithms"と記載してください．
2.を実行する際には出力フォーマットの研究の流れに"Creating Python Programs"と記載してください．
3.を実行する際には出力フォーマットの研究の流れに"Proof of Validity"と記載してください．
4.を実行する際には出力フォーマットの研究の流れに"Study Completed"と記載してください．

また，上記の研究の流れの2.に関して作成されたプログラムを実行した結果エラーになる可能性があります．
その際は，どのように修正すればよいかなどのアドバイスを出力フォーマットのコメントに記載してください．
アドバイスがない場合は何も記入しないでください．

出力フォーマットはJSON形式です．
出力フォーマット：
{"研究の流れ":"研究の流れ", "コメント"："コメント"}
"""

        messages = [
            {
                    "role": "system",
                    "content": f"""{default_message}"""
            }
            ]
        
        
        
        old_log = []
        messages = messages + old_log
        
        for i in range(5):
          chat_completion = self.client.chat.completions.create(
            model=self.GPT_id,
            messages=messages,
            temperature = 0.0
          )
          ans = chat_completion.choices[0].message.content
          old_log =[
            {
                    "role": "assistant",
                    "content": ans
            }
            ]
          messages = messages + old_log
          ans_json = json.loads(ans)
          print(ans_json['研究の流れ'])
        
        
          if ans_json['研究の流れ'] == "Creation of pseudo-algorithms":
            AB = AplusB(self.api_key,self.GPT_id,self.M_pseudocode,self.Ad_pseudocode,self.M_name,self.A_name)
            mix_python,think,think2,python2_1,python2_2 = AB.M2_code_gen()
            result = mix_python
            print(mix_python)
            self.mix_python = mix_python
            self.think = think
            self.think2 = think2
            self.python2_1 = python2_1
            self.python2_2 = python2_2
        
          elif ans_json['研究の流れ'] == "Creating Python Programs":
            if 'mix_python' in locals():
              print('ON!!')
              pro1 = PRO(self.api_key,self.GPT_id,self.M_name,mix_python,self.reference_python)
              program2 = pro1.gen_program()
              result = program2
              self.program2 = program2

              os.makedirs("output", exist_ok=True)
              f = open("./output/M2_code.py","w")
              f.write(program2)
              f.close()
              f = open("./output/M_code.py","w")
              f.write(self.reference_python)
              f.close()
            else:
              result = "新規手法の擬似アルゴリズムが作成されていません"
        
          elif ans_json['研究の流れ'] == "Proof of Validity":
            if 'program2' in locals():
              print("M2_Start")
              params = {
                  'lr': {'type': 'log_float', 'args': [1e-5, 1e-3]}
              }
              #params = {
              #    'learning_rate': {'type': 'log_float', 'args': [1e-8, 0.1]},
              #    'iterations': {'type': 'log_float', 'args': [100, 1000]},
              #    "lambda": 1
              #}
              model_path='/content/drive/MyDrive/Autores/Mockup_pipline2/output/M2_code.py'
              are = AutoResEvaluator(
                    llm_name='gpt-4-turbo-preview',
                    dataset_name='cifar10',
                    valuation_index='accuracy',
                    datasave_path='./data',
                    params=params,
                    )
              are.exec(model_path)
              if not os.path.isfile("result.log"):
                with open("result.log",mode='x') as f:
                  s = f.read()
              else:
                with open("result.log",mode='w') as f:
                  s = f.read()
              output2 = s.split("\n")
              output2 = output2[len(output2)-3:]

              
              print("M1_Start")
              params = {
                  'lr': {'type': 'log_float', 'args': [1e-5, 1e-3]}
              }
              #params = {
              #    'learning_rate': {'type': 'log_float', 'args': [1e-8, 0.1]},
              #    'iterations': {'type': 'log_float', 'args': [100, 1000]},
              #    "lambda": 1
              #}
              model_path='/content/drive/MyDrive/Autores/Mockup_pipline2/output/M_code.py'
              
              are = AutoResEvaluator(
                    llm_name='gpt-4-turbo-preview',
                    dataset_name='cifar10',
                    valuation_index='accuracy',
                    datasave_path='./data',
                    params=params,
                    )
              are.exec(model_path)
              with open("result.log") as f:
                  s = f.read()
              output1 = s.split("\n")
              output1 = output1[len(output1)-3:]


              old_log = [
                    {
                            "role": "user",
                            "content": f"""以下の対象手法Mと対象手法M'の2つの擬似アルゴリズムを比較のため先ほど生成したプログラムを実行すると以下のような結果を得た．
それぞれの結果を比較しどちらがどのように良いのかを考察しなさい．

(対象手法Mの実行結果)
{output1}

(対象手法M'の実行結果)
{output2}
"""		
                    },
                    ]
              messages = messages + old_log
              chat_completion = self.client.chat.completions.create(
                model=self.GPT_id,
                messages=messages,
                temperature = 0.0
                )
              consideration = chat_completion.choices[0].message.content
              old_log =[
                {
                        "role": "assistant",
                        "content": consideration
                }
                ]
              messages = messages + old_log
              result = consideration
        
            else:
              result = "新規手法の検証のためのプログラムが生成されていません"
        
          elif ans_json['研究の流れ'] == "Study Completed":
            
            old_log = [
                  {
                          "role": "user",
                          "content": f"""研究で得られた成果物を用いてレポートを作成しなさい．レポートの構成としては以下の通りです．
・既存研究
・新規手法の提案
・検証
・考察

既存研究では対象手法Mの概要に関して記載しなさい．その際の参考となるのは以下の対象手法MのPythonコードである．
{self.reference_python}

検証ではどのようなプログラムを用いてどのような観点で検証を行ったのか，またその結果はどうだったのかを記載しなさい．その際の参考となるのは以下の検証のために生成したプログラム，以下の実行結果である．
また必ず実際に得られたスコアを記載しなさい．
(対象手法Mプログラム)
{self.reference_python}
(対象手法M'プログラム)
{program2}
(対象手法M実行結果)
{output1}
(対象手法M'実行結果)
{output2}

考察では先ほど考察した内容をまとめて記載しなさい．要点としてはどちらの手法がよかったのか，どのように良かったのかを記載しなさい．
{consideration}
"""		
                    },
                  ]
            messages = messages + old_log
            chat_completion = self.client.chat.completions.create(
              model=self.GPT_id,
              messages=messages,
              temperature = 0.0
              )
            Report = chat_completion.choices[0].message.content
            f = open('./output/Report.txt', 'w')
            f.write(Report)
            f.close()
            break
        
          else:
            print(ans_json['研究の流れ'])
            print("error")
        
        
          messages = messages + [
            {
                    "role": "user",
                    "content": f"""{ans_json['研究の流れ']}を行った結果以下の結果を得ました．
結果から次に行うべき判断を以下の研究の流れからしてください．
(研究の流れ)
1. 新規手法の擬似アルゴリズムの作成
2. 新規手法の検証のためのプログラム生成
3. 新規手法の有効性の証明
4. 研究完了

1.を実行する際には出力フォーマットの研究の流れに"Creation of pseudo-algorithms"と記載してください．
2.を実行する際には出力フォーマットの研究の流れに"Creating Python Programs"と記載してください．
3.を実行する際には出力フォーマットの研究の流れに"Proof of Validity"と記載してください．
4.を実行する際には出力フォーマットの研究の流れに"Study Completed"と記載してください．

出力フォーマットはJSON形式です．
出力フォーマット：
{{"研究の流れ":"研究の流れ", "コメント"："コメント"}}

(結果)
{result}
        """
            }
            ]

        return mix_python,program2,think,think2,python2_1,python2_2
