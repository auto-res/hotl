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

class Validation_prompt:
    def __init__(self,llm_model,llm_name,api_key,mix_python_element,reference_python_code):
        self.llm_name = llm_name
        self.llm_model = llm_model
        self.mix_python_element = mix_python_element
        self.client = OpenAI(
            api_key = api_key,
        )
        self.model_answer = reference_python_code

    def exec(self):
        ret = self.llm_model(self.llm_name, self.mix_python_element)
        return ret
    
    def val(self):
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
The assistant's role is to compare the answer to a given question with the correct answer to determine if the answer is correct.
First, the assistant carefully analyzes the contents of the ANSWER tag to understand what the final answer is. Next, it compares it with the MODEL_ANSWER tag to determine if the final answer of the ANSWER tag is consistent with the MODEL_ANSWER tag, and then answers with the RESULT tag.
NOTES.
- The assistant must respond with the results of the decision using the RESULT tag.
- The answer must be selected from two options, "correct" and "incorrect".
</RULE>


<ANSWER>
{answer}
</ANSWER>

<MODEL_ANSWER>
{model_answer}
</MODEL_ANSWER>
"""
        func_method_decomposition = LLMFunction(
        template=template_method_composition, variables=['answer','model_answer'])
        ret = func_method_decomposition(answer=st.session_state.val_prompt, model_answer=self.model_answer)
        ret = self.llm_model(self.llm_name, ret)
        LP = LPML_paeser()
        result = LP.findall(LP.parse(ret), 'RESULT')[0]['content'][0]
        return result

