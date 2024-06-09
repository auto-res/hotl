import streamlit as st
from src.evaluator.main import Evaluator

def evaluator_tab_script():
    st.markdown('## Evaluator')
    st.markdown('新規手法の評価')
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
            key = "llm_name_for_evaluator"
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
    eval = Evaluator(
        llm_name = llm_name,
        dataset_name = dataset_name,
        params = param,
        valuation_index = evaluation_index,
        datasave_path = datasave_path,
        n_trials = n_trials,
        )

    st.markdown('### 実行')
    exec_code_path = st.text_input('実行するコードのパス')
    if st.button("Exec", key = "exec_evaluator"):
        result = eval.exec(exec_code_path)
        st.write("実行が完了しました")
        st.write(result)
    else:
        st.write("実行してください")
