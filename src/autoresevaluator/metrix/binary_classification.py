# F1-score
# accuracy
# logloss
# ROC-AUC
# PR-AUC
# pAUC
# Precission
# Recall
import numpy as np
from sklearn.metrics import f1_score, accuracy_score, log_loss
from sklearn.metrics import roc_auc_score, auc, precision_recall_curve
from sklearn.metrics import precision_score, recall_score

from numpy.typing import NDArray

from ...utils.log_config import setup_logging

_, result_logger, _ = setup_logging()


def binary_classification(y_test, y_prob: NDArray[np.float64], valuation_index: str):
    threshold = 0.5
    y_pred = np.where(np.array(y_prob) > threshold, 1, 0)
    f1 = f1_score(y_test, y_pred)
    result_logger.info(f"f1_score: {f1}")
    accuracy = accuracy_score(y_test, y_pred)
    result_logger.info(f"accuracy: {accuracy}")
    logloss = log_loss(y_test, y_prob)
    result_logger.info(f"logloss: {logloss}")
    roc_auc = roc_auc_score(y_test, y_prob)
    result_logger.info(f"roc_auc: {roc_auc}")
    precision = precision_score(y_test, y_pred, average="binary")
    result_logger.info(f"precision: {precision}")
    recall = recall_score(y_test, y_pred, average="binary")
    result_logger.info(f"recall: {recall}")
    pre, reca, _ = precision_recall_curve(y_test, y_pred)
    pr_auc = auc(reca, pre)
    result_logger.info(f"pre: {pr_auc}")

    if valuation_index == "f1_score":
        return f1
    elif valuation_index == "accuracy":
        return accuracy
    elif valuation_index == "logloss":
        return logloss
    elif valuation_index == "roc_auc":
        return roc_auc
    elif valuation_index == "precision":
        return precision
    elif valuation_index == "recall":
        return recall
    elif valuation_index == "pr_auc":
        return pr_auc
    else:
        raise ValueError(f"valuation_index: {valuation_index} is not defined")


def binary_classification_objective(valuation_index):
    if valuation_index == "f1_score":
        return "maximize"
    elif valuation_index == "accuracy":
        return "maximize"
    elif valuation_index == "logloss":
        return "minimize"
    elif valuation_index == "roc_auc":
        return "maximize"
    elif valuation_index == "precision":
        return "maximize"
    elif valuation_index == "recall":
        return "maximize"
    elif valuation_index == "pr_auc":
        return "maximize"
