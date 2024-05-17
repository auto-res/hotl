import numpy as np
import traceback
import sys
from sklearn.model_selection import KFold
from ...utils.log_config import setup_logging
from ..codefix import codefix
from ..load_method import load_method_from_path

_, result_logger, model_logger = setup_logging()


def _exec_model(llm_name, llm_model, copy_file_path, X_train, y_train, X_test, params):
    """
    Executes the model.

    Args:
        llm_name (str): The name of the model.
        llm_model (str): The model to be executed.
        copy_file_path (str): The file path of the model.
        X_train (array-like): The training data.
        y_train (array-like): The target values for the training data.
        X_test (array-like): The test data.
        params (dict): Additional parameters for the model.

    Raises:
        ValueError: If the predicted values are not a NumPy array.

    Returns:
        array-like: The predicted values.
    """
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

            # Process to pass all error information to model fix
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_details = traceback.format_exception(
                exc_type, exc_value, exc_traceback
            )
            codefix(llm_name, llm_model, copy_file_path, traceback_details)

            retry_count += 1
            if retry_count >= retry_limit:
                model_logger.error("Maximum retry limit reached")

    if retry_count < retry_limit:
        model_logger.error("Execution successful, exiting loop")
    else:
        model_logger.error("Maximum retry limit reached, execution failed")


def pred_dataset(llm_model, copy_file_path, dataset, metrix, params, valuation_index):
    """
    Predicts the target variable using the provided LLN model and evaluates the performance using the given metrics.

    Args:
        llm_model (object): The LLN model object used for prediction.
        copy_file_path (str): The file path for copying the model.
        dataset (pandas.DataFrame): The dataset containing the features and target variable.
        metrix (function): The evaluation metric function to be used.
        params (dict): Additional parameters for model execution.
        valuation_index (int): The index used for valuation.

    Returns:
        float: The average evaluation index across multiple rounds of prediction.

    """
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
