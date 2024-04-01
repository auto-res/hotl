import textwrap

import jinja2


def make_prompt(prompt_template: str, **kwargs) -> str:
    template = jinja2.Template(prompt_template)
    prompt = template.render(**kwargs)
    return textwrap.dedent(prompt)
