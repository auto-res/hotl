# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 16:57:10 2024

@author: Yz
"""


from openai import OpenAI
from src.creator.yoshinosan.LPML_paeser import LPML_paeser
from src.creator.yoshinosan.LPML_wrapper_gpt import ChatGPT
from src.creator.yoshinosan.LPML_wrapper_function import LLMFunction


class Abstractor:
    def __init__(self,api_key,GPT_id,M_pseudo_code,method_name,PROMPTS_abs,TAG_DEFINE_abs,prompts_method):
        self.GPT_id = GPT_id
        self.M_pseudo_code = M_pseudo_code
        self.client = OpenAI(
            api_key = api_key,
        )
        self.method_name = method_name
        self.PROMPTS_abs = PROMPTS_abs
        self.TAG_DEFINE_abs = TAG_DEFINE_abs
        self.prompts_method = prompts_method

    def exec(self):
        if self.prompts_method == 0:
            template_method_decomposition = '''
<RULE>
The system and the assistant exchange messages.
All messages MUST be formatted in XML format. XML element ::= <tag attribute="value">content</tag>
Tags determine the meaning and function of the content. The content must not contradict the definition of the tag.
</RULE>

{TAG_DEFINE_abs}

{PROMPTS_abs}

<MIXED_METHOD>
{mixed_method}
</MIXED_METHOD>

<EOS></EOS>
'''.strip()
            
        elif self.prompts_method == 1:
            template_method_decomposition = '''
<RULE>
The system and the assistant exchange messages.
All messages MUST be formatted in XML format. XML element ::= <tag attribute="value">content</tag>
Tags determine the meaning and function of the content. The content must not contradict the definition of the tag.
</RULE>

{TAG_DEFINE_abs}

{PROMPTS_abs}

<MIXED_PROMPT>
{mixed_method}
</MIXED_PROMPT>

<EOS></EOS>
'''.strip()

        llm = ChatGPT(temperature=0.7, top_p=0.5, max_tokens=2048, stop='<EOS', model='gpt-4-turbo-preview')
        func_method_decomposition = LLMFunction(
            llm, template=template_method_decomposition, variables=['TAG_DEFINE_abs','PROMPTS_abs','mixed_method'])

        if self.prompts_method == 0:
            mixed_method = f'''
{self.method_name}
<PYTHON>
{self.M_pseudo_code}
</PYTHON>
'''.strip()
        elif self.prompts_method == 1:
            mixed_method = f'''
{self.method_name}
<PROMPTS>
{self.M_pseudo_code}
</PROMPTS>
'''.strip()

        ret = func_method_decomposition(TAG_DEFINE_abs=self.TAG_DEFINE_abs, PROMPTS_abs=self.PROMPTS_abs, mixed_method=mixed_method)
        LP = LPML_paeser()
        think = LP.deparse(LP.findall(LP.parse(ret), 'THINK')[0]['content'])
        if self.prompts_method == 0:
            python1 = LP.deparse([LP.findall(LP.parse(ret), 'ELEMENTAL_METHOD')[0]])
            python2 = LP.deparse([LP.findall(LP.parse(ret), 'ELEMENTAL_METHOD')[1]])
        elif self.prompts_method == 1:
            python1 = LP.deparse([LP.findall(LP.parse(ret), 'ELEMENTAL_PROMPT')[0]])
            python2 = LP.deparse([LP.findall(LP.parse(ret), 'ELEMENTAL_PROMPT')[1]])
            
        return think,python1,python2
    

