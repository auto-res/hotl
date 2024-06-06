import streamlit as st

def evaluator_tab_script():
    st.markdown('## Evaluator')
    st.markdown('新規手法の評価')
    st.markdown('### 設定')
    llm_name = st.radio(
        'LLMの選択', 
        (
            "gpt-4-turbo-preview", 
            "gpt-4-turbo-2024-04-09",
            "gpt-3.5-turbo-0125",
            "gemini-pro",
            "claude-3-opus-20240229"
        ),
        key = "llm_name"
    )
    dataset_name = st.radio(
        'データセットの選択',
        (
            'cifar10',
            'cifar100',
            'mnist',
            'fashion_mnist'
        ),
        key = "dataset_name"
    )
    param = st.text_input('パラメータ')
    evaluation_index = st.radio(
        '最適化指標の選択',
        (
            "f1_macro",
            "f1_micro",
            "f1_weighted",
            'accuracy',
            "logloss",
            'roc_auc',
            "precision_macro",
            "recall_macro"    
        ),
        key = "evaluation_index"
    )
    datasave_path = st.text_input('検証する際のデータを保存する場所')
    n_trials = st.slider("Optunaの探索回数", 1, 100, 10)

    st.markdown('### 実行')
    exec_code_path = st.text_input('実行するコードのパス')
    if st.button("Exec", key = "exec_evaluator"):
        st.write("実行が完了しました")
    else:
        st.write("実行してください")
