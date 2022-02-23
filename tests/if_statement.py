from yate import YateTemplate

template = YateTemplate(
    """
    {% if True %}
        true
    {% else %}
        false
    {% end %}
"""
)

tmp = template.render()

print(tmp)
