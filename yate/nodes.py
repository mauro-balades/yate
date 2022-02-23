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

import operator
from yate.errors import TemplateError, TemplateSyntaxError
from yate.utils import clean_loop, eval_expression, resolve
from yate.tokens import (
    operator_lookup_table,
    BLOCK_TOKEN_START,
    CLOSE_BLOCK_FRAGMENT,
    OPEN_BLOCK_FRAGMENT,
    TEXT_FRAGMENT,
    VAR_FRAGMENT,
    VAR_TOKEN_START,
    WHITESPACE,
)


class Fragment(object):
    def __init__(self, raw_text):
        self.raw = raw_text
        self.clean = self.clean_fragment()

    def clean_fragment(self):
        if self.raw[:2] in (VAR_TOKEN_START, BLOCK_TOKEN_START):
            return self.raw.strip()[2:-2].strip()
        return self.raw

    @property
    def type(self):
        raw_start = self.raw[:2]
        if raw_start == VAR_TOKEN_START:
            return VAR_FRAGMENT
        elif raw_start == BLOCK_TOKEN_START:
            return (
                CLOSE_BLOCK_FRAGMENT if self.clean[:3] == "end" else OPEN_BLOCK_FRAGMENT
            )
        else:
            return TEXT_FRAGMENT


class _Node(object):
    creates_scope = False

    def __init__(self, fragment=None):
        self.children = []
        self.process_fragment(fragment)

    def process_fragment(self, fragment):
        pass

    def enter_scope(self):
        pass

    def render(self, context):
        pass

    def exit_scope(self):
        pass

    def render_children(self, context, children=None):
        if children is None:
            children = self.children

        def render_child(child):
            child_html = child.render(context)
            return "" if not child_html else str(child_html)

        return "".join(map(render_child, children))


class _ScopableNode(_Node):
    creates_scope = True


class Root(_Node):
    def render(self, context):
        return self.render_children(context)


class Variable(_Node):
    def process_fragment(self, fragment):
        self.name = fragment

    def render(self, context):
        return resolve(self.name, context)


class Loop(_ScopableNode):
    def process_fragment(self, fragment):
        try:
            _, it = WHITESPACE.split(fragment, 1)
            self.it_name = "it"

            bits = clean_loop(fragment.split()[1:])
            if len(bits) > 1:
                if bits[1] == "as":
                    if len(bits) > 2:
                        self.it_name = bits[2]

                    else:
                        raise TemplateSyntaxError(it)
                else:
                    raise TemplateSyntaxError(it)

            self.it = eval_expression(bits[0])
        except ValueError:
            raise TemplateSyntaxError(fragment)

    def render(self, context):

        items = self.it[1] if self.it[0] == "literal" else resolve(self.it[1], context)

        def render_item(item):
            return self.render_children({"..": context, self.it_name: item})

        return "".join(map(render_item, items))


class IfStatement(_ScopableNode):
    def process_fragment(self, fragment):
        bits = fragment.split()[1:]
        if len(bits) not in (1, 3):
            raise TemplateSyntaxError(fragment)
        self.lhs = eval_expression(bits[0])
        if len(bits) == 3:
            self.op = bits[1]
            self.rhs = eval_expression(bits[2])

    def render(self, context):
        lhs = self.resolve_side(self.lhs, context)
        if hasattr(self, "op"):
            op = operator_lookup_table.get(self.op)
            if op is None:
                raise TemplateSyntaxError(self.op)
            rhs = self.resolve_side(self.rhs, context)
            exec_if_branch = op(lhs, rhs)
        else:
            exec_if_branch = operator.truth(lhs)
        self.if_branch, self.else_branch = self.split_children()
        return self.render_children(
            context, self.if_branch if exec_if_branch else self.else_branch
        )

    def resolve_side(self, side, context):
        return side[1] if side[0] == "literal" else resolve(side[1], context)

    def exit_scope(self):
        self.if_branch, self.else_branch = self.split_children()

    def split_children(self):
        if_branch, else_branch = [], []
        curr = if_branch
        for child in self.children:
            if isinstance(child, ElseStatement):
                curr = else_branch
                continue
            curr.append(child)
        return if_branch, else_branch


class ElseStatement(_Node):
    def render(self, context):
        pass


class Call(_Node):
    def process_fragment(self, fragment):
        try:
            bits = WHITESPACE.split(fragment)
            self.callable = bits[1]
            self.args, self.kwargs = self._parse_params(bits[2:])
        except Exception as e:
            raise TemplateSyntaxError(fragment)

    def _parse_params(self, params):
        args, kwargs = [], {}
        for param in params:
            if "=" in param:
                name, value = param.split("=")
                kwargs[name] = eval_expression(value)
            else:
                args.append(eval_expression(param))
        return args, kwargs

    def render(self, context):
        resolved_args, resolved_kwargs = [], {}
        for kind, value in self.args:
            if kind == "name":
                value = resolve(value, context)
            resolved_args.append(value)
        for key, (kind, value) in self.kwargs.items():
            if kind == "name":
                value = resolve(value, context)
            resolved_kwargs[key] = value
        resolved_callable = resolve(self.callable, context)
        if hasattr(resolved_callable, "__call__"):
            return resolved_callable(*resolved_args, **resolved_kwargs)
        else:
            raise TemplateError("'%s' is not a callable" % self.callable)


class Text(_Node):
    def process_fragment(self, fragment):
        self.text = fragment

    def render(self, context):
        return self.text
