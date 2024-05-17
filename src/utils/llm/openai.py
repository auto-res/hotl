from openai import OpenAI


def _openai_model(model_name, prompt):
    """
    Generate a completion using the OpenAI chat model.

    Args:
        model_name (str): The name of the OpenAI model to use.
        prompt (str): The user's prompt for generating the completion.

    Returns:
        str: The generated completion response.

    """
    client = OpenAI()
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        seed=3655,
    )

    return response.choices[0].message.content
