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
    """
    Executes the model.

    Args:
        llm_name (str): The name of the model.
        llm_model (str): The model to be executed.
        copy_file_path (str): The file path for copying the model.
        train_dataloader (type): The training dataloader.
        test_dataloader (type): The test dataloader.
        params (type): Additional parameters for the model.

    Raises:
        ValueError: If `y_pred` is not a NumPy array.

    Returns:
        numpy.ndarray: The predicted values.
    """
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

            # Process to pass all error information to model modification
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_details = traceback.format_exception(
                exc_type, exc_value, exc_traceback
            )
            codefix(llm_name, llm_model, copy_file_path, traceback_details)

            retry_count += 1
            if retry_count >= retry_limit:
                model_logger.error("Maximum retry limit reached")

    if retry_count < retry_limit:
        model_logger.error("Execution successful, exiting the loop")
    else:
        model_logger.error("Maximum retry limit reached, execution failed")


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
    """Predict the output using the given model and dataloaders.

    Args:
        llm_name (str): The name of the model.
        llm_model (object): The model object.
        copy_file_path (str): The file path for copying the model.
        train_dataloader (object): The dataloader for training data.
        test_dataloader (object): The dataloader for test data.
        metric (function): The evaluation metric function.
        params (dict): Additional parameters for prediction.
        valuation_index (int): The index for valuation.

    Returns:
        int: The evaluation index.
    """    
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
