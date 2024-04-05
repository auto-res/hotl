from openai import OpenAI


def _openai_model(model_name, prompt):
    client = OpenAI()
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        seed=3655,
    )

    return response.choices[0].message.content
