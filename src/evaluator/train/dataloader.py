import numpy as np
from ..codefix import codefix
from ...utils.log_config import setup_logging
from ..load_method import load_method_from_path
import traceback
import sys

_, result_logger, model_logger = setup_logging()


def _exec_model(
    llm_name, llm_model, copy_file_path, train_dataloader, test_dataloader, params
):
    result_logger.info("------exec model------")
    retry_limit = 10
    retry_count = 0

    while retry_count < retry_limit:
        try:
            model = load_method_from_path(copy_file_path)
            y_pred = model(train_dataloader, test_dataloader, params)
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
            codefix(llm_name, llm_model, copy_file_path, traceback_details)

            retry_count += 1
            if retry_count >= retry_limit:
                model_logger.error("試行回数が上限に達しました")

    if retry_count < retry_limit:
        model_logger.error("処理が成功し、ループを終了しました")
    else:
        model_logger.error("最大試行回数を超えましたが、処理は成功しませんでした")


def pred_dataloader(
    llm_name,
    llm_model,
    copy_file_path,
    train_dataloader,
    test_dataloader,
    metric,
    params,
    valuation_index,
):
    result_logger.info("------pred dataloader------")
    y_pred = _exec_model(
        llm_name, llm_model, copy_file_path, train_dataloader, test_dataloader, params
    )

    y_true = []
    for data in test_dataloader:
        _, labels = data
        y_true.extend(labels.numpy())
    y_true = np.array(y_true)

    index = metric(y_true, y_pred, valuation_index)
    return index
