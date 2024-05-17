import streamlit as st
import pandas as pd
import numpy as np


st.markdown('# AutoRes')
st.markdown('## 機械学習研究の自律的な実行')

st.sidebar.title('関連リンク')
with st.sidebar:
    st.markdown('* [プロジェクトページ](https://sites.google.com/view/automated-research/home?authuser=0)')
    st.markdown('* [GitHub](https://github.com/auto-res/Mockup_python)')


tab1, tab2, tab3 = st.tabs(["Creator", "Coder", "Evaluator"])


with tab1:
    st.markdown('## Creator')
    st.markdown('新規手法の作成')
    st.markdown('こちらに吉野さんの実行画面を作成していただきたいです！')



with tab2:
    st.markdown('## Coder')
    st.markdown('実験用コードの作成')
    
    
    
with tab3:
    st.markdown('## Evaluator')
    st.markdown('新規手法の評価')
