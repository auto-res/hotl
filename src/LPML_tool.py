import ast
import traceback
from io import StringIO
from contextlib import redirect_stdout


def _exec(code, globals=None, locals=None):
    if globals is None:
        globals = {}
    if locals is None:
        locals = globals

    a = ast.parse(code)
    last_expression = None

    if a.body:
        if isinstance(a_last := a.body[-1], ast.Expr):
            last_expression = ast.unparse(a.body.pop())
        elif isinstance(a_last, ast.Assign):
            last_expression = ast.unparse(a_last.targets[0])
        elif isinstance(a_last, (ast.AnnAssign, ast.AugAssign)):
            last_expression = ast.unparse(a_last.target)

    exec(ast.unparse(a), globals, locals)

    if last_expression:
        return eval(last_expression, globals, locals)


def exec_python(code, namespace={}):
    f = StringIO()
    try:
        with redirect_stdout(f):
            ret = _exec(code, namespace)
    except:
        t = traceback.format_exc()
        return t
    ret = str(ret)
    return f.getvalue() + ret


class Python:

    def __init__(self, output_tag='OUTPUT'):
        self.output_tag = output_tag
        self.namespace = {}

    def __call__(self, element):
        if element['tag'] != 'PYTHON':
            raise ValueError
        code = '\n'.join(element['content'])
        out = exec_python(code, self.namespace).strip()
        if out == '':
            out = 'Error: Use `print()` to get output.'
        output = {
            'tag': self.output_tag,
            'attributes': element['attributes'].copy(),
            'content': ['\n', out, '\n']
        }
        return output


def python(element, output_tag='OUTPUT'):
    return Python(output_tag)(element)
