# yate (Yet a small template engine)
Yet another template engine. Yate is a small, fast html template engine.

```html
<ul>
    {% each [1, 2, 3, 4] as x %}
        <li>{{ x }}</li>
    {% end %}
<ul>
```

## Installation

This package is registered in [pypi](https://pypi.org/project/yate-engine/). This means that by using the `pip` command yate will be installed.

Install yate by runing the following command:
```
$ pip3 install yate-engine
```

## Documentation

The documentation for `yate` can be found at the [wiki](https://github.com/mauro-balades/yate/wiki/Documentation).

## License

Yate is under the license of `MIT`. Check it out in [LICENSE](./LICENSE)
