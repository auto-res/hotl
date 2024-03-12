# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 16:57:10 2024

@author: Yz
"""


from openai import OpenAI
from src.LPML_paeser import LPML_paeser
from src.LPML_wrapper_gpt import ChatGPT
from src.LPML_wrapper_function import LLMFunction


class ABS:
    def __init__(self,api_key,GPT_id,M_pseudo_code,method_name):
        self.GPT_id = GPT_id
        self.M_pseudo_code = M_pseudo_code
        self.client = OpenAI(
            api_key = api_key,
        )
        self.method_name = method_name

    def abstraction(self):
        template_method_decomposition = '''
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

<RULE role="assistant">
The assistant is a friendly and helpful research assistant, well versed in the various areas of machine learning.
The assistant's role is to analyze the contents of a given MIXED_METHOD in detail and to decompose it into two ELEMENTAL_METHOD.
The assistant first carefully analyzes the contents of MIXED_METHOD using the THINK tag and then describes the decomposed method using the ELEMENTAL_METHOD tag.
Notes:
    - The assistant MUST use THINK tags before using ELEMENTAL_METHOD tags.
    - The method of decomposition varies depending on the point of view. The assistant must find the most sparsely coupled point in MIXED_METHOD and split it there.
    - Sparse coupling is, for example, the addition of "ad hoc" modules or thin dependencies.
    - The assistant must first describe the first ELEMENTAL_METHOD as a method from which another ELEMENTAL_METHOD has been removed from the MIXED_METHOD.
    - Next, the other processing must be abstracted and organized in such a way that it can be used as a drop-in for various other methods, and described as a second ELEMENTAL_METHOD.
</RULE>

<MIXED_METHOD>
{mixed_method}
</MIXED_METHOD>

<EOS></EOS>
'''.strip()

        llm = ChatGPT(temperature=0.7, top_p=0.5, max_tokens=2048, stop='<EOS', model='gpt-4-turbo-preview')
        func_method_decomposition = LLMFunction(
            llm, template=template_method_decomposition, variables=['mixed_method'])

        mixed_method = f'''
{self.method_name}
<PYTHON>
{self.M_pseudo_code}
</PYTHON>
'''.strip()

        ret = func_method_decomposition(mixed_method=mixed_method)
        LP = LPML_paeser()
        think = LP.deparse(LP.findall(LP.parse(ret), 'THINK')[0]['content'])
        python1 = LP.deparse([LP.findall(LP.parse(ret), 'ELEMENTAL_METHOD')[0]])
        python2 = LP.deparse([LP.findall(LP.parse(ret), 'ELEMENTAL_METHOD')[1]])

        return(think,python1,python2)
    

