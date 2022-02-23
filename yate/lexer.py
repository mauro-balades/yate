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
import re

from yate.tokens import TOK_REGEX


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
        return TOK_REGEX.split(self.source)

    def __str__(self):
        return self.source

    def __repr__(self):
        return "<YateLexer src=\"%s\"" % self.source