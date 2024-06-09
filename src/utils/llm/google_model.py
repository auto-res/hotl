import google.generativeai as genai


def _google_model(model_name, prompt):
    """Generates content using a generative model.

    Args:
        model_name (str): The name of the generative model.
        prompt (str): The prompt for generating content.

    Returns:
        str: The generated content.
    """    
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

if __name__ == "__main__":
    text = _google_model("gemini-1.0-pro", "Hello,")
    print(text)
