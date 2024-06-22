import streamlit as st
from src.creator.yoshinosan.abstractor import Abstractor
from src.creator.yoshinosan.concretizer import Concretizer
from src.creator.yoshinosan.VALUE_src import VALUE_init
from src.creator.yoshinosan.TAG_src import TAG_init
from src.creator.yoshinosan.VALUE_src_prompts import VALUE_init_prompts
from src.creator.yoshinosan.TAG_src_prompts import TAG_init_prompts
from src.creator.yoshinosan.TAG_src_prompts import TAG_init_prompts
from src.creator.yoshinosan.TAG_src_method import TAG_init_method



def creator_tab_script():
    st.markdown('## Creator')
    if st.button('手法モード'):
        st.session_state.prompts_method = 0
        TAG_init_method()
        VALUE_init()
    if st.button('プロンプトモード'):
        st.session_state.prompts_method = 1
        TAG_init_prompts()
        VALUE_init_prompts()


    st.markdown('新規手法の作成')
    txt_GPT_id = st.text_input('GPT_ID', value='gpt-4-1106-preview', max_chars=100)
    txt_api_key = st.text_input('API Kye', placeholder='ここにAPIキーを入力', max_chars=100)

    if "txt_OBJECTIVE_value" not in st.session_state:
        st.session_state.txt_M_pre_name_value = ""
        st.session_state.txt_M_pre_code_value = ""
        st.session_state.txt_M_patch_name_value = ""
        st.session_state.txt_M_patch_code_value = ""
        st.session_state.reference_python_code_value = ""
        st.session_state.txt_OBJECTIVE_value = ""
        st.session_state.prompts_method = 0
    
    st.markdown('  \n 1. 初期値の入力')
    txt_OBJECTIVE = st.text_input(
        '目的', 
        placeholder='ここにどのように改善してほしいのか目的を記入', 
        value = st.session_state.txt_OBJECTIVE_value,
        max_chars=1000)
    
    txt_M_pre_name = st.text_input(
        'M_preの名前', 
        placeholder='ここにM_preの手法名を記入', 
        value=st.session_state.txt_M_pre_name_value,
        max_chars=100
        )
    txt_M_pre_code = st.text_area(
        'M_pre', 
        placeholder='もとになる対象手法M_preのPythonコードを入力',
        height=150, 
        value = st.session_state.txt_M_pre_code_value,
        max_chars=10000
        )
    txt_M_patch_name = st.text_input(
        'M_patchの名前', 
        placeholder='ここにM_patchの手法名を記入', 
        value = st.session_state.txt_M_patch_name_value,
        max_chars=100
        )
    txt_M_patch_code = st.text_area(
        'M_patch', 
        placeholder='もとになる対象手法M_patchのPythonコードを入力', 
        height=150, 
        value = st.session_state.txt_M_patch_code_value,
        max_chars=10000
        )
    reference_python_code = st.text_area(
        'reference_python', 
        placeholder='参考になるA_B-datasetリポジトリのPythonコードを入力', 
        height=150, 
        value = st.session_state.reference_python_code_value,
        max_chars=100000
        )
    
    if st.button('2. 抽象化の実行'):
        abs = Abstractor(txt_api_key,txt_GPT_id,txt_M_patch_code,txt_M_patch_name,
                         st.session_state.PROMPTS_abs,st.session_state.TAG_DEFINE_abs,st.session_state.prompts_method)
        st.session_state.think,st.session_state.python1,st.session_state.python2 = abs.exec()
        st.markdown('think')
        st.code(st.session_state.think, language="python")
        st.markdown('python1')
        st.code(st.session_state.python1, language="python")
        st.markdown('python2')
        st.code(st.session_state.python2, language="python")

    if st.button('3. 具体化の実行'):
        st.markdown('think')
        st.code(st.session_state.think, language="python")
        st.markdown('python1')
        st.code(st.session_state.python1, language="python")
        st.markdown('python2')
        st.code(st.session_state.python2, language="python")

        con = Concretizer(txt_api_key,txt_GPT_id,txt_M_pre_code,
                          st.session_state.python1,st.session_state.python2,st.session_state.think,txt_OBJECTIVE,
                          st.session_state.PROMPTS_con,st.session_state.TAG_DEFINE_con,st.session_state.prompts_method)
        st.session_state.mix_python,st.session_state.think2 = con.exec()
        st.markdown('think2')
        st.code(st.session_state.think2, language="python")
        st.markdown('M_post_code')
        st.code(st.session_state.mix_python, language="python")
