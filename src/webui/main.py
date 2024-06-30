import streamlit as st
import pandas as pd
import numpy as np
from tabs.creator import creator_tab_script
from tabs.coder import coder_tab_script
from tabs.evaluator import evaluator_tab_script


st.markdown('# AutoRes')
st.markdown('## 機械学習研究の自律的な実行')

st.sidebar.title('関連リンク')
with st.sidebar:
    st.markdown('* [プロジェクトページ](https://sites.google.com/view/automated-research/home?authuser=0)')
    st.markdown('* [GitHub](https://github.com/auto-res/Mockup_python)')


creator_tab, coder_tab, evaluator_tab = st.tabs(["Creator", "Coder", "Evaluator"])


with creator_tab:
    creator_tab_script()



#with coder_tab:
    #coder_tab_script()
        
#with evaluator_tab:
    #evaluator_tab_script()
