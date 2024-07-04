# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 16:57:10 2024

@author: Yz
"""


from openai import OpenAI
import streamlit as st
from src.creator.yoshinosan.LPML_paeser import LPML_paeser
from src.creator.yoshinosan.LPML_wrapper_gpt import ChatGPT
from src.creator.yoshinosan.LPML_wrapper_function import LLMFunction
from src.creator.yoshinosan.LPML_paeser import LPML_paeser

class Improvement_prompt:
    def __init__(self,llm_model,llm_name,api_key,PROMPTS_abs,PROMPTS_con,val_prompt):
        self.llm_name = llm_name
        self.llm_model = llm_model
        self.PROMPTS_abs = PROMPTS_abs
        self.PROMPTS_con = PROMPTS_con
        self.client = OpenAI(
            api_key = api_key,
        )
        self.val_prompt = val_prompt
    
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

<TAG name="RESULT">
This tag indicates that a decision has been made.
This tag must not contain any response other than "correct" or "incorrect".
Attributes
    - label (optional): A label summarizing the content.
</TAG>
        
<RULE role="assistant">
The assistant's role is to modify the prompts to perform the given task.
First, the assistant should understand that there are two prompts to modify.
The first prompt is to decompose an existing method into two methods.
The second prompt is to select one of the two given methods and replace elements of the existing method to create an efficient method.
These two prompts are used to create another prompt A to perform the task. However, prompt A is a secret prompt to the assistant.
First, the assistant carefully analyzes why the results of the task solved using prompt A in the ANSWER tag went wrong. Next, it carefully analyzes the contents of the existing PROMPTS tag that created prompt A. It then takes a deep breath and calmly considers and understands step by step why it created prompt A, which could not complete the task with these two prompts. The results of your understanding should be output using the THINK tag.
Next, modify the contents of the two PROMPTS tags using the results of your discussion. When modifying the tags, use the existing PROMPTS tags as a basis for the modifications.
Caution
- Assistants must respond with three deliverables: one THINK tag and two PROMPTS tags.
- First, the assistant must respond to the results of the discussion using the THINK tag.
- The modified prompt must be answered using the PROMPTS tag, first a prompt to decompose the existing method into two methods, followed by a prompt to select one of the two given methods and replace elements of the existing method to create an efficient method.
- Do not include any tags other than the THINK and PROMPTS tags.
</RULE>

<ANSWER>
{answer}
</ANSWER>

<PROMPTS>
{prompts_abs}
</PROMPTS>

<PROMPTS>
{prompts_con}
</PROMPTS>
"""
        func_method_decomposition = LLMFunction(
        template=template_method_composition, variables=['answer','prompts_abs','prompts_con'])
        ret = func_method_decomposition(answer=self.val_prompt,prompts_abs=self.PROMPTS_abs,prompts_con=self.PROMPTS_con)
        ret = self.llm_model(self.llm_name, ret)
        LP = LPML_paeser()

        think = LP.deparse(LP.findall(LP.parse(ret), 'THINK'))
        prompts_abs = LP.deparse([LP.findall(LP.parse(ret), 'PROMPTS')[0]])
        prompts_con = LP.deparse([LP.findall(LP.parse(ret), 'PROMPTS')[1]])
        return think,prompts_abs,prompts_con

