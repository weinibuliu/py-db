# python-database

本模块旨在为项目提供一套可重用的，便于拓展的基础设施，包含：

- 数据库交互
- 鉴权函数 (设计中)

## 设计原则

- 使用 SQL ORM
- 下游应当可以便捷的调用
- 尽可能降低侵入程度 减少接入成本

## Python

> 包名为 `db`

### 直接安装

```bash
# 在项目根目录下
pip install -e py-db

# 在子项目中
pip install -e ../py-db

# 或者使用绝对路径
pip install -e /path/to/py-db
```

### 在 requirements.txt 中添加

```bash
# requirements.txt (使用相对于 requirements.txt 文件所在的相对目录)
# ...
-e ../py-db

# bash
pip install -r requirements.txt
```

然后可以 import 使用

```python
import db
# ...
```
