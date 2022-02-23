from yate import YateTemplate

template = YateTemplate("<h1>hello, {{name}}</h1>")
tmp = template.render(name="YATE")

print(tmp)
