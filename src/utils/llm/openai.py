from openai import OpenAI
import unittest
from unittest.mock import patch

def _openai_model(model_name, prompt):
    """
    Generate a completion using the OpenAI model.

    Args:
        model_name (str): The name of the OpenAI model to use.
        prompt (str): The user's prompt for generating the completion.

    Returns:
        str: The generated completion response.

    """
    client = OpenAI()
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            seed=3655,
        )
        return response.choices[0].message.content
    except Exception as e:
        return str(e)

class TestOpenAIModel(unittest.TestCase):
    def test_openai_model(self, mock_openai):
        # エラーケースをシミュレート
        # mock_openai.return_value.chat.completions.create.side_effect = Exception("API Error")

        # 関数を実行してエラーメッセージを確認
        result = _openai_model("gpt-4-turbo-2024-04-09", "Hello, world")
        print(result)

        # 正常なレスポンスをモック
        #mock_openai.return_value.chat.completions.create.return_value = type('obj', (object,), {'choices': [type('obj', (object,), {'message': type('obj', (object,), {'content': "Hello World"})})]})
        
        # 正常な動作を確認
        #result = _openai_model("text-davinci-003", "Hello")
        #self.assertEqual(result, "Hello World")

if __name__ == "__main__":
    unittest.main()
