# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 16:57:10 2024

@author: Yz
"""


from openai import OpenAI
from src.LPML_paeser import LPML_paeser
from src.LPML_wrapper_gpt import ChatGPT
from src.LPML_wrapper_function import LLMFunction
from src.LPML_paeser import LPML_paeser

class CON:
    def __init__(self,api_key,GPT_id,M_pseudo_code,python2_1,python2_2,think2):
        self.GPT_id = GPT_id
        self.M_pseudo_code = M_pseudo_code
        self.python2_1 = python2_1
        self.python2_2 = python2_2
        self.client = OpenAI(
            api_key = api_key,
        )
        self.think = think2

    def concrete(self):
        template_method_composition = '''
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
The assistant's role is to select one of the two given ELEMENTAL_METHODs and replace an element in the MIXED_METHOD to create a more efficient MIXED_METHOD.
First, the assistant carefully analyzes the contents of the two ELEMENTAL_METHODs using the THINK tag to understand which one will contribute to the improvement of the MIXED_METHOD's performance. Then, using the MIXED_METHOD tag, the assistant explains how the selected ELEMENTAL_METHOD and the original MIXED_METHOD were combined.
Notes.
- The assistant must use the THINK tag before using the MIXED_METHOD tag.
  - The THINK tag must detail and specify how it was combined and how improvements are expected as a description of the MIXED_METHOD.
  - There are many ways to combine, but the assistant must perform the combination that seems most natural and reasonable.
</RULE>

<THINK>
{think}
</THINK>

<MIXED_METHOD>
{M_pseudo_code}
</MIXED_METHOD>

<ELEMENTAL_METHOD>
{python2_1}
</ELEMENTAL_METHOD>

<ELEMENTAL_METHOD>
{python2_2}
</ELEMENTAL_METHOD>

<EOS></EOS>
'''.strip()
        llm = ChatGPT(temperature=0.7, top_p=0.5, max_tokens=2048, stop='<EOS', model='gpt-4-turbo-preview')
        func_method_decomposition = LLMFunction(
            llm, template=template_method_composition, variables=['M_pseudo_code', 'python2_1','python2_2','think'])
        ret = func_method_decomposition(M_pseudo_code=self.M_pseudo_code, python2_1=self.python2_1, python2_2=self.python2_2,think=self.think)
        
        LP = LPML_paeser()
        mix_python = LP.deparse(LP.findall(LP.parse(ret), 'MIXED_METHOD'))
        think = LP.deparse(LP.findall(LP.parse(ret), 'THINK'))
        return mix_python,think
    

