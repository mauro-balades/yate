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

from argparse import ArgumentError
from yate.errors import TemplateError, TemplateSyntaxError
from yate.nodes import (
    Call,
    Loop,
    ElseStatement,
    Fragment,
    IfStatement,
    Root,
    Text,
    Variable,
)

from yate.tokens import (
    CLOSE_BLOCK_FRAGMENT,
    OPEN_BLOCK_FRAGMENT,
    TEXT_FRAGMENT,
    TOK_REGEX,
    VAR_FRAGMENT,
)


class YateLexer:
    """The lexer will parse the template
    and separating the contents into fragments.

    Each fragment can either be arbitrary HTML or a tag.

    Args:
        source [str]: The HTML template to be parsed.
    """

    def __init__(self, *args, **kwargs):
        self.source = kwargs.get("source", None)

        if self.source is None:
            raise ArgumentError("Template source code not given in arguments")

    def tokenize(self):
        root = Root()
        scope_stack = [root]
        for fragment in self.each_fragment():
            if not scope_stack:
                raise TemplateError("nesting issues")

            parent_scope = scope_stack[-1]
            if fragment.type == CLOSE_BLOCK_FRAGMENT:
                parent_scope.exit_scope()
                scope_stack.pop()
                continue

            new_node = self.create_node(fragment)
            if new_node:
                parent_scope.children.append(new_node)
                if new_node.creates_scope:
                    scope_stack.append(new_node)
                    new_node.enter_scope()
        return root

    # INNER METHODS

    def split(self):
        return TOK_REGEX.split(self.source)

    def each_fragment(self):
        for fragment in self.split():
            if fragment:
                yield Fragment(fragment)

    def create_node(self, fragment):
        node_class = None

        if fragment.type == TEXT_FRAGMENT:
            node_class = Text

        elif fragment.type == VAR_FRAGMENT:
            node_class = Variable

        elif fragment.type == OPEN_BLOCK_FRAGMENT:
            command = fragment.clean.split()[0]
            if command == "each":
                node_class = Loop
            elif command == "if":
                node_class = IfStatement
            elif command == "else":
                node_class = ElseStatement
            elif command == "call":
                node_class = Call

        if node_class is None:
            raise TemplateSyntaxError(fragment)

        return node_class(fragment.clean)

    def __str__(self):
        return self.source

    def __repr__(self):
        return '<YateLexer src="%s"' % self.source
