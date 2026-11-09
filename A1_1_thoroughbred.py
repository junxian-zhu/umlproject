# -*- coding: utf-8 -*-
"""A1-1 Thoroughbred（优良品质的马）—— 类图对应的 Python 实现。

类图要点：
    Thoroughbred
    - mother : Thoroughbred      # 私有
    - father : Thoroughbred      # 私有
    - birthYear : int            # 私有
    + getCurrentAge() : int
    + getFather() : Thoroughbred
    + getMother() : Thoroughbred

两条自关联：mother 0..1 —— 0..*，father 0..1 —— 0..*。
即一匹马至多有一个母亲、一个父亲，而一匹马可以是多匹马的父/母。
"""
from __future__ import annotations

import datetime
from typing import List, Optional


class Thoroughbred:
    """优良品质的马。"""

    def __init__(self, name: str, birth_year: int,
                 father: Optional["Thoroughbred"] = None,
                 mother: Optional["Thoroughbred"] = None) -> None:
        self._name = name
        # 三个属性都是私有的（类图中以 - 表示），Python 用下划线前缀表达封装意图
        self.__mother: Optional[Thoroughbred] = None
        self.__father: Optional[Thoroughbred] = None
        self.__birth_year = birth_year
        # 自关联 1 : 0..* 的“多”端：作为父/母登记的后代
        self.__offspring: List[Thoroughbred] = []

        # 通过 setter 建立关联，保证双向一致
        if father is not None:
            self.setFather(father)
        if mother is not None:
            self.setMother(mother)

    # ---------- 图中给出的三个操作 ----------
    def getCurrentAge(self) -> int:
        """按出生年份计算当前年龄（周岁）。"""
        return datetime.date.today().year - self.__birth_year

    def getFather(self) -> Optional["Thoroughbred"]:
        return self.__father

    def getMother(self) -> Optional["Thoroughbred"]:
        return self.__mother

    # ---------- 维护自关联的操作（图中未列出，属于实现细节） ----------
    def setFather(self, father: "Thoroughbred") -> None:
        self.__father = father
        father.__offspring.append(self)      # 多重性 0..*：父马可有多匹后代

    def setMother(self, mother: "Thoroughbred") -> None:
        self.__mother = mother
        mother.__offspring.append(self)

    @property
    def offspring(self) -> List["Thoroughbred"]:
        return list(self.__offspring)

    @property
    def name(self) -> str:
        return self._name

    @property
    def birthYear(self) -> int:
        return self.__birth_year

    def __repr__(self) -> str:
        return f"Thoroughbred({self._name}, {self.__birth_year})"


def main() -> None:
    stallion = Thoroughbred("闪电", 2015)      # 公马
    mare = Thoroughbred("流星", 2016)          # 母马
    foal = Thoroughbred("小星", 2021, father=stallion, mother=mare)

    print("=== A1-1 Thoroughbred ===")
    print(f"{foal.name} 的父亲：{foal.getFather().name}，母亲：{foal.getMother().name}")
    print(f"{foal.name} 当前年龄：{foal.getCurrentAge()} 岁")
    print(f"{stallion.name} 的后代数：{len(stallion.offspring)}（多重性 0..*）")
    print(f"无父母记录的马：{Thoroughbred('野马', 2020).getFather()}（多重性 0..1 允许为空）")


if __name__ == "__main__":
    main()
