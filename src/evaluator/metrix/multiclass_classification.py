import numpy as np
from sklearn.metrics import f1_score, accuracy_score, log_loss
from sklearn.metrics import roc_auc_score
from sklearn.metrics import precision_score, recall_score
from sklearn.preprocessing import label_binarize

from ...utils.log_config import setup_logging

_, result_logger, _ = setup_logging()


def multiclass_classification(y_test, y_prob, valuation_index):
    n_classes = y_prob.shape[1]
    # 確率から予測クラスに変換
    y_pred = np.argmax(y_prob, axis=1)
    if len(y_test.shape) == 1 or y_test.shape[1] == 1:
        y_test_binarized = label_binarize(y_test, classes=np.arange(n_classes))
    else:
        y_test_binarized = y_test

    # メトリクスの計算
    accuracy = accuracy_score(y_test, y_pred)
    logloss = log_loss(y_test_binarized, y_prob)
    roc_auc = roc_auc_score(
        y_test_binarized, y_prob, multi_class="ovr", average="weighted"
    )

    # 平均パラメータを指定してメトリクスを計算
    f1_macro = f1_score(y_test, y_pred, average="macro")
    f1_micro = f1_score(y_test, y_pred, average="micro")
    f1_weighted = f1_score(y_test, y_pred, average="weighted")
    precision_macro = precision_score(y_test, y_pred, average="macro")
    recall_macro = recall_score(y_test, y_pred, average="macro")

    # ログ記録
    result_logger.info(f"Accuracy: {accuracy}")
    result_logger.info(f"Log Loss: {logloss}")
    result_logger.info(f"ROC AUC: {roc_auc}")
    result_logger.info(f"F1 Score (Macro): {f1_macro}")
    result_logger.info(f"F1 Score (Micro): {f1_micro}")
    result_logger.info(f"F1 Score (Weighted): {f1_weighted}")
    result_logger.info(f"Precision (Macro): {precision_macro}")
    result_logger.info(f"Recall (Macro): {recall_macro}")

    # 評価指標に応じた結果を返す
    if valuation_index == "f1_macro":
        return f1_macro
    elif valuation_index == "f1_micro":
        return f1_micro
    elif valuation_index == "f1_weighted":
        return f1_weighted
    elif valuation_index == "accuracy":
        return accuracy
    elif valuation_index == "logloss":
        return logloss
    elif valuation_index == "roc_auc":
        return roc_auc
    elif valuation_index == "precision_macro":
        return precision_macro
    elif valuation_index == "recall_macro":
        return recall_macro
    else:
        raise ValueError(f"valuation_index: {valuation_index} is not defined")


# 目的関数は、指標に応じて最大化または最小化を指定します。
def multiclass_classification_objective(valuation_index):
    if valuation_index in [
        "f1_macro",
        "f1_micro",
        "f1_weighted",
        "accuracy",
        "precision_macro",
        "recall_macro",
        "roc_auc",
    ]:
        return "maximize"
    elif valuation_index == "logloss":
        return "minimize"
    else:
        raise ValueError(
            f"valuation_index: {valuation_index} is not directly supported for multi-class in this snippet"
        )
