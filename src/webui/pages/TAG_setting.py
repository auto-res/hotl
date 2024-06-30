import streamlit as st
from src.creator.yoshinosan.TAG_src import TAG_init

st.markdown('# LPML TAG Setting page')

TAG_init()
tab_tag1, tab_tag2 = st.tabs(["抽象化", "具体化"])
with tab_tag1:
    st.markdown('## LPMLプロンプト')
    st.session_state.PROMPTS_abs = st.text_area(
    'PROMPTS_abs', value = st.session_state.PROMPTS_abs, height=1000, max_chars=10000
    )
    st.markdown('## LPMLタグ定義')
    st.session_state.TAG_DEFINE_abs = st.text_area(
    'TAG_DEFINE_abs', value = st.session_state.TAG_DEFINE_abs, height=1000, max_chars=10000
    )

with tab_tag2:
    st.markdown('## LPMLプロンプト')
    st.session_state.PROMPTS_con = st.text_area(
    'PROMPTS_con', value = st.session_state.PROMPTS_con, height=1000, max_chars=10000
    )

    st.markdown('## LPMLタグ定義')
    st.session_state.TAG_DEFINE_con = st.text_area(
    'TAG_DEFINE_con', value = st.session_state.TAG_DEFINE_con, height=1000, max_chars=10000
    )
