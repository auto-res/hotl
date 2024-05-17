import anthropic


def _anthropic_model(model_name, prompt):
    """
    Generate a response using the Anthropic model.

    Args:
        model_name (str): The name of the model to use.
        prompt (str): The prompt for generating the response.

    Returns:
        str: The generated response.
    """    
    client = anthropic.Anthropic()
    message = client.messages.create(
        model=model_name,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content
