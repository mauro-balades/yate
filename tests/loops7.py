
from yate import YateTemplate

template = YateTemplate("""
    <h1>
        {{name}}
    </h1>
    {% each lines %}
        <span class="{{..name}}-{{it.name}}">
            {{it.name}}
        </span>
    {% end %}
""")

ctx = {'lines': [{'name': 'l1'}], 'name': 'p1'}
tmp = template.render(**ctx)

print(tmp)