from yate import YateTemplate

template = YateTemplate("<h1>{{hello}}</h1>")
template.render(hello = "hello")
