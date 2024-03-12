class LLMFunction:

    def __init__(self, llm, template, variables=[]):
        self.llm = llm
        self.template = template
        self.variables = variables

    def __call__(self, **kwargs):
        prompt = self.template.format(**kwargs)
        messages = [{'role': 'system', 'content': prompt}]
        res = self.llm(messages)
        return res
