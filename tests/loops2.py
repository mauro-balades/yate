from yate import YateTemplate

template = YateTemplate(
    """
    <ul>
        {% each list as i %}
            <li>{{ i }}</li>
        {% end %}
    </ul>
"""
)
tmp = template.render(list=[1, 2, 3, 4])

print(tmp)
