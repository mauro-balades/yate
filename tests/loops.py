from yate import YateTemplate

template = YateTemplate(
    """
    <ul>
        {% each [1, 2, 3, 4] %}
            <li>{{ it }}</li>
        {% end %}
    </ul>
"""
)
tmp = template.render()

print(tmp)
