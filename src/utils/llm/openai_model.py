from openai import OpenAI
#import unittest
#from unittest.mock import patch

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


if __name__ == "__main__":
    text = _openai_model("gpt-4o-2024-05-13", "Hello,")
    print(text)
