from yate import YateTemplate

template = YateTemplate(
    """
    {% if var == 2 %}
        true
    {% else %}
        false
    {% end %}
"""
)

tmp = template.render(var=2)

print(tmp)
