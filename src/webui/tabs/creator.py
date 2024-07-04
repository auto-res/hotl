import streamlit as st
from src.creator.abstractor import Abstractor
from src.creator.concretizer import Concretizer
from src.creator.validation_prompt import Validation_prompt
from src.creator.correction_prompt import Correction_prompt
from src.creator.VALUE_src import VALUE_init
from src.creator.TAG_src import TAG_init
from src.creator.VALUE_src_prompts import VALUE_init_prompts
from src.creator.TAG_src_prompts import TAG_init_prompts
from src.creator.TAG_src_prompts import TAG_init_prompts
from src.creator.TAG_src_method import TAG_init_method
from src.utils.llm.openai_model import _openai_model
from src.utils.llm.google_model import _google_model
from src.utils.llm.anthropic_model import _anthropic_model

def _select_llm(llm_name):
    if llm_name == "gpt-4-0125-preview":
        llm_model = _openai_model
    elif llm_name == "gpt-4-turbo-2024-04-09":
        llm_model = _openai_model
    elif llm_name == "gpt-3.5-turbo-0125":
        llm_model = _openai_model
    elif llm_name == "gpt-4o-2024-05-13":
        llm_model = _openai_model
    elif llm_name == "gemini-1.5-pro":
        llm_model = _google_model
    elif llm_name == "gemini-1.5-flash":
        llm_model = _google_model
    elif llm_name == "gemini-1.0-pro":
        llm_model = _google_model
    elif llm_name == "claude-3-opus-20240229":
        llm_model = _anthropic_model
    elif llm_name == "claude-3-haiku-20240307":
        llm_model = _anthropic_model
    else:
        raise ValueError(f"Invalid llm_name: {llm_name}")
    return llm_model

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
    st.session_state.llm_name = st.radio(
    'LLMの選択', 
    (
        "gpt-4o-2024-05-13",
        "gpt-4-0125-preview", 
        "gpt-4-turbo-2024-04-09",
        "gpt-3.5-turbo-0125",
        "gemini-1.5-pro",
        "gemini-1.5-flash",
        "gemini-1.0-pro",
        "claude-3-opus-20240229",
        "claude-3-haiku-20240307"
        ),
        key = "llm_name_for_coder"
    )    
    txt_api_key = st.text_input('API Kye', placeholder='ここにAPIキーを入力', max_chars=100)


    st.session_state.llm_model = _select_llm(st.session_state.llm_name)

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
    
    if st.button('抽象化・具体化の実行'):
        abs = Abstractor(st.session_state.llm_model,st.session_state.llm_name,txt_api_key,txt_M_patch_code,txt_M_patch_name,
                         st.session_state.PROMPTS_abs,st.session_state.TAG_DEFINE_abs,st.session_state.prompts_method)
        st.session_state.think,st.session_state.python1,st.session_state.python2 = abs.exec()
        st.markdown('## 抽象化結果')
        st.markdown('think')
        st.code(st.session_state.think, language="python")
        st.markdown('python1')
        st.code(st.session_state.python1, language="python")
        st.markdown('python2')
        st.code(st.session_state.python2, language="python")

        con = Concretizer(st.session_state.llm_model,st.session_state.llm_name,txt_api_key,txt_M_pre_code,
                          st.session_state.python1,st.session_state.python2,st.session_state.think,txt_OBJECTIVE,
                          st.session_state.PROMPTS_con,st.session_state.TAG_DEFINE_con,st.session_state.prompts_method)
        st.session_state.mix_python,st.session_state.mix_python_element,st.session_state.think2 = con.exec()
        st.markdown('## 具体化結果')
        st.markdown('think2')
        st.code(st.session_state.think2, language="python")
        st.markdown('M_post_code')
        st.code(st.session_state.mix_python, language="python")

    if st.session_state.prompts_method == 1:
        if st.button('プロンプト検証開始'):
            st.markdown('## 抽象化結果')
            st.markdown('think')
            st.code(st.session_state.think, language="python")
            st.markdown('python1')
            st.code(st.session_state.python1, language="python")
            st.markdown('python2')
            st.code(st.session_state.python2, language="python")
            st.markdown('## 具体化結果')
            st.markdown('think2')
            st.code(st.session_state.think2, language="python")
            st.markdown('M_post_code')
            st.code(st.session_state.mix_python, language="python")

            val = Validation_prompt(st.session_state.llm_model,st.session_state.llm_name,txt_api_key,
                                    st.session_state.mix_python_element,reference_python_code)
            st.session_state.val_prompt = val.exec()
            st.markdown('## 検証結果')
            st.code(st.session_state.val_prompt, language="latex")
            st.session_state.judge = val.val()
            st.code(st.session_state.judge, language="python")



        if st.button('試行開始'):
            st.markdown('## 抽象化結果')
            st.markdown('think')
            st.code(st.session_state.think, language="python")
            st.markdown('python1')
            st.code(st.session_state.python1, language="python")
            st.markdown('python2')
            st.code(st.session_state.python2, language="python")
            st.markdown('## 具体化結果')
            st.markdown('think2')
            st.code(st.session_state.think2, language="python")
            st.markdown('M_post_code')
            st.code(st.session_state.mix_python, language="python")

            st.session_state.txt_correction = st.text_input(
                    '試行回数',  
                    value = 5,
                    max_chars=10)

            for correction_n in range(int(st.session_state.txt_correction)):
                cor = Correction_prompt(st.session_state.llm_model,st.session_state.llm_name,txt_api_key,
                            st.session_state.PROMPTS_abs,st.session_state.PROMPTS_con,st.session_state.mix_python_element)
                st.session_state.ret = cor.exec()
                st.code(st.session_state.ret, language="latex")
                    

            

