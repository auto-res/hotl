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
    txt_OBJECTIVE = st.text_input('目的', placeholder='ここにどのように改善してほしいのか目的を記入', max_chars=1000)

    st.markdown('1. 初期値の入力')
    tab1_1, tab1_2, tab1_3 = st.tabs(["M_pre初期値", "M_post初期値", "その他初期値"])
    with tab1_1:
        txt_M_pre_name = st.text_input('M_preの名前', placeholder='ここにM_preの手法名を記入', max_chars=100)
        txt_M_pre_code = st.text_area(
        'M_pre', placeholder='もとになる対象手法M_preのPythonコードを入力', height=150, max_chars=10000
        )
    with tab1_2:
        txt_M_patch_name = st.text_input('M_patchの名前', placeholder='ここにM_patchの手法名を記入', max_chars=100)
        txt_M_patch_code = st.text_area(
        'M_patch', placeholder='もとになる対象手法M_patchのPythonコードを入力', height=150, max_chars=10000
        )
    with tab1_3:
        reference_python_code = st.text_area(
        'reference_python', placeholder='参考になるA_B-datasetリポジトリのPythonコードを入力', height=150, max_chars=100000
        )



with tab2:
    st.markdown('## Coder')
    st.markdown('実験用コードの作成')
    
    
    
with tab3:
    st.markdown('## Evaluator')
    st.markdown('新規手法の評価')
