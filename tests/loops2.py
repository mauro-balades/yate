from yate import YateTemplate

template = YateTemplate(
    """
    <ul>
        {% each my_array as i %}
            <li>{{ i }}</li>
        {% end %}
    </ul>
"""
)
tmp = template.render(my_array=[1, 2, 3, 4])

print(tmp)
