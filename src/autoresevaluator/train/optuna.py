from .dataset import pred_dataset
from .dataloader import pred_dataloader
import optuna
from ...utils.log_config import setup_logging
from tqdm.auto import tqdm

from typing import Dict, Any, Callable

optuna.logging.set_verbosity(optuna.logging.WARNING)

_, result_logger, _ = setup_logging()


def _set_trial_params(trial, params):
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
            # 'type' と 'args' キーがない場合、そのままの値を使用
            optuna_params[key] = value

    return optuna_params


def _dataset_objective(
    llm_model, copy_file_path, train_dataloader, metric, params, valuation_index
):
    def objective(trial):
        optuna_params = _set_trial_params(trial, params)
        average_index = pred_dataset(
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
    llm_model: Callable[[str], str],
    copy_file_path: str,
    train_dataloader,
    test_dataloader,
    metric: str,
    params: Dict[str, Any],
    valuation_index: str,
    objective: Callable[..., Any],
    datatype: str,
) -> None:
    result_logger.info("------Optuna start------")
    n_trials = 100
    study = optuna.create_study(direction=objective)
    if datatype == "table":
        objective = _dataset_objective(
            llm_model, copy_file_path, train_dataloader, metric, params, valuation_index
        )
    else:
        objective = _dataloader_objective(
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
    return
