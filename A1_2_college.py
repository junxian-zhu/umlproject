# -*- coding: utf-8 -*-
"""A1-2 College / Building / Course —— 类图对应的 Python 实现。

类图要点：
    College 1 ◇—— 1..* Building   聚合：建筑构成学院，但建筑可独立存在
    College 1 ◆—— 1..* Course     组合：课程是学院的一部分，学院撤销则课程消亡
    {Course 必须在某个 Building 中进行}  约束注释（附着在 Course 上）
"""
from __future__ import annotations

from typing import List, Optional


class Building:
    """教学楼（可独立于学院存在）。"""

    def __init__(self, code: str, address: str) -> None:
        self._code = code
        self._address = address

    @property
    def code(self) -> str:
        return self._code

    def __repr__(self) -> str:
        return f"Building({self._code})"


class Course:
    """课程（组合部件：生命周期依赖学院）。"""

    def __init__(self, code: str, title: str, credit: float,
                 held_in: Optional["Building"] = None) -> None:
        self._code = code
        self._title = title
        self._credit = credit
        # 约束 {Course 必须在某个 Building 中进行}
        self._held_in = held_in

    @property
    def code(self) -> str:
        return self._code

    @property
    def heldIn(self) -> Optional["Building"]:
        return self._held_in

    def setHeldIn(self, building: "Building") -> None:
        self._held_in = building

    def __repr__(self) -> str:
        return f"Course({self._code}:{self._title})"


class College:
    """学院。"""

    def __init__(self, name: str, code: str) -> None:
        self._name = name
        self._code = code
        self._buildings: List[Building] = []   # 聚合，多重性 1..*
        self._courses: List[Course] = []       # 组合，多重性 1..*

    # ----- 聚合端：建筑由外部创建，学院只持有引用 -----
    def addBuilding(self, building: Building) -> None:
        if building not in self._buildings:
            self._buildings.append(building)

    # ----- 组合端：课程由学院内部创建并负责销毁 -----
    def addCourse(self, code: str, title: str, credit: float, building: Building) -> Course:
        course = Course(code, title, credit, held_in=building)
        self._courses.append(course)
        return course

    def getCourseCount(self) -> int:
        return len(self._courses)

    @property
    def courses(self) -> List[Course]:
        return list(self._courses)

    @property
    def buildings(self) -> List[Building]:
        return list(self._buildings)

    # ----- 约束校验 -----
    def checkConstraints(self) -> None:
        if not self._buildings:
            raise ValueError("约束不满足：学院至少要有 1 栋建筑（1..*）")
        for course in self._courses:
            if course.heldIn is None or course.heldIn not in self._buildings:
                raise ValueError(f"约束不满足：{course} 必须在学院所属的某个 Building 中进行")

    def close(self) -> None:
        """撤销学院：组合端课程随之销毁，聚合端建筑保留。"""
        self._courses.clear()

    def __repr__(self) -> str:
        return f"College({self._name})"


def main() -> None:
    print("=== A1-2 College / Building / Course ===")
    college = College("计算机学院", "CS")
    b1 = Building("A-101", "东校区 1 号楼")
    b2 = Building("B-203", "东校区 2 号楼")
    college.addBuilding(b1)
    college.addBuilding(b2)

    c1 = college.addCourse("CS101", "程序设计基础", 4.0, b1)
    c2 = college.addCourse("CS201", "软件工程", 3.5, b2)
    college.checkConstraints()
    print(f"{college} 课程数：{college.getCourseCount()}，建筑数：{len(college.buildings)}")

    # 约束演示：把课程挂到不属于本学院的建筑上
    outside = Building("X-999", "校外")
    c2.setHeldIn(outside)
    try:
        college.checkConstraints()
    except ValueError as e:
        print("约束检查：", e)
    c2.setHeldIn(b2)

    # 组合 vs 聚合
    college.close()
    print(f"学院撤销后：课程数 {college.getCourseCount()}（组合，随学院销毁），"
          f"建筑仍在 {b1} {b2}（聚合，独立存在）")


if __name__ == "__main__":
    main()
