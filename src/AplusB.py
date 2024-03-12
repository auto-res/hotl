# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 21:27:21 2024

@author: Yz
"""


from src.ABS import ABS
from src.concrete import CON
import re
from src.LPML_paeser import LPML_paeser
from src.LPML_wrapper_gpt import ChatGPT
from src.LPML_wrapper_function import LLMFunction


class AplusB:
    def __init__(self,api_key,GPT_id,M_pseudo_code,A_pseudo_code,M_name,A_name):
        self.GPT_id = GPT_id
        self.M_pseudo_code = M_pseudo_code
        self.A_pseudo_code = A_pseudo_code
        self.api_key = api_key
        self.M_name = M_name
        self.A_name = A_name

    def M2_code_gen(self):
        abs = ABS(self.api_key,self.GPT_id,self.M_pseudo_code,self.M_name)
        think1,python1_1,python1_2 = abs.abstraction()

        abs = ABS(self.api_key,self.GPT_id,self.A_pseudo_code,self.A_name)
        think2,python2_1,python2_2 = abs.abstraction()

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
The assistant's role is to create a completely new MIXED_METHOD that may improve performance from the existing MIXED_METHOD from four ELEMENTAL_METHODs decomposed from two MIXED_METHODs, by selecting the appropriate two from the ELEMENTAL_METHODs The first step is to select two appropriate ELEMENTAL_METHODs to create a new MIXED_METHOD.
The assistant should first carefully analyze the contents of ELEMENTAL_METHOD using the two THINK tags, and then use the SELECTED_ELEMENTAL_METHOD tag to make the selection.
NOTES.
    - Assistants must use the THINK tag before using the SELECTED_ELEMENTAL_METHOD tag.
　　- There are two THINK tags, "Classifying ELEMENTAL_METHODs" and "Selection Justification," and the "Classifying ELEMENTAL_METHODs" tag contains the contents of classifying ELEMENTAL_METHODs into basic and additional methods. The "Classifying ELEMENTAL_METHODs" section should include the classification of ELEMENTAL_METHODs into basic and additional methods, and the "Selection Justification" section should include the actual ELEMENTAL_METHOD tag name selected and why such a selection was made.
    - The assistant must select two SELECTED_ELEMENTAL_METHODs from the ELEMENTAL_METHODs.
　　- The contents of the SELECTED_ELEMENTAL_METHOD tag must be exactly the same as the selected ELEMENTAL_METHOD tag.
    - The method of selection depends on the viewpoint. Assistants must classify the ELEMENTAL_METHOD into basic and additional methods, and select one from each of the two types of methods classified.
    - Basic methods are generally well-known methods, for example, "past research" in the case of a paper.
　　- An additional method is, for example, a method that is the difference between the "past research" and the proposed method in the case of a paper.
</RULE>

<THINK>
{think1}
</THINK>

<ELEMENTAL_METHOD>
{python1_1}
</ELEMENTAL_METHOD>

<ELEMENTAL_METHOD>
{python1_2}
</ELEMENTAL_METHOD>

<THINK>
{think2}
</THINK>

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
            llm, template=template_method_decomposition, variables=['think1','python1_1','python1_2','think2','python2_1','python2_2'])
        ret = func_method_decomposition(think1=think1,python1_1=python1_1,python1_2=python1_2,think2=think2,python2_1=python2_1,python2_2=python2_2)
        
        LP = LPML_paeser()
        think = LP.deparse(LP.findall(LP.parse(ret), 'THINK')[1]['content'])
        python1 = LP.deparse([LP.findall(LP.parse(ret), 'ELEMENTAL_METHOD')[0]])
        python2 = LP.deparse([LP.findall(LP.parse(ret), 'ELEMENTAL_METHOD')[1]])

        con = CON(self.api_key,self.GPT_id,python1,python2,think)
        mix_python = con.concrete()
        return mix_python,think1,python1_1,python1_2,think2,python2_1,python2_2