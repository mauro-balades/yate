
from yate import YateTemplate

def sum(n1 = 5, n2 = 5):
    return n1 + n2

template = YateTemplate("{% call sum %}") # 10
tmp = template.render(sum = sum)
print(tmp)

template = YateTemplate("{% call sum 2 5 %}") # 7
tmp = template.render(sum = sum)
print(tmp)

template = YateTemplate("{% call sum n2=5 2 %}") # 7
tmp = template.render(sum = sum)
print(tmp)

template = YateTemplate("{% call sum var 5 %}") # 7
tmp = template.render(sum = sum, var = 2)
print(tmp)

template = YateTemplate("{% call sum n2=2 %}") # 7
tmp = template.render(sum = sum)
print(tmp)

