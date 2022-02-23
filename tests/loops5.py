from yate import YateTemplate

template = YateTemplate("""
    <ul>
        {% each [1,4125,52312," hello "] as x %}
            <li>{{ x }}</li>
        {% end %}
    </ul>
""")
tmp = template.render(list = [1, 2, 3, 4])

print(tmp)