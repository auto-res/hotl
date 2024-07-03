# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 16:57:10 2024

@author: Yz
"""


from openai import OpenAI
import streamlit as st
from src.creator.LPML_paeser import LPML_paeser
from src.creator.LPML_wrapper_gpt import ChatGPT
from src.creator.LPML_wrapper_function import LLMFunction
from src.creator.LPML_paeser import LPML_paeser

class Correction_prompt:
    def __init__(self,llm_model,llm_name,api_key,PROMPTS_abs,PROMPTS_con,mix_python_element):
        self.llm_name = llm_name
        self.llm_model = llm_model
        self.PROMPTS_abs = PROMPTS_abs
        self.client = OpenAI(
            api_key = api_key,
        )
        self.PROMPTS_con = PROMPTS_con
        self.mix_python_element = mix_python_element


    def exec(self):
        template_method_composition = """
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
Must be answered in Japanese.
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

<TAG name="PROMPTS">
This tag represents an executable LLM prompt.
This tag does not contain any descriptive text or other information other than the prompt.
Attributes
    - label (optional): A label summarizing the content.
</TAG>

<TAG name="MIXED_PROMPT">
This tag represents a mixed method created by combining several elemental methods.
The content of this tag consists of a textual description of the method and sample prompts.
Attributes:
    - name : The name of the method.
Notes:
    - This tag must contain one PROMPTS tag inside.
</TAG>

<TAG name="ELEMENTAL_PROMPT">
This tag represents an elemental methods.
The content of this tag consists of a textual description of the method and sample prompts.
Attributes:
    - name : The name of the method.
Notes:
    - This tag must contain one PROMPTS tag inside.
</TAG>

<TAG name="ANSWER">
This tag represents an answer to a question.
This tag does not contain anything other than the answer to the question, and may contain information such as how the question was solved.
Attributes
    - label (optional): A label summarizing the content.
</TAG>

<TAG name="MODEL_ANSWER">
This tag contains the correct answer to the question.
This tag contains no content other than the result of the correct answer to the question.
Attributes
    - label (optional): A label summarizing the content.
</TAG>

<RULE role="assistant">
The assistant's role is to modify the two given <RULE role="assistant"> and create a <RULE role="assistant"> that yields the proper result.
We know that the existing PROMPT tag yields incorrect results. However, the specific results are confidential.
This PROMPT tag is an automatically generated prompt from two <RULE role="assistant">.
The first <RULE role="assistant"> is a prompt to find the most loosely coupled points from one known method and decompose it into two methods.
The second prompt, <RULE role="assistant">, is a prompt to find the most natural and reasonable combination of the method obtained with the first <RULE role="assistant"> and the method obtained with the other method to obtain a single combined method (PROMPT tag). PROMPT.
Therefore, the assistant must first carefully analyze the contents of the <RULE role="assistant"> to understand what went wrong with the <RULE role="assistant"> prompt and why it resulted in a PROMPT tag that yielded incorrect results. Then, consider what modifications should be made to the existing PROMPT tag and respond with a THINK tag. Next, based on the Nei use you have considered, modify the two <RULE role="assistant"> and respond with <RULE role="assistant">.
Attention.
- The assistant must create three results, one THINK tag and two <RULE role="assistant">.
- The first <RULE role="assistant"> must contain a modified prompt that breaks down into two methods.
- The second <RULE role="assistant"> must contain a prompt that modifies the prompt to obtain a PROMPT tag from the two methods.
- The <RULE role="assistant"> to be created must not directly contain the contents of the PROMPT tag.
- When modifying two <RULE role="assistant">, please refer to the information in the existing <RULE role="assistant">.
- It should be kept in mind that the existing PROMPT tag is a prompt generated from the prompts of the two <RULE role="assistant">s.
</RULE>

<PROMPTS>
{mix_python_element}
</PROMPTS>

{prompts_abs}

{prompts_con}
"""
        func_method_decomposition = LLMFunction(
        template=template_method_composition, variables=['mix_python_element','prompts_abs','prompts_con'])
        ret = func_method_decomposition(mix_python_element=self.mix_python_element,prompts_abs=self.PROMPTS_abs, prompts_con=self.PROMPTS_con)
        ret = self.llm_model(self.llm_name, ret)
        #LP = LPML_paeser()
        #result = LP.findall(LP.parse(ret), 'RESULT')[0]['content'][0]
        return ret

