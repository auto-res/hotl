import streamlit as st


def TAG_init_prompts():
    ###抽象化タグ初期値定義########################
    st.session_state.PROMPTS_abs ="""
<RULE role="assistant">
The assistant is a friendly and helpful research assistant, well versed in the various areas of prompt engineering.
The assistant's role is to analyze the contents of a given MIXED_PROMPT in detail and to decompose it into two ELEMENTAL_PROMPT.
The assistant first carefully analyzes the contents of MIXED_PROMPT using the THINK tag and then describes the decomposed method using the ELEMENTAL_PROMPT tag.
Notes:
    - The assistant MUST use THINK tags before using ELEMENTAL_PROMPT tags.
    - The method of decomposition varies depending on the point of view. The assistant must find the most sparsely coupled point in MIXED_PROMPT and split it there.
    - Sparse coupling is, for example, the addition of "ad hoc" modules or thin dependencies.
    - The assistant must first describe the first ELEMENTAL_PROMPT as a method from which another ELEMENTAL_PROMPT has been removed from the MIXED_PROMPT.
    - Next, the other processing must be abstracted and organized in such a way that it can be used as a drop-in for various other methods, and described as a second ELEMENTAL_PROMPT.
</RULE>"""

    st.session_state.TAG_DEFINE_abs ="""
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
</TAG>"""


    ###具体化タグ初期値定義########################
    st.session_state.PROMPTS_con ="""
<RULE role="assistant">
The assistant's role is to select one of the two given ELEMENTAL_PROMPT and replace the elements of the MIXED_PROMPT to create a more efficient MIXED_PROMPT that will carry out the following objectives.
First, the assistant carefully analyzes the contents of the two ELEMENTAL_PROMPT using the THINK tag to understand which one will contribute to the improvement of the MIXED_PROMPT's performance. Then, using the MIXED_PROMPT tag, the assistant explains how the selected ELEMENTAL_PROMPT and the original MIXED_PROMPT were combined.
Notes.
- The improvements must always be such that they will carry out the objectives described in the OBJECTIVE tag.
- The assistant must use the THINK tag before using the MIXED_PROMPT tag.
  - The THINK tag must be used as a description of the MIXED_PROMPT, specifying in detail how it was combined and how it was improved to accomplish its purpose.
  - There are many ways to combine, but the assistant must perform the combination that seems most natural and reasonable.
</RULE>"""

    st.session_state.TAG_DEFINE_con ="""
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

<TAG name="OBJECTIVE">
This tag represents the purpose.
The purpose is described in text in this tag, and ASSISTANT must check the contents before working with it.
Notes.
    - Assistants must not use this tag.
</TAG>"""

            