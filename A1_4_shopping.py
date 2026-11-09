# -*- coding: utf-8 -*-
"""A1-4 简化的网上购物系统 —— 类图对应的 Python 实现。

类图要点：
    Customer 1 —— 0..* Order
    Order    1 ◆—— 1..* OrderDetail       组合
    OrderDetail 0..* —— 1 Product
    Order    1 —— 1..* Payment
    Payment（抽象）◁—— Credit / Cash / WireTransfer / AliPay / WeixinPay
    Order.status : OrderStatus（枚举 CREATE / PAID / SHIPPING / DELIVERED / CANCEL）
"""
from __future__ import annotations

import datetime
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional


class OrderStatus(Enum):
    """订单状态枚举。"""
    CREATE = "CREATE"
    PAID = "PAID"
    SHIPPING = "SHIPPING"
    DELIVERED = "DELIVERED"
    CANCEL = "CANCEL"


class Product:
    """商品项。

    题目只给出 title / weight / description 三个属性，未给出单价；
    为了让 getPriceForQuantity() 可运行，这里用类级价格表补充单价，不改变类图结构。
    """

    _PRICE_TABLE: Dict[str, float] = {}

    def __init__(self, title: str, weight: float, description: str = "") -> None:
        self._title = title
        self._weight = weight
        self._description = description

    @classmethod
    def setPrice(cls, title: str, price: float) -> None:
        cls._PRICE_TABLE[title] = price

    @property
    def title(self) -> str:
        return self._title

    def getPriceForQuantity(self, quantity: int = 1) -> float:
        """按数量计算商品金额。"""
        return self._PRICE_TABLE.get(self._title, 0.0) * quantity

    def getWeight(self) -> float:
        return self._weight

    def __repr__(self) -> str:
        return f"Product({self._title})"


class OrderDetail:
    """订单详情（组合部件，随订单创建与销毁）。"""

    def __init__(self, quantity: int, product: Product) -> None:
        self._quantity = quantity
        self._product = product

    @property
    def quantity(self) -> int:
        return self._quantity

    @property
    def product(self) -> Product:
        return self._product

    def calculateSubTotal(self) -> float:
        """小计金额 = 单价 × 数量。"""
        return self._product.getPriceForQuantity(self._quantity)

    def calculateWeight(self) -> float:
        """小计重量 = 单件重量 × 数量。"""
        return self._product.getWeight() * self._quantity

    def __repr__(self) -> str:
        return f"OrderDetail({self._product.title}×{self._quantity})"


class Payment(ABC):
    """支付方式（抽象类）。"""

    def __init__(self, amount: float) -> None:
        self._amount = amount

    @property
    def amount(self) -> float:
        return self._amount

    @abstractmethod
    def pay(self) -> str:
        """执行支付，返回支付说明。"""


class Credit(Payment):
    """信用卡支付。"""

    def __init__(self, amount: float, number: str, type: str, expire_date: datetime.date) -> None:
        super().__init__(amount)
        self._number = number
        self._type = type
        self._expire_date = expire_date

    def pay(self) -> str:
        return f"信用卡({self._number[-4:].rjust(len(self._number), '*')}, {self._type}) 支付 {self._amount:.2f} 元"


class Cash(Payment):
    """现金支付。"""

    def __init__(self, amount: float, cash_tendered: float) -> None:
        super().__init__(amount)
        self._cash_tendered = cash_tendered

    @property
    def cashTendered(self) -> float:
        return self._cash_tendered

    def pay(self) -> str:
        change = self._cash_tendered - self._amount
        return f"现金支付 {self._amount:.2f} 元，收 {self._cash_tendered:.2f} 元，找零 {change:.2f} 元"


class WireTransfer(Payment):
    """在线转账。"""

    def __init__(self, amount: float, bank_id: str, bank_name: str) -> None:
        super().__init__(amount)
        self._bank_id = bank_id
        self._bank_name = bank_name

    def pay(self) -> str:
        return f"由 {self._bank_name}({self._bank_id}) 转账 {self._amount:.2f} 元"


class AliPay(Payment):
    """支付宝。"""

    def __init__(self, amount: float, number: str) -> None:
        super().__init__(amount)
        self._number = number

    def pay(self) -> str:
        return f"支付宝账号 {self._number} 支付 {self._amount:.2f} 元"


class WeixinPay(Payment):
    """微信支付。"""

    def __init__(self, amount: float, number: str) -> None:
        super().__init__(amount)
        self._number = number

    def pay(self) -> str:
        return f"微信账号 {self._number} 支付 {self._amount:.2f} 元"


class Order:
    """订单。"""

    def __init__(self, create_date: Optional[datetime.date] = None) -> None:
        self._create_date = create_date or datetime.date.today()
        self._status = OrderStatus.CREATE
        self._details: List[OrderDetail] = []   # 组合，1..*
        self._payments: List[Payment] = []      # 1..*

    # ---- 组合端：订单详情由订单创建 ----
    def addItem(self, product: Product, quantity: int) -> OrderDetail:
        detail = OrderDetail(quantity, product)
        self._details.append(detail)
        return detail

    # ---- 支付 ----
    def addPayment(self, payment: Payment) -> None:
        self._payments.append(payment)
        self._status = OrderStatus.PAID

    def ship(self) -> None:
        self._status = OrderStatus.SHIPPING

    def deliver(self) -> None:
        self._status = OrderStatus.DELIVERED

    def cancel(self) -> None:
        self._status = OrderStatus.CANCEL

    @property
    def status(self) -> OrderStatus:
        return self._status

    @property
    def details(self) -> List[OrderDetail]:
        return list(self._details)

    @property
    def payments(self) -> List[Payment]:
        return list(self._payments)

    def __repr__(self) -> str:
        return f"Order({self._create_date}, {self._status.value})"


class Customer:
    """客户。"""

    def __init__(self, name: str, contact: str, delivery_address: str, active: bool = True) -> None:
        self._name = name
        self._contact = contact
        self._delivery_address = delivery_address
        self._active = active
        self._orders: List[Order] = []          # 0..*

    def placeOrder(self, create_date: Optional[datetime.date] = None) -> Order:
        order = Order(create_date)
        self._orders.append(order)
        return order

    @property
    def orders(self) -> List[Order]:
        return list(self._orders)

    def __repr__(self) -> str:
        return f"Customer({self._name})"


def main() -> None:
    print("=== A1-4 网上购物系统 ===")
    Product.setPrice("机械键盘", 399.0)
    Product.setPrice("无线鼠标", 129.0)

    keyboard = Product("机械键盘", 0.9, "87 键热插拔")
    mouse = Product("无线鼠标", 0.12, "2.4G 静音")

    customer = Customer("王小明", "13800000000", "武汉市洪山区大学路 1 号")
    order = customer.placeOrder(datetime.date(2026, 11, 9))
    d1 = order.addItem(keyboard, 1)
    d2 = order.addItem(mouse, 2)

    total = sum(d.calculateSubTotal() for d in order.details)
    weight = sum(d.calculateWeight() for d in order.details)
    print(f"{customer} 下单：{order}")
    for d in order.details:
        print(f"  {d}：小计 {d.calculateSubTotal():.2f} 元，重量 {d.calculateWeight():.2f} kg")
    print(f"合计金额 {total:.2f} 元，总重量 {weight:.2f} kg")

    payments = [
        Credit(total, "6222020200112233", "VISA", datetime.date(2028, 6, 30)),
        Cash(total, 700.0),
        WireTransfer(total, "ICBC001", "中国工商银行"),
        AliPay(total, "wx_abc123"),
        WeixinPay(total, "wx_abc123"),
    ]
    for p in payments:
        print("  " + p.pay())

    order.addPayment(payments[0])
    print(f"支付后订单状态：{order.status.value}")
    order.ship()
    print(f"发货后订单状态：{order.status.value}")
    order.deliver()
    print(f"收货后订单状态：{order.status.value}")


if __name__ == "__main__":
    main()
