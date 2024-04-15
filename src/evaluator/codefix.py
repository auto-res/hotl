from ..utils.log_config import setup_logging

_, _, model_logger = setup_logging()


def codefix(llm_name, llm_model, copy_file_path, error):
    """Fixes the code based on the given error message.

    Args:
        llm_name (str): The name of the llm.
        llm_model (object): The llm model object.
        copy_file_path (str): The path of the file to be fixed.
        error (str): The error message.

    Returns:
        None
    """    
    model_logger.info("------Codefix------")

    with open(copy_file_path, "r") as file:
        content = file.read()

    input = """
    * Python code
    ---
    {content}
    ---
    * Error message
    ---
    {error}
    ---
    Correct the "Python code" based on the "Error message". Output only the modified "Python code" without using the code block.
    """.format(content=content, error=error)

    output = llm_model(llm_name, input)
    model_logger.info(f"output: {output}")

    with open(copy_file_path, "w") as file:
        file.write(output)

    return
