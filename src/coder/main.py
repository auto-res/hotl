from ..utils.log_config import setup_logging

import re

from ..utils.jinja_template import make_prompt
import importlib.resources as pkg_resources


from ..utils.llm.openai import _openai_model
from ..utils.llm.google import _googel_model
from ..utils.llm.anthropic import _anthropic_model


makemethod_logger, _, _ = setup_logging()


class Coder:
    def __init__(
        self,
        llm_name: str,
        save_dir: str,
    ):
        self.llm_name = llm_name
        self.save_dir = save_dir
        self._load_prompt_templates()
        self._select_llm()

    def _load_prompt_templates(self) -> None:
        prompt_template_mapping = {
            "path": "src.utils.prompt_template",
        }

        with pkg_resources.open_text(
            prompt_template_mapping["path"], "synthetic_template.j2"
        ) as file:
            self._synthetic_prompt_template = file.read()

        with pkg_resources.open_text(
            prompt_template_mapping["path"],
            "base.j2",
        ) as file:
            self._base_model_template = file.read()

    def _select_llm(self):
        if self.llm_name == "gpt-4-turbo-preview":
            self.llm_model = _openai_model
        elif self.llm_name == "gpt-3.5-turbo-0125":
            self.llm_model = _openai_model
        elif self.llm_name == "gemini-pro":
            self.llm_model = _googel_model
        elif self.llm_name == "claude-3-opus-20240229":
            self.llm_model = _anthropic_model
        else:
            raise ValueError(f"Invalid llm_name: {self.llm_name}")
        return

    def _code2lpml(self, code: str):
        lpml_args = {
            "base_code": code,
        }
        lpml_base_code = make_prompt(
            prompt_template=self._base_model_template, **lpml_args
        )
        return lpml_base_code

    def _read_file(self, new_method_path):
        with open(new_method_path, "r") as f:
            new_method = f.read()
        return new_method

    def _exec_lpml(self, method1, method2):
        prompt_args = {
            "elemental_method1": method1,
            "elemental_method2": method2,
        }
        prompt = make_prompt(
            prompt_template=self._synthetic_prompt_template, **prompt_args
        )
        output = self.llm_model(self.llm_name, prompt)
        return output

    def _method_extraction(self, text: str):
        pattern = re.compile(r"<PYTHON>(.*?)</PYTHON>", re.DOTALL)
        match = pattern.search(text)
        if match:
            python_code = match.group(1)
            return python_code

    def _write_file(self, save_file_name, exec_code):
        save_path = self.save_dir + save_file_name
        with open(save_path, "w") as f:
            f.write(exec_code)
        return save_path

    def exec(self, base_code_path, new_method_path, save_file_name):
        base_code = self._read_file(base_code_path)
        new_method = self._read_file(new_method_path)
        lpml_base_code = self._code2lpml(base_code)
        lpml_output = self._exec_lpml(lpml_base_code, new_method)
        # makemethod_logger.info(f"synthetic method:\n {synthetic_method}")
        exec_code = self._method_extraction(lpml_output)
        # makemethod_logger.info(f"synthetic code:\n {synthetic_code}")
        exec_code_path = self._write_file(save_file_name, exec_code)
        return exec_code_path
