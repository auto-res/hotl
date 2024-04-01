import logging


def setup_logging():
    # ロガー1の設定
    makemethod_logger = logging.getLogger("MakeMethodLogger")
    makemethod_logger.setLevel(logging.DEBUG)
    if not makemethod_logger.handlers:
        handler1 = logging.FileHandler("makemethod.log", mode="w")
        formatter1 = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler1.setFormatter(formatter1)
        makemethod_logger.addHandler(handler1)

    # ロガー2の設定
    result_logger = logging.getLogger("ResultLogger")
    result_logger.setLevel(logging.DEBUG)
    if not result_logger.handlers:
        handler2 = logging.FileHandler("result.log", mode="w")
        formatter2 = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler2.setFormatter(formatter2)
        result_logger.addHandler(handler2)

    # ロガー3の設定
    model_logger = logging.getLogger("ModelErrorLogger")
    model_logger.setLevel(logging.DEBUG)
    if not model_logger.handlers:
        handler3 = logging.FileHandler("model_error.log", mode="w")
        formatter3 = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler3.setFormatter(formatter3)
        model_logger.addHandler(handler3)

    return makemethod_logger, result_logger, model_logger
