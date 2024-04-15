from .dataset import pred_dataset
from .dataloader import pred_dataloader
import optuna
from ...utils.log_config import setup_logging
from tqdm.auto import tqdm

from typing import Dict, Any, Callable

optuna.logging.set_verbosity(optuna.logging.WARNING)

_, result_logger, _ = setup_logging()


def _set_trial_params(trial, params):
    """Set trial parameters for Optuna.

    This function sets the trial parameters for Optuna based on the given `params` dictionary.

    Args:
        trial (optuna.trial.Trial): The Optuna trial object.
        params (dict): A dictionary containing the parameter values.

    Raises:
        ValueError: If an unsupported parameter type is encountered.

    Returns:
        dict: A dictionary containing the Optuna trial parameters.
    """    
    optuna_params = {}
    for key, value in params.items():
        if isinstance(value, dict):
            if "type" in value and "args" in value:
                param_type = value["type"]
                if param_type == "log_float":
                    optuna_params[key] = trial.suggest_float(
                        key, *value["args"], log=True
                    )
                elif param_type == "float":
                    optuna_params[key] = trial.suggest_float(key, *value["args"])
                elif param_type == "int":
                    optuna_params[key] = trial.suggest_int(key, *value["args"])
                else:
                    raise ValueError(f"Unsupported parameter type: {param_type}")
        else:
            # If 'type' and 'args' keys are not present, use the value as is
            optuna_params[key] = value

    return optuna_params


def _dataset_objective(
    llm_name,
    llm_model,
    copy_file_path,
    train_dataloader,
    metric,
    params,
    valuation_index,
):
    def objective(trial):
        optuna_params = _set_trial_params(trial, params)
        average_index = pred_dataset(
            llm_name,
            llm_model,
            copy_file_path,
            train_dataloader,
            metric,
            optuna_params,
            valuation_index,
        )

        return average_index

    return objective


def _dataloader_objective(
    llm_name,
    llm_model,
    copy_file_path,
    train_dataloader,
    test_dataloader,
    metric,
    params,
    valuation_index,
):
    def objective(trial):
        optuna_params = _set_trial_params(trial, params)
        average_index = pred_dataloader(
            llm_name,
            llm_model,
            copy_file_path,
            train_dataloader,
            test_dataloader,
            metric,
            optuna_params,
            valuation_index,
        )

        return average_index

    return objective


def exec_optuna(
    llm_name: str,
    llm_model: Callable[[str], str],
    copy_file_path: str,
    train_dataloader,
    test_dataloader,
    metric: str,
    params: Dict[str, Any],
    valuation_index: str,
    objective: Callable[..., Any],
    datatype: str,
    n_trials: int,
) -> None:
    """Executes the Optuna hyperparameter optimization.

    This function performs hyperparameter optimization using Optuna library.
    It creates an Optuna study, defines the objective function, and optimizes it
    for a given number of trials.

    Args:
        llm_name (str): The name of the LLM.
        llm_model (Callable[[str], str]): The function that returns the LLM model.
        copy_file_path (str): The path to the file to be copied.
        train_dataloader (_type_): The training dataloader.
        test_dataloader (_type_): The test dataloader.
        metric (str): The evaluation metric.
        params (Dict[str, Any]): The dictionary of hyperparameters.
        valuation_index (str): The index used for valuation.
        objective (Callable[..., Any]): The objective function to be optimized.
        datatype (str): The type of data (either "table" or "dataloader").
        n_trials (int): The number of trials for optimization.

    Returns:
        _type_: The best value obtained from the optimization.
    """    
    result_logger.info("------Optuna start------")
    study = optuna.create_study(direction=objective)
    if datatype == "table":
        objective = _dataset_objective(
            llm_name,
            llm_model,
            copy_file_path,
            train_dataloader,
            metric,
            params,
            valuation_index,
        )
    else:
        objective = _dataloader_objective(
            llm_name,
            llm_model,
            copy_file_path,
            train_dataloader,
            test_dataloader,
            metric,
            params,
            valuation_index,
        )
    with tqdm(total=n_trials) as bar:

        def callback(study, trial):
            bar.update(1)

        study.optimize(objective, n_trials=n_trials, callbacks=[callback])
    result_logger.info(f"Best params:{study.best_params}")
    result_logger.info(f"Best score:{study.best_value}")
    return study.best_value
