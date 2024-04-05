import google.generativeai as genai


def _googel_model(model_name, prompt):
    model = genai.GenerativeModel(
        model_name,
        generation_config=dict(
            # temperature=temperature,
            # top_p=None,
            # candidate_count=None,
            # stop_sequences=None,
            # max_output_tokens=None,
            # top_k=None,
        ),
    )
    response = model.generate_content(prompt)

    return response.text
