import streamlit as st


def TAG_init():
    ###抽象化タグ初期値定義########################
    if "RULE_abs" not in st.session_state:
        st.session_state.RULE_abs ="""<RULE>
The system and the assistant exchange messages.
All messages MUST be formatted in XML format. XML element ::= <tag attribute="value">content</tag>
Tags determine the meaning and function of the content. The content must not contradict the definition of the tag.
</RULE>"""

    if "TAG_assistant_abs" not in st.session_state:
        st.session_state.TAG_assistant_abs ="""<RULE role="assistant">
The assistant is a friendly and helpful research assistant, well versed in the various areas of machine learning.
The assistant's role is to analyze the contents of a given MIXED_METHOD in detail and to decompose it into two ELEMENTAL_METHOD.
The assistant first carefully analyzes the contents of MIXED_METHOD using the THINK tag and then describes the decomposed method using the ELEMENTAL_METHOD tag.
Notes:
    - The assistant MUST use THINK tags before using ELEMENTAL_METHOD tags.
    - The method of decomposition varies depending on the point of view. The assistant must find the most sparsely coupled point in MIXED_METHOD and split it there.
    - Sparse coupling is, for example, the addition of "ad hoc" modules or thin dependencies.
    - The assistant must first describe the first ELEMENTAL_METHOD as a method from which another ELEMENTAL_METHOD has been removed from the MIXED_METHOD.
    - Next, the other processing must be abstracted and organized in such a way that it can be used as a drop-in for various other methods, and described as a second ELEMENTAL_METHOD.
</RULE>"""

    if "TAG_RULE_abs" not in st.session_state:
        st.session_state.TAG_RULE_abs ="""<TAG name="RULE">
This tag defines rules. The defined content is absolute.
Attributes:
    - role (optional) : A role that should follow the rules. Roles are "system" or "assistant".
Notes:
    - The assistant must not use this tag.
</TAG>"""

    if "TAG_TAG_abs" not in st.session_state:
        st.session_state.TAG_TAG_abs ="""<TAG name="TAG">
This tag defines a tag. The defined content is absolute.
Attributes:
    - name : A tag name.
Notes:
    - The assistant must not use this tag.
</TAG>"""

    if "TAG_SYSTEM_abs" not in st.session_state:
        st.session_state.TAG_SYSTEM_abs ="""<TAG name="SYSTEM">
This tag represents a system message.
Notes:
    - The assistant MUST NOT use this tag.
</TAG>"""

    if "TAG_EOS_abs" not in st.session_state:
        st.session_state.TAG_EOS_abs ="""<TAG name="EOS">
Indicates the end of a message.
</TAG>"""

    if "TAG_THINK_abs" not in st.session_state:
        st.session_state.TAG_THINK_abs ="""<TAG name="THINK">
This tag represents a thought process.
If you use this tag, take a drop deep breath and work on the problem step-by-step.
Must be answered in Japanese.
Attributes:
    - label (optional) : A label summarizing the contents.
Notes:
    - The thought process must be described step by step.
    - Premises in reasoning must be made as explicit as possible. That is, there should be no leaps of reasoning.
</TAG>"""

    if "TAG_PYTHON_abs" not in st.session_state:
        st.session_state.TAG_PYTHON_abs ="""<TAG name="PYTHON">
This tag represents an executable Python code.
Attributes:
    - label (optional) : A label summarizing the contents.
</TAG>"""

    if "TAG_MIXED_METHOD_abs" not in st.session_state:
        st.session_state.TAG_MIXED_METHOD_abs ="""<TAG name="MIXED_METHOD">
This tag represents a mixed method created by combining several elemental methods.
The content of this tag consists of a textual description of the method and sample code.
Attributes:
    - name : The name of the method.
Notes:
    - Only one PYTHON tag must be placed within this tag.
</TAG>"""

    if "TAG_ELEMENTAL_METHOD_abs" not in st.session_state:
        st.session_state.TAG_ELEMENTAL_METHOD_abs ="""<TAG name="ELEMENTAL_METHOD">
This tag represents an elemental methods.
The content of this tag consists of a textual description of the method and sample code.
Attributes:
    - name : The name of the method.
Notes:
    - This tag must contain one PYTHON tag inside.
</TAG>"""


    ###具体化タグ初期値定義########################
    if "RULE_con" not in st.session_state:
        st.session_state.RULE_con ="""<RULE>
The system and the assistant exchange messages.
All messages MUST be formatted in XML format. XML element ::= <tag attribute="value">content</tag>
Tags determine the meaning and function of the content. The content must not contradict the definition of the tag.
</RULE>"""

    if "TAG_assistant_con" not in st.session_state:
        st.session_state.TAG_assistant_con ="""<RULE role="assistant">
The assistant's role is to select one of the two given ELEMENTAL_METHODs and replace an element in the MIXED_METHOD to create a more efficient MIXED_METHOD.
First, the assistant carefully analyzes the contents of the two ELEMENTAL_METHODs using the THINK tag to understand which one will contribute to the improvement of the MIXED_METHOD's performance. Then, using the MIXED_METHOD tag, the assistant explains how the selected ELEMENTAL_METHOD and the original MIXED_METHOD were combined.
Notes.
- The assistant must use the THINK tag before using the MIXED_METHOD tag.
- The THINK tag must detail and specify how it was combined and how improvements are expected as a description of the MIXED_METHOD.
- There are many ways to combine, but the assistant must perform the combination that seems most natural and reasonable.
</RULE>"""

    if "TAG_RULE_con" not in st.session_state:
        st.session_state.TAG_RULE_con ="""<TAG name="RULE">
This tag defines rules. The defined content is absolute.
Attributes:
    - role (optional) : A role that should follow the rules. Roles are "system" or "assistant".
Notes:
    - The assistant must not use this tag.
</TAG>"""

    if "TAG_TAG_con" not in st.session_state:
        st.session_state.TAG_TAG_con ="""<TAG name="TAG">
This tag defines a tag. The defined content is absolute.
Attributes:
    - name : A tag name.
Notes:
    - The assistant must not use this tag.
</TAG>"""

    if "TAG_SYSTEM_con" not in st.session_state:
        st.session_state.TAG_SYSTEM_con ="""<TAG name="SYSTEM">
This tag represents a system message.
Notes:
    - The assistant MUST NOT use this tag.
</TAG>"""

    if "TAG_EOS_con" not in st.session_state:
        st.session_state.TAG_EOS_con ="""<TAG name="EOS">
Indicates the end of a message.
</TAG>"""

    if "TAG_THINK_con" not in st.session_state:
        st.session_state.TAG_THINK_con ="""<TAG name="THINK">
This tag represents a thought process.
If you use this tag, take a drop deep breath and work on the problem step-by-step.
Must be answered in Japanese.
Attributes:
    - label (optional) : A label summarizing the contents.
Notes:
    - The thought process must be described step by step.
    - Premises in reasoning must be made as explicit as possible. That is, there should be no leaps of reasoning.
</TAG>"""

    if "TAG_PYTHON_con" not in st.session_state:
        st.session_state.TAG_PYTHON_con ="""<TAG name="PYTHON">
This tag represents an executable Python code.
Attributes:
    - label (optional) : A label summarizing the contents.
</TAG>"""

    if "TAG_MIXED_METHOD_con" not in st.session_state:
        st.session_state.TAG_MIXED_METHOD_con ="""<TAG name="MIXED_METHOD">
This tag represents a mixed method created by combining several elemental methods.
The content of this tag consists of a textual description of the method and sample code.
Attributes:
    - name : The name of the method.
Notes:
    - Only one PYTHON tag must be placed within this tag.
</TAG>"""

    if "TAG_ELEMENTAL_METHOD_con" not in st.session_state:
        st.session_state.TAG_ELEMENTAL_METHOD_con ="""<TAG name="ELEMENTAL_METHOD">
This tag represents an elemental methods.
The content of this tag consists of a textual description of the method and sample code.
Attributes:
    - name : The name of the method.
Notes:
    - This tag must contain one PYTHON tag inside.
</TAG>"""
        
    if "TAG_OBJECTIVE_con" not in st.session_state:
        st.session_state.TAG_OBJECTIVE_con ="""<TAG name="OBJECTIVE">
This tag represents the purpose.
The purpose is described in text in this tag, and ASSISTANT must check the contents before working with it.
Notes.
    - Assistants must not use this tag.
</TAG>"""

            