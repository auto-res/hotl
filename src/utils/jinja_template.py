import textwrap

import jinja2


import jinja2
import textwrap

def make_prompt(prompt_template: str, **kwargs) -> str:
    """
    Generate a prompt by rendering a Jinja template.

    Args:
        prompt_template (str): The Jinja template string for the prompt.

    Returns:
        str: The rendered prompt string.
    """
    template = jinja2.Template(prompt_template)
    prompt = template.render(**kwargs)
    return textwrap.dedent(prompt)
