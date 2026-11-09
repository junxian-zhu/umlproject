# 软件工程实验三：面向对象的系统建模 A

UML 类图建模 + Python 实现，共四道题（A1-1 ~ A1-4）。

## 目录结构

```
.
├── diagrams/            # 类图（SVG 源文件 + PNG 插图，2 倍分辨率）
├── src/                 # 四道题的 Python 实现
│   ├── A1_1_thoroughbred.py
│   ├── A1_2_college.py
│   ├── A1_3_school.py
│   └── A1_4_shopping.py
├── tools/               # 类图生成脚本（SVG → PNG）
└── 实验报告.docx
```

## 运行环境

- Python 3.8+（仅用标准库，无第三方依赖）
- 直接运行即可，无需安装：

```bash
python src/A1_1_thoroughbred.py
python src/A1_2_college.py
python src/A1_3_school.py
python src/A1_4_shopping.py
```

## 题目与实现对应关系

| 题号 | 建模内容 | 关键 UML 要素 | 实现文件 |
| --- | --- | --- | --- |
| A1-1 | 优良品质的马 Thoroughbred | 类、私有属性、公有操作、两条自关联（0..1 / 0..*） | `A1_1_thoroughbred.py` |
| A1-2 | College / Building / Course | 聚合、组合、约束注释 | `A1_2_college.py` |
| A1-3 | School / Department / Instructor / Subject / Student | 五类之间的关联与多重性（1..*、1..3、1..5） | `A1_3_school.py` |
| A1-4 | 简化的网上购物系统 | 组合、抽象类与泛化、枚举、多重性 | `A1_4_shopping.py` |

## 代码与模型的对应说明

- **可见性**：类图中的 `-`（私有）用 Python 的双下划线属性实现，`+`（公有）用普通方法实现，`#`（受保护）用单下划线属性实现。
- **多重性**：`1..3`、`1..5` 这类上界约束在 `addXxx()` / `teach()` / `enroll()` 方法中做校验，越界抛 `ValueError`。
- **聚合与组合**：聚合端（College—Building）由外部创建对象后传入引用；组合端（College—Course、Order—OrderDetail）由整体对象内部创建，整体销毁时部件随之消失。
- **抽象类与泛化**：`Payment` 用 `abc.ABC` + `@abstractmethod` 实现，五个子类分别实现 `pay()`。
- **枚举**：`OrderStatus` 用 `enum.Enum` 实现 CREATE / PAID / SHIPPING / DELIVERED / CANCEL 五个取值。
- **说明**：A1-4 的 `Product` 题目未给出单价，为让 `getPriceForQuantity()` 可运行，实现中用类级价格表 `_PRICE_TABLE` 补充单价，不改变类图结构。

## 重新生成类图

`diagrams/` 下的图由 `tools/` 中的脚本生成（纯 SVG 手绘 + Edge 无头浏览器渲染）：

```bash
bash tools/render.sh
```
