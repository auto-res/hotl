import importlib.util
import sys
import traceback
from .codefix import codefix
from ..utils.log_config import setup_logging

_, _, model_logger = setup_logging()


def load_method_from_path(copy_file_path, method_name="model"):
    module_name = copy_file_path.split("/")[-1].split(".")[0]

    try:
        spec = importlib.util.spec_from_file_location(module_name, copy_file_path)
        model_logger.info(f"ModuleSpec: {spec}")
        module = importlib.util.module_from_spec(spec)
        model_logger.info(f"Module: {module}")
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        method = getattr(module, method_name, None)
        if method is None:
            raise model_logger.error(
                f"Method {method_name} not found in {copy_file_path}", exc_info=True
            )
        model_logger.info("メソッドが正常にインポートされました")

    except Exception as error:
        model_logger.error(
            f"Error importing method {method_name} from {copy_file_path}: {error}",
            exc_info=True,
        )

        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_details = traceback.format_exception(
            exc_type, exc_value, exc_traceback
        )
        codefix(copy_file_path, traceback_details)

        raise

    return method
