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
import io

from yate.lexer import YateLexer


class YateTemplate:
    """Yet another template engine. Yate is a small, fast html template engine.

    In this class, user will be able to access al of yate's functions such as
    fill the template.

    The template engine will consist of the classic curly brace style. Since we
    are implementing our engine in Python, some Python concepts will appear in
    our syntax.

    Data from the context is inserted using double curly braces.
        => `hello, {{ name }}`

    This data will be probided from a context object when the template is being
    rendered.

    python:
        dict["key"]
        obj.attr
        obj.method()

    template:
        dict.key
        obj.attr
        obj.method

    The dot will access object attributes or dictionary values, and if the resulting
    value is callable, it's automatically called. This is different than the Python code,
    where you need to use different syntax for those operations.

    You can use functions called filters to modify values. Filters are invoked with a pipe
    character:
        => `<p>Short name: {{story.subject|slugify|lower}}</p>`

    Building interesting pages usually requires at least a small amount of decision-making,
    so conditionals are available:
        => `{% if num > 5 %}
                <div>more than 5</div>
            {% else %}
                <div>less than or equal to 5</div>
            {% end %}`

    Conditionals need no explanation. Our language will support if and else constructs,
    and the following operators: `==`, `<=`, `>=`, `!=`, `is`, `>`, `<`.

    Callables can be passed via the template context and get called with positional or keyword
    arguments in the template. Call blocks do not need to be closed.
        => `<div class='date'>
                {% call prettify date_created %}
            </div>
            <div>
                {% call log 'here' verbosity='debug' %}
            </div>`

    There is also for loops included into the template engine. Loops allow for iterations
    over collections or iterable objects.
        => `{% each [1, 2, 3] as it %}
                <div>{{it}}</div>
            {% end %}

            {% each records %}
                <div>{{..name}}</div>
            {% end %}`

    In the example above, it refers to the current item in the iteration.
    Dotted paths in names will resolve to nested dictionary attributes. Using ’..’ we
    can access names in the parent context.

    Args:
        source [str | file]: String or file object ready to be compiled.
    """

    def __init__(self, source, *args, **kwargs):

        self.source = source

        if isinstance(self.source, io.IOBase):
            self.source = self.source.read()
        elif isinstance(self.source, str):
            pass  # Already declared as a string
        else:
            raise ArgumentError(
                'Source is neither a string or a file object, instead it is a "%s".'
                % type(source)
            )

        self._lexer: YateLexer = YateLexer(source=self.source)

    def render(self, *args, **kwargs):
        tree = self._lexer.tokenize()
        return tree.render(kwargs)
