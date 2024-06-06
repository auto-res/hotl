import streamlit as st

def coder_tab_script():
    st.markdown('## Coder')
    st.markdown('実験用コードの作成')
    st.markdown('### 設定')
    st.radio(
        'LLMの選択', 
        (
            "gpt-4-turbo-preview", 
            "gpt-4-turbo-2024-04-09",
            "gpt-3.5-turbo-0125",
            "gemini-pro",
            "claude-3-opus-20240229"
            )
        )
    
    st.markdown('### 実行')
    base_file_path = st.text_input('ベースとなるコードのパス', key = "base_file_path")
    new_method_path = st.text_input('新しい手法のコードのパス', key = "new_method_path")
    save_file_path = st.text_input('保存するファイルのパス', key = "save_file_path")
    if st.button("Exec", key = "exec_coder"):
        st.write("実行が完了しました")
    else:
        st.write("実行してください")
