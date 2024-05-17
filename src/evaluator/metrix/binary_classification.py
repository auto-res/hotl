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
    """
    Calculate evaluation metrics for binary classification.

    Args:
        y_test (array-like): True labels of the binary classification.
        y_prob (NDArray[np.float64]): Predicted probabilities of the positive class.
        valuation_index (str): The evaluation metric to calculate. Can be one of the following:
            - "f1_score": F1 score
            - "accuracy": Accuracy
            - "logloss": Logarithmic loss
            - "roc_auc": Area under the ROC curve
            - "precision": Precision
            - "recall": Recall
            - "pr_auc": Area under the precision-recall curve

    Raises:
        ValueError: If the valuation_index is not one of the defined options.

    Returns:
        float: The value of the specified evaluation metric.
    """    
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
    """Returns the optimization direction for a given valuation index.

    Args:
        valuation_index (str): The valuation index to determine the optimization direction for.

    Returns:
        str: The optimization direction for the given valuation index. Possible values are 'maximize' or 'minimize'.
    """    
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
