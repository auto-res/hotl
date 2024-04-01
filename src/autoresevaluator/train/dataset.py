import numpy as np
import traceback
import sys
from sklearn.model_selection import KFold
from ...utils.log_config import setup_logging
from ..codefix import codefix
from ..load_method import load_method_from_path

_, result_logger, model_logger = setup_logging()


def _exec_model(llm_model, copy_file_path, X_train, y_train, X_test, params):
    result_logger.info("------exec model------")
    retry_limit = 10
    retry_count = 0

    while retry_count < retry_limit:
        try:
            model = load_method_from_path(copy_file_path)
            y_pred = model(X_train, y_train, X_test, params)
            if not isinstance(y_pred, np.ndarray):
                raise ValueError("y_pred must be a NumPy array.")
            return y_pred

        except Exception as error:
            model_logger.error(f"Exec Error: {error}", exc_info=True)

            # モデル修正にすべてのエラー情報を渡すための処理
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_details = traceback.format_exception(
                exc_type, exc_value, exc_traceback
            )
            codefix(llm_model, copy_file_path, traceback_details)

            retry_count += 1
            if retry_count >= retry_limit:
                model_logger.error("試行回数が上限に達しました")

    if retry_count < retry_limit:
        model_logger.error("処理が成功し、ループを終了しました")
    else:
        model_logger.error("最大試行回数を超えましたが、処理は成功しませんでした")


def pred_dataset(llm_model, copy_file_path, dataset, metrix, params, valuation_index):
    result_logger.info("------pred dataset------")
    X = dataset.drop(columns=["target"]).values
    y = dataset["target"].values

    kf = KFold(n_splits=3, shuffle=True, random_state=3655)
    i = 0
    index_list = []
    for train_index, test_index in kf.split(X):
        i += 1
        result_logger.info(f"------Round{i}------")
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        y_pred = _exec_model(
            llm_model, copy_file_path, X_train, y_train, X_test, params
        )
        index = metrix(y_test, y_pred, valuation_index)
        index_list.append(index)

    average_index = sum(index_list) / len(index_list)
    return average_index
