import streamlit as st


def VALUE_init_prompts():
    ###値の初期値########################
    st.session_state.txt_OBJECTIVE_value ="""The objective is to generate prompts that will solve the problem more accurately."""
    st.session_state.txt_M_pre_name_value ="""CoT"""

    st.session_state.txt_M_pre_code_value ="""Find the remainder when the sum \\[75+76+77+78+79+80+81+82\\]is divided by 16. Let's think step by step."""

    st.session_state.txt_M_patch_name_value ="""Few-Shot Prompting"""

    st.session_state.txt_M_patch_code_value ="""The remainder of the sum \\[1+2+3+4+4+5+6+7+8\\] divided by 2 can be solved as follows
1+2+3+4+4+5+6+7+8=36
36/2=18
The answer is 18.
At this time, find the remainder when the sum \[10+11+72+7+71+44+11+22\]is divided by 16."""

    st.session_state.reference_python_code_value ="""a"""