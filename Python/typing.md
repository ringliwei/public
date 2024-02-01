# Typing

- [Typing](#typing)
  - [resources](#resources)

```py
def check(fn):
    def wrapper(*args, **kwargs):
        print(fn.__annotations__)
        list_anno_values = list(fn.__annotations__.values())
        print(list_anno_values)

        for index, para in enumerate(args):
            # 如果True说明送参类型正确
            print(para, list_anno_values[index])
            print(isinstance(para, list_anno_values[index]))

        for k, v in kwargs.items():
            # 如果True说明送参类型正确；False说明送参错误
            print(v, fn.__annotations__[str(k)])
            print(isinstance(v, fn.__annotations__[str(k)]))

        ret = fn(*args, **kwargs)
        return ret

    return wrapper


@check  # add = check(add) #add=>wrapper
def add(x: int, y: int) -> int:
    return x + y


print(add(4, y=5))
```

## resources

- [PEP 3107 – Function Annotations](https://peps.python.org/pep-3107/)
- [PEP 484 – Type Hints](https://peps.python.org/pep-0484/)
- [PEP 593 – Flexible function and variable annotations](https://peps.python.org/pep-0593/)
- [FastAPI: Python 类型提示简介](https://fastapi.tiangolo.com/zh/python-types/)
- [Python 的类型注解 Annotation](https://zhuanlan.zhihu.com/p/139056271)
- [Mypy](https://mypy.readthedocs.io/en/latest/index.html) is a static type checker for Python.
  - [Type hints cheat sheet](https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html)
- [Python 类型提示简介](https://fastapi.tiangolo.com/zh/python-types/)
