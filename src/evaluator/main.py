from ..utils.log_config import setup_logging

from .dataset.tabledata.titanic import titanic_data
from .dataset.cv.cifar10 import cifar10_data
from .dataset.cv.cifar100 import cifar100_data
from .dataset.cv.fashion_mnist import fashion_mnist_data
from .dataset.cv.mnist import mnist_data

from .metrix.binary_classification import (
    binary_classification,
    binary_classification_objective,
)
from .metrix.multiclass_classification import (
    multiclass_classification,
    multiclass_classification_objective,
)

from ..utils.llm.openai_model import _openai_model
from ..utils.llm.google_model import _google_model
from ..utils.llm.anthropic_model import _anthropic_model

from .train.optuna import exec_optuna
import shutil

from typing import Dict, Any

_, result_logger, _ = setup_logging()


class Evaluator:
    def __init__(
        self,
        llm_name: str,
        dataset_name: str,
        params: Dict[str, Any],
        valuation_index: str,
        datasave_path: str,
        n_trials: int,
    ) -> None:
        self.llm_name = llm_name
        self.dataset_name = dataset_name
        self.params = params
        self.valuation_index = valuation_index
        self.datasave_path = datasave_path
        self.n_trials = n_trials
        self._select_dataset()
        self._select_llm()
        self.model = None
        pass

    def _select_dataset(self):
        if self.dataset_name == "titanic":
            self.datatype = "table"
            self.train_dataloader, self.test_dataloader = titanic_data()
            self.metrix = binary_classification
            self.objective = binary_classification_objective(self.valuation_index)
        elif self.dataset_name == "cifar10":
            self.datatype = "image"
            self.train_dataloader, self.test_dataloader = cifar10_data(
                self.datasave_path
            )
            self.metrix = multiclass_classification
            self.objective = multiclass_classification_objective(self.valuation_index)
        elif self.dataset_name == "cifar100":
            self.datatype = "image"
            self.train_dataloader, self.test_dataloader = cifar100_data(
                self.datasave_path
            )
            self.metrix = multiclass_classification
            self.objective = multiclass_classification_objective(self.valuation_index)
        elif self.dataset_name == "fashion_mnist":
            self.datatype = "image"
            self.train_dataloader, self.test_dataloader = fashion_mnist_data(
                self.datasave_path
            )
            self.metrix = multiclass_classification
            self.objective = multiclass_classification_objective(self.valuation_index)
        elif self.dataset_name == "mnist":
            self.datatype = "image"
            self.train_dataloader, self.test_dataloader = mnist_data(self.datasave_path)
            self.metrix = multiclass_classification
            self.objective = multiclass_classification_objective(self.valuation_index)

    def _select_llm(self):
        if self.llm_name == "gpt-4-0125-preview":
            self.llm_model = _openai_model
        elif self.llm_name == "gpt-4-turbo-2024-04-09":
            self.llm_model = _openai_model
        elif self.llm_name == "gpt-3.5-turbo-0125":
            self.llm_model = _openai_model
        elif self.llm_name == "gpt-4o-2024-05-13":
            self.llm_model = _openai_model
        elif self.llm_name == "gemini-1.5-pro":
            self.llm_model = _google_model
        elif self.llm_name == "gemini-1.5-flash":
            self.llm_model = _google_model
        elif self.llm_name == "gemini-1.0-pro":
            self.llm_model = _google_model
        elif self.llm_name == "claude-3-opus-20240229":
            self.llm_model = _anthropic_model
        elif self.llm_name == "claude-3-haiku-20240307":
            self.llm_model = _anthropic_model
        else:
            raise ValueError(f"Invalid llm_name: {self.llm_name}")
        return

    def _copy_file(self, model_path: str):
        last_slash_index = model_path.rfind("/")
        directory_path = model_path[: last_slash_index + 1]
        copy_file_path = directory_path + "copy_file.py"
        shutil.copyfile(model_path, copy_file_path)
        return copy_file_path

    def exec(self, model_path: str):
        result_logger.info("------AutoRes Evaluator Start------")
        result_logger.info(f"dataset name: {self.dataset_name}")
        result_logger.info(f"data type: {self.datatype}")
        result_logger.info(f"llm name: {self.llm_name}")
        result_logger.info(f"model path: {model_path}")
        result_logger.info(f"valuation_index: {self.valuation_index}")
        result_logger.info(f"objective: {self.objective}")
        self.copy_file_path = self._copy_file(model_path)

        best_score = exec_optuna(
            self.llm_name,
            self.llm_model,
            self.copy_file_path,
            self.train_dataloader,
            self.test_dataloader,
            self.metrix,
            self.params,
            self.valuation_index,
            self.objective,
            self.datatype,
            self.n_trials,
        )
        return best_score
