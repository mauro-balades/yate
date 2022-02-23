"""
| YATE engine
|-------------
| MIT License
|
| Copyright (c) 2022 Mauro Baladés
|
| Permission is hereby granted, free of charge, to any person obtaining a copy
| of this software and associated documentation files (the "Software"), to deal
| in the Software without restriction, including without limitation the rights
| to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
| copies of the Software, and to permit persons to whom the Software is
| furnished to do so, subject to the following conditions:
|
| The above copyright notice and this permission notice shall be included in all
| copies or substantial portions of the Software.
|
| THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
| IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
| FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
| AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
| LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
| OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
| SOFTWARE.
"""

import ast
from yate.errors import TemplateContextError, TemplateSyntaxError


def resolve(name, context):
    if name.startswith(".."):
        context = context.get("..", {})
        name = name[2:]
    try:
        for tok in name.split("."):
            context = context[tok]
        return context
    except KeyError:
        raise TemplateContextError(name)


def clean_loop(bits):

    if bits[0].startswith("[") and bits[0].endswith("]"):
        return bits

    arr_open = False
    as_exists = False

    arr = ""
    for i in bits:
        if i == "as" and arr_open:
            raise TemplateSyntaxError("".join(bits))
        elif i == "as":
            as_exists = True
            break

        if i.startswith("["):
            arr_open = True
            arr += i
        elif i.endswith("]"):
            arr_open = False
            arr += i
        else:
            arr += i

    if as_exists:
        return [arr, "as", bits[-1]]

    return [arr]


def eval_expression(expr):
    try:
        return "literal", ast.literal_eval(expr)
    except Exception:
        return "name", expr
