from ..utils.log_config import setup_logging

import re

from ..utils.jinja_template import make_prompt
import importlib.resources as pkg_resources


from ..utils.llm.openai import _openai_model
from ..utils.llm.google import _googel_model
from ..utils.llm.anthropic import _anthropic_model

makemethod_logger, _, _ = setup_logging()


class AutoResMaker:
    def __init__(
        self,
        llm_name: str,
        base_model: str,
        dataset_name: str,
    ) -> None:
        self.llm_name = llm_name
        self.base_model = base_model
        self.dataset_name = dataset_name
        self._load_prompt_templates()
        self._select_llm()

    def _load_prompt_templates(self) -> None:
        synthtic_prompt_mapping = {
            "base": "src.autoresmaker.prompt_template",
        }

        base_prompt_mapping = {
            "cifar10": "src.autoresmaker.prompt_template.cifar10",
        }

        model_prompt_mapping = {
            "cnn": "cnn_format_template.j2",
        }

        with pkg_resources.open_text(
            synthtic_prompt_mapping["base"], "synthetic_template.j2"
        ) as file:
            self._synthetic_prompt_template = file.read()

        with pkg_resources.open_text(
            base_prompt_mapping[self.dataset_name],
            model_prompt_mapping[self.base_model],
        ) as file:
            self._default_fit_prompt_template = file.read()

    def _select_llm(self):
        if self.llm_name == "openai":
            self.llm_model = _openai_model
        elif self.llm_name == "google":
            self.llm_model = _googel_model
        elif self.llm_name == "anthropic":
            self.llm_model = _anthropic_model
        else:
            raise ValueError(f"Invalid llm_name: {self.llm_name}")
        return

    def _method_synthetic(self, elemental_method1, elemental_method2):
        prompt_args = {
            "elemental_method1": elemental_method1,
            "elemental_method2": elemental_method2,
        }
        prompt_ = make_prompt(
            prompt_template=self._synthetic_prompt_template, **prompt_args
        )
        output = self.llm_model(prompt_)
        return output

    def _method_extraction(self, text: str, extraction_type: str):
        if extraction_type == "outer":
            pattern = re.compile(r"(<PYTHON>.*?</PYTHON>)", re.DOTALL)
            python_code = pattern.findall(text)
            return python_code
        elif extraction_type == "inner":
            pattern = re.compile(r"<PYTHON>(.*?)</PYTHON>", re.DOTALL)
            match = pattern.search(text)
            if match:
                python_code = match.group(1)
                return python_code

    def _method_format(self, synthetic_code: str):
        prompt_args = {
            "elemental_method1": self._default_fit_prompt_template,
            "elemental_method2": synthetic_code,
        }
        prompt_ = make_prompt(
            prompt_template=self._synthetic_prompt_template, **prompt_args
        )
        output = self.llm_model(prompt_)
        return output

    def exec(self, elemental_method1, elemental_method2):
        synthetic_method = self._method_synthetic(elemental_method1, elemental_method2)
        makemethod_logger.info(f"synthetic method:\n {synthetic_method}")
        synthetic_code = self._method_extraction(synthetic_method, "outer")
        makemethod_logger.info(f"synthetic code:\n {synthetic_code}")
        formatted_code = self._method_format(synthetic_code)
        makemethod_logger.info(f"formatted code:\n {formatted_code}")
        code = self._method_extraction(formatted_code, "inner")
        makemethod_logger.info(f"code:\n {code}")
        return code
