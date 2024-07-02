# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 16:57:10 2024

@author: Yz
"""


from openai import OpenAI
from src.creator.LPML_paeser import LPML_paeser
from src.creator.LPML_wrapper_gpt import ChatGPT
from src.creator.LPML_wrapper_function import LLMFunction
from src.creator.LPML_paeser import LPML_paeser

class Concretizer:
    def __init__(self,llm_model,llm_name,api_key,M_pseudo_code,python2_1,python2_2,think2,OBJECTIVE,PROMPTS_con,TAG_DEFINE_con,prompts_method):
        self.llm_name = llm_name
        self.llm_model = llm_model
        self.M_pseudo_code = M_pseudo_code
        self.python2_1 = python2_1
        self.python2_2 = python2_2
        self.client = OpenAI(
            api_key = api_key,
        )
        self.think2 = think2
        self.OBJECTIVE = OBJECTIVE
        self.PROMPTS_con = PROMPTS_con
        self.TAG_DEFINE_con = TAG_DEFINE_con
        self.prompts_method = prompts_method

    def exec(self):
        if self.prompts_method == 0:
            template_method_composition = '''
<RULE>
The system and the assistant exchange messages.
All messages MUST be formatted in XML format. XML element ::= <tag attribute="value">content</tag>
Tags determine the meaning and function of the content. The content must not contradict the definition of the tag.
</RULE>

{TAG_DEFINE_con}

{PROMPTS_con}

<OBJECTIVE>
{OBJECTIVE}
</OBJECTIVE>

<THINK>
{think2}
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
            

        if self.prompts_method == 1:
            template_method_composition = '''
<RULE>
The system and the assistant exchange messages.
All messages MUST be formatted in XML format. XML element ::= <tag attribute="value">content</tag>
Tags determine the meaning and function of the content. The content must not contradict the definition of the tag.
</RULE>

{TAG_DEFINE_con}

{PROMPTS_con}

<OBJECTIVE>
{OBJECTIVE}
</OBJECTIVE>

<THINK>
{think2}
</THINK>

<MIXED_PROMPT>
{M_pseudo_code}
</MIXED_PROMPT>

<ELEMENTAL_PROMPT>
{python2_1}
</ELEMENTAL_PROMPT>

<ELEMENTAL_PROMPT>
{python2_2}
</ELEMENTAL_PROMPT>

<EOS></EOS>
'''.strip()
            

        #llm = ChatGPT(temperature=0.7, top_p=0.5, max_tokens=2048, stop='<EOS', model='gpt-4-turbo-preview')
        #func_method_decomposition = LLMFunction(
        #    llm, template=template_method_composition, 
        #    variables=['TAG_DEFINE_con','PROMPTS_con','M_pseudo_code', 'python2_1','python2_2','think','OBJECTIVE'])
        func_method_decomposition = LLMFunction(
            template=template_method_composition, 
            variables=['TAG_DEFINE_con','PROMPTS_con','M_pseudo_code', 'python2_1','python2_2','think','OBJECTIVE'])
        ret = func_method_decomposition(TAG_DEFINE_con=self.TAG_DEFINE_con, PROMPTS_con=self.PROMPTS_con,
                                        M_pseudo_code=self.M_pseudo_code, python2_1=self.python2_1, 
                                        python2_2=self.python2_2,think2=self.think2,OBJECTIVE=self.OBJECTIVE)
        ret = self.llm_model(self.llm_name, ret)
        LP = LPML_paeser()
        if self.prompts_method == 0:
            mix_python = LP.deparse(LP.findall(LP.parse(ret), 'MIXED_METHOD'))
            mix_python_element = LP.deparse(LP.findall(LP.parse(ret), 'PYTHON'))
            think = LP.deparse(LP.findall(LP.parse(ret), 'THINK'))
        elif self.prompts_method == 1:
            mix_python = LP.deparse(LP.findall(LP.parse(ret), 'MIXED_PROMPT'))
            mix_python_element = LP.deparse(LP.findall(LP.parse(ret), 'PROMPTS'))
            think = LP.deparse(LP.findall(LP.parse(ret), 'THINK'))
            
        return mix_python,mix_python_element,think
    

