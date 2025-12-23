# dumpobj

一个用于以结构化树形方式查看并美观打印 Python 对象的小工具。

它会遍历对象，构建一个中立的 Node 树（key/props/attrs/value/children），再通过可插拔的格式化器进行渲染（内置了一个纯文本格式化器）。

- 无第三方依赖，Python 3.11+
- 支持内置容器、原始类型、类、实例、异常、以及省略号 Ellipsis
- 支持控制遍历深度、每类项目数量上限、循环引用处理
- 支持注册自定义类型处理器

## 安装

```
pip install dumpobj
```

需要 Python 3.11 及以上版本。

## 快速上手

```python
from dumpobj._dumpobj import Dump
from dumpobj.formatter.plain_formatter import PlainFormatter

obj = {
    "a": [1, 2, 3, 4, 5],
    "b": "ABCDEFG",
    "c": {"x": 1, "y": 2},
}

# 构建树
d = Dump()
d.set_in_detail(True)          # True：以树展开明细；False：对许多类型仅输出一行摘要
d.set_head_count(3)            # 对容器/字符串仅输出前 3 项/字符
d.set_depth(5)                 # 最多向下遍历 5 层
d.set_str_if_recur("<recur>") # 自定义循环引用的标记；也可用 Ellipsis

root = d.dump(obj)

# 渲染
pf = PlainFormatter()
for line in pf.render(root):
    print(line)
```

示例输出（略去地址信息）：

```
<{title empty} dict>
a = <list @=... __len__=5 __sizeof__=...>
+-- [0] = <int @=... __sizeof__=...> 1
+-- [1] = <int @=... __sizeof__=...> 2
+-- [2] = <int @=... __sizeof__=...> 3
+-- <More 2 items...>
b = <str @=... __len__=7 __sizeof__=...> ABC...(more 4 chars)
c = <dict @=... __len__=2 __sizeof__=...>
+-- x = <int @=... __sizeof__=...> 1
+-- y = <int @=... __sizeof__=...> 2
```

说明：
- 纯文本格式化器打印轻量级树结构。你也可以继承 `Formatter` 实现自定义格式化器。
- 当达到 `head_count` 限制时会出现 "More N items..." 截断提示。

## 概念与数据模型

转储器首先构建由 `Node` 组成的中间树，然后再渲染。

Node 字段：
- key: str — 字段/索引名称（如 dict 的键，或列表索引 "[0]")
- props: dict — 核心描述
  - title: 如对象的类名
  - type: 如 "dict"、"list"、"str"、"int"，或全限定类名
- attrs: dict[str, Any] — 按类型收集的额外属性，例如：
  - "@": 对象 id（十六进制）
  - "__len__": 容器长度
  - "__sizeof__": Python sizeof
  - 异常类型包含 "msg" 字段
- value: Any — 叶子值的字符串表示（如数字、被截断的字符串；当非明细模式时，可能是容器的紧凑摘要）
- children: list[Node] — 子节点

## API

### Dump

位置：`dumpobj._dumpobj.Dump`

作用：遍历对象并生成代表其结构的 `Node` 树。

默认支持的类型：
- dict、list、tuple、set
- str、bool、int、float、complex、None、Ellipsis
- BaseException、type、object（通用兜底）

主要方法与属性：
- set_in_detail(in_detail: bool)：
  - True：为容器/对象构建完整子树
  - False：许多类型仅存储一行摘要到 `value`
- set_head_count(n: int)：限制每个容器/字符串的项目数/字符数；默认 100
- get_head_count() -> int | None
- set_depth(n: int | None)：限制最大递归深度；默认 5；None 表示不限制
- get_depth() -> int | None
- set_str_if_recur(mark: str | Ellipsis | None)：自定义循环引用标记
  - Ellipsis：把节点 key 置为 "..."
  - str：把节点 key 置为该字符串
  - None：在 attrs 中添加 Ref@，指向已见对象 id
- get_str_if_recur() -> str | Ellipsis | None
- register_handle(t: type, handle: Callable[[Node, object, int], Node])：注册/覆盖类型处理器
- dump(obj: object) -> Node：开始一次新的转储并返回根节点

属性收集由内部 `attr_config` 控制。比如容器/字符串会包含 `@`、`__len__`、`__sizeof__`。

循环引用：非值类型会记录对象 id；检测到环时根据 `str_if_recur` 标记。值类型（数字/字符串/字节/布尔）不会记录 id。

深度与截断：
- 深度限制在 `in_detail` 为 True 时控制子节点遍历。
- 项数限制应用于容器；字符串被截断为前 `head_count` 个字符。

注意：当前版本要求 `head_count` 为正整数。

### Node

位置：`dumpobj.node.Node`

访问器：
- set_key/get_key
- set_prop/get_prop；`PropKeys` 为 `"title" | "type"`
- set_attr/set_attrs/get_attr/get_attrs
- set_value/get_value
- append_node/iter_children：用于构建树
- set_parent/get_parent

### Formatter 与 PlainFormatter

- 基类：`dumpobj.formatter.base_formatter.Formatter`
  - 需重写 `_format_key/_format_props/_format_attrs/_format_value/_format_header`
  - 生命周期钩子：`_pre_render/_post_render/_pre_node/_post_node`
  - `render(node)` 以生成器形式懒加载输出
- 纯文本实现：`dumpobj.formatter.plain_formatter.PlainFormatter`
  - 配置：`attr_key_rename` 字典可重命名属性键
  - 缩进：每层 4 空格，使用 `+--` 作为树形前缀

示例：重命名 "@" 属性键：

```python
pf = PlainFormatter()
pf.config["attr_key_rename"] = {"@": "@"}
for line in pf.render(d.dump(obj)):
    print(line)
```

## 自定义类型处理器

可以注册自定义处理器来改变类型的转储方式。处理器接收当前 `Node`、对象和当前深度，应就地修改并返回该节点。

```python
from datetime import datetime
from dumpobj._dumpobj import Dump
from dumpobj.node import Node

d = Dump()

def dump_datetime(node: Node, obj: datetime, depth: int) -> Node:
    node.set_prop("type", "datetime")
    node.set_value(obj.isoformat())
    return node

d.register_handle(datetime, dump_datetime)
```

## 开发

- 需要 Python 3.11+
- 项目元数据见 `pyproject.toml`

快速自检：

```
python - <<"PY"
from dumpobj._dumpobj import Dump
from dumpobj.formatter.plain_formatter import PlainFormatter

obj = {"a": [1,2,3,4], "b": "ABCDEFG"}
d = Dump(); d.set_in_detail(True); d.set_head_count(3)
for line in PlainFormatter().render(d.dump(obj)):
    print(line)
PY
```

## 许可证

MIT License，见 LICENSE。

## 链接

- 代码仓库：https://github.com/Ruilx/dumpobj
- 作者：Ruilx
