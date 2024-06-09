import streamlit as st

st.markdown('# LPML TAG Setting page')

tab_tag1, tab_tag2 = st.tabs(["抽象化", "具体化"])


with tab_tag1:
    st.markdown('## LPMLプロンプト')
    st.session_state.RULE_abs = st.text_area(
    'RULE_abs', value = st.session_state.RULE_abs, height=150, max_chars=10000
    )
    st.session_state.TAG_assistant_abs = st.text_area(
    'TAG_assistant_abs', value = st.session_state.TAG_assistant_abs, height=150, max_chars=10000
    )

    st.markdown('## LPMLタグ定義')
    st.session_state.TAG_RULE_abs = st.text_area(
    'TAG_RULE_abs', value = st.session_state.TAG_RULE_abs, height=150, max_chars=10000
    )
    st.session_state.TAG_TAG_abs = st.text_area(
    'TAG_TAG_abs', value = st.session_state.TAG_TAG_abs, height=150, max_chars=10000
    )
    st.session_state.TAG_SYSTEM_abs = st.text_area(
    'TAG_SYSTEM_abs', value = st.session_state.TAG_SYSTEM_abs, height=150, max_chars=10000
    )
    st.session_state.TAG_EOS_abs = st.text_area(
    'TAG_EOS_abs', value = st.session_state.TAG_EOS_abs, height=150, max_chars=10000
    )
    st.session_state.TAG_THINK_abs = st.text_area(
    'TAG_THINK_abs', value =st.session_state.TAG_THINK_abs , height=150, max_chars=10000
    )
    st.session_state.TAG_PYTHON_abs = st.text_area(
    'TAG_PYTHON_abs', value = st.session_state.TAG_PYTHON_abs, height=150, max_chars=10000
    )
    st.session_state.TAG_MIXED_METHOD_abs = st.text_area(
    'TAG_MIXED_METHOD_abs', value = st.session_state.TAG_MIXED_METHOD_abs, height=150, max_chars=10000
    )
    st.session_state.TAG_ELEMENTAL_METHOD_abs = st.text_area(
    'TAG_ELEMENTAL_METHOD_abs', value = st.session_state.TAG_ELEMENTAL_METHOD_abs, height=150, max_chars=10000
    )

with tab_tag2:
    st.markdown('## LPMLプロンプト')
    st.session_state.RULE_con = st.text_area(
    'RULE_con', value = st.session_state.RULE_con, height=150, max_chars=10000
    )
    st.session_state.TAG_assistant_con = st.text_area(
    'TAG_assistant_con', value = st.session_state.TAG_assistant_con, height=150, max_chars=10000
    )

    st.markdown('## LPMLタグ定義')
    st.session_state.TAG_RULE_con = st.text_area(
    'TAG_RULE_con', value = st.session_state.TAG_RULE_con, height=150, max_chars=10000
    )
    st.session_state.TAG_TAG_con = st.text_area(
    'TAG_TAG_con', value = st.session_state.TAG_TAG_con, height=150, max_chars=10000
    )
    st.session_state.TAG_SYSTEM_con = st.text_area(
    'TAG_SYSTEM_con', value = st.session_state.TAG_SYSTEM_con, height=150, max_chars=10000
    )
    st.session_state.TAG_EOS_con = st.text_area(
    'TAG_EOS_con', value = st.session_state.TAG_EOS_con, height=150, max_chars=10000
    )
    st.session_state.TAG_THINK_con = st.text_area(
    'TAG_THINK_con', value =st.session_state.TAG_THINK_con , height=150, max_chars=10000
    )
    st.session_state.TAG_PYTHON_con = st.text_area(
    'TAG_PYTHON_con', value = st.session_state.TAG_PYTHON_con, height=150, max_chars=10000
    )
    st.session_state.TAG_MIXED_METHOD_con = st.text_area(
    'TAG_MIXED_METHOD_con', value = st.session_state.TAG_MIXED_METHOD_con, height=150, max_chars=10000
    )
    st.session_state.TAG_ELEMENTAL_METHOD_con = st.text_area(
    'TAG_ELEMENTAL_METHOD_con', value = st.session_state.TAG_ELEMENTAL_METHOD_con, height=150, max_chars=10000
    )
    st.session_state.TAG_OBJECTIVE_con = st.text_area(
    'TAG_OBJECTIVE_con', value = st.session_state.TAG_OBJECTIVE_con, height=150, max_chars=10000
    )

    













