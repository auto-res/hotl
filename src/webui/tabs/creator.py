import streamlit as st
#from src.creator.yoshinosan import Abstractor

def creator_tab_script():
    st.markdown('## Creator')
    st.markdown('新規手法の作成')
    txt_OBJECTIVE = st.text_input('目的', placeholder='ここにどのように改善してほしいのか目的を記入', max_chars=1000)
    txt_GPT_id = st.text_input('GPT_ID', value='gpt-4-1106-preview', max_chars=100)
    txt_api_key = st.text_input('API Kye', placeholder='ここにAPIキーを入力', max_chars=100)

    st.markdown('  \n 1. 初期値の入力')
    creator_tab1, creator_tab2, creator_tab3 = st.tabs(["M_pre初期値", "M_post初期値", "その他初期値"])
    with creator_tab1:
        txt_M_pre_name = st.text_input(
            'M_preの名前', 
            placeholder='ここにM_preの手法名を記入', 
            max_chars=100
            )
        txt_M_pre_code = st.text_area(
            'M_pre', 
            placeholder='もとになる対象手法M_preのPythonコードを入力',
            height=150, 
            max_chars=10000
            )
    with creator_tab2:
        txt_M_patch_name = st.text_input(
            'M_patchの名前', 
            placeholder='ここにM_patchの手法名を記入', 
            max_chars=100
            )
        txt_M_patch_code = st.text_area(
            'M_patch', 
            placeholder='もとになる対象手法M_patchのPythonコードを入力', 
            height=150, 
            max_chars=10000
            )
    with creator_tab3:
        reference_python_code = st.text_area(
            'reference_python', 
            placeholder='参考になるA_B-datasetリポジトリのPythonコードを入力', 
            height=150, 
            max_chars=100000
            )
    st.markdown('  \n2. 抽象化の実行')
    
    if st.button('表示'):
        think,python1,python2 = Abstractor()
