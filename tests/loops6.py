from yate import YateTemplate

template = YateTemplate("""
    <ul>
        {% each dict as x %}
            <li>{{ x.name }}</li>
        {% end %}
    </ul>
""")
tmp = template.render(dict = [{ "name": "hello" }])

print(tmp)