#import sys
#sys.path.append('/root/src')

import streamlit as st
from src.coder.main import Coder

def coder_tab_script():
    st.markdown('## Coder')
    st.markdown('実験用コードの作成')
    st.markdown('### 設定')
    llm_name = st.radio(
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
    coder = Coder(llm_name = llm_name)
    
    st.markdown('### 実行')
    base_file_path = st.text_input('ベースとなるコードのパス', key = "base_file_path")
    new_method_path = st.text_input('新しい手法のコードのパス', key = "new_method_path")
    save_file_path = st.text_input('保存するファイルのパス', key = "save_file_path")
    if st.button("Exec", key = "exec_coder"):
        exec_code = coder.exec(base_file_path, new_method_path, save_file_path)
        st.write("実行が完了しました")
        st.write(exec_code)
    else:
        st.write("実行してください")
