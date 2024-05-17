# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 16:57:10 2024

@author: Yz
"""

from openai import OpenAI
from src.LPML_paeser import LPML_paeser
from src.LPML_wrapper_gpt import ChatGPT
from src.LPML_wrapper_function import LLMFunction


class PRO:
    def __init__(self, api_key, GPT_id, M_name, mix_python, reference_python):
        self.GPT_id = GPT_id
        self.reference_python = reference_python
        self.client = OpenAI(
            api_key=api_key,
        )
        self.M_name = M_name
        self.mix_python = mix_python

    def gen_program(self):
        template_method_decomposition = """
<RULE>
The system and the assistant exchange messages.
All messages MUST be formatted in XML format. XML element ::= <tag attribute="value">content</tag>
Tags determine the meaning and function of the content. The content must not contradict the definition of the tag.
</RULE>

<TAG name="RULE">
This tag defines rules. The defined content is absolute.
Attributes:
    - role (optional) : A role that should follow the rules. Roles are "system" or "assistant".
Notes:
    - The assistant must not use this tag.
</TAG>

<TAG name="TAG">
This tag defines a tag. The defined content is absolute.
Attributes:
    - name : A tag name.
Notes:
    - The assistant must not use this tag.
</TAG>

<TAG name="SYSTEM">
This tag represents a system message.
Notes:
    - The assistant MUST NOT use this tag.
</TAG>

<TAG name="EOS">
Indicates the end of a message.
</TAG>

<TAG name="THINK">
This tag represents a thought process.
If you use this tag, take a drop deep breath and work on the problem step-by-step.
Attributes:
    - label (optional) : A label summarizing the contents.
Notes:
    - The thought process must be described step by step.
    - Premises in reasoning must be made as explicit as possible. That is, there should be no leaps of reasoning.
</TAG>

<TAG name="PYTHON">
This tag represents an executable Python code.
Attributes:
    - label (optional) : A label summarizing the contents.
</TAG>

<TAG name="MIXED_METHOD">
This tag represents a mixed method created by combining several elemental methods.
The content of this tag consists of a textual description of the method and sample code.
Attributes:
    - name : The name of the method.
Notes:
    - This tag must contain one PYTHON tag inside.
</TAG>

<TAG name="ELEMENTAL_METHOD">
This tag represents an elemental methods.
The content of this tag consists of a textual description of the method and sample code.
Attributes:
    - name : The name of the method.
Notes:
    - This tag must contain one PYTHON tag inside.
</TAG>

<TAG name="REFERENCE_METHOD">
This tag represents a reference method.
The content of this tag consists of sample code for the method.
Attributes
    - name : Name of the method.
Notes.
    - One PYTHON tag must be included inside this tag.
</TAG>

<RULE role="assistant">
The Assistant is a friendly and helpful research assistant with expertise in various areas of machine learning.
The Assistant's role is to create verifiable and executable Python code using the created MIXED_METHOD.
The assistant will first find the {M_name} part in the contents of the REFERENCE_METHOD tag, then replace and incorporate the MIXED_METHOD as a custom function with the {M_name} part without changing the flow of the REFERENCE_METHOD, and create code using the PYTHON tag PYTHON tag.

Caution.
    - The assistant must parse the REFERENCE_METHOD tag before using the PYTHON tag.
　　- Since the REFERENCE_METHOD tag contains executable Python code, the {M_name} portion must be replaced with MIXED_METHOD using the contents of REFERENCE_METHOD.
    - The PYTHON tag must always contain executable code. For this purpose, the variable type, input/output format, number of arguments, etc., should be aborted when creating it.
</RULE>

<REFERENCE_METHOD>
{reference_python}
</REFERENCE_METHOD>

<MIXED_METHOD>
{mix_python}
</MIXED_METHOD>

<EOS></EOS>
""".strip()

        llm = ChatGPT(
            temperature=0.7,
            top_p=0.5,
            max_tokens=2048,
            stop="<EOS",
            model="gpt-4-turbo-preview",
        )
        func_method_decomposition = LLMFunction(
            llm,
            template=template_method_decomposition,
            variables=["M_name", "reference_python", "mix_python"],
        )
        ret = func_method_decomposition(
            M_name=self.M_name,
            reference_python=self.reference_python,
            mix_python=self.mix_python,
        )

        LP = LPML_paeser()
        return LP.deparse(LP.parse(ret)[1]["content"])
