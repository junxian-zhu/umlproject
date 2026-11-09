# -*- coding: utf-8 -*-
"""A1-3 School / Department / Instructor / Subject / Student —— 类图对应的 Python 实现。

类图要点（含多重性）：
    School  1 —— 1..*  Department    学院由 1 到多个系构成
    Department 1..* —— 1..*  Instructor  每个系至少 1 位教师，每位教师至少属于 1 个系
    Department 1 —— 1..*  Subject    每个系提供至少 1 门课程
    Instructor 1..* —— 1..3  Subject 每位教师教授 1~3 门课程
    School  1 —— 0..*  Student       学院拥有 0 到多名学生
    Student 1..5 —— 1..*  Subject    学生参加 1~5 门课程
"""
from __future__ import annotations

from typing import List


class Subject:
    """课程。"""

    def __init__(self, name: str, credit: float) -> None:
        self._name = name
        self._credit = credit
        self._instructors: List["Instructor"] = []

    @property
    def name(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return f"Subject({self._name})"


class Instructor:
    """指导教师。"""

    def __init__(self, name: str, title: str) -> None:
        self._name = name
        self._title = title
        self._departments: List["Department"] = []
        self._subjects: List[Subject] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def subjects(self) -> List[Subject]:
        return list(self._subjects)

    def teach(self, subject: Subject) -> None:
        """建立“教授”关联，并校验 1..3 的多重性。"""
        if subject in self._subjects:
            return
        if len(self._subjects) >= 3:
            raise ValueError(f"{self._name} 最多教授 3 门课程（多重性 1..3）")
        self._subjects.append(subject)
        subject._instructors.append(self)

    def join(self, department: "Department") -> None:
        if department not in self._departments:
            self._departments.append(department)

    def __repr__(self) -> str:
        return f"Instructor({self._name})"


class Student:
    """学生。"""

    def __init__(self, name: str, student_no: str) -> None:
        self._name = name
        self._student_no = student_no
        self._subjects: List[Subject] = []

    def enroll(self, subject: Subject) -> None:
        """选课，并校验 1..5 的多重性。"""
        if subject in self._subjects:
            return
        if len(self._subjects) >= 5:
            raise ValueError(f"{self._name} 最多选修 5 门课程（多重性 1..5）")
        self._subjects.append(subject)

    def __repr__(self) -> str:
        return f"Student({self._name})"


class Department:
    """系。"""

    def __init__(self, name: str, dept_no: str) -> None:
        self._name = name
        self._dept_no = dept_no
        self._instructors: List[Instructor] = []
        self._subjects: List[Subject] = []

    def addInstructor(self, instructor: Instructor) -> None:
        if instructor not in self._instructors:
            self._instructors.append(instructor)
            instructor.join(self)

    def addSubject(self, subject: Subject) -> None:
        if subject not in self._subjects:
            self._subjects.append(subject)

    @property
    def name(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return f"Department({self._name})"


class School:
    """学院。"""

    def __init__(self, name: str) -> None:
        self._name = name
        self._departments: List[Department] = []
        self._students: List[Student] = []

    def addDepartment(self, department: Department) -> None:
        if department not in self._departments:
            self._departments.append(department)

    def addStudent(self, student: Student) -> None:
        self._students.append(student)

    def checkConstraints(self) -> None:
        if not (1 <= len(self._departments)):
            raise ValueError("学院至少要有 1 个系（1..*）")
        for d in self._departments:
            if len(d._instructors) < 1:
                raise ValueError(f"{d} 至少要有 1 位指导教师（1..*）")
            if len(d._subjects) < 1:
                raise ValueError(f"{d} 至少要有 1 门课程（1..*）")
            for i in d._instructors:
                if len(i._departments) < 1:
                    raise ValueError(f"{i} 至少属于 1 个系（1..*）")

    def __repr__(self) -> str:
        return f"School({self._name})"


def main() -> None:
    print("=== A1-3 School / Department / Instructor / Subject ===")
    school = School("信息工程学院")

    cs = Department("计算机系", "D01")
    se = Department("软件工程系", "D02")
    school.addDepartment(cs)
    school.addDepartment(se)

    s1 = Subject("数据结构", 4.0)
    s2 = Subject("操作系统", 4.0)
    s3 = Subject("软件工程", 3.5)
    s4 = Subject("编译原理", 3.0)
    for sub in (s1, s2):
        cs.addSubject(sub)
    for sub in (s3, s4):
        se.addSubject(sub)

    zhang = Instructor("张老师", "教授")
    li = Instructor("李老师", "副教授")
    cs.addInstructor(zhang)
    se.addInstructor(li)

    zhang.teach(s1)
    zhang.teach(s3)
    li.teach(s3)
    li.teach(s4)

    stu = Student("王小明", "2023001")
    school.addStudent(stu)
    for sub in (s1, s3, s4):
        stu.enroll(sub)

    school.checkConstraints()
    print(f"{school} 系数量：{len(school._departments)}")
    print(f"{zhang} 教授课程：{[s.name for s in zhang.subjects]}（1..3）")
    print(f"{stu} 选修课程：{[s.name for s in stu._subjects]}（1..5）")

    # 多重性上界演示
    try:
        zhang.teach(s2)
        zhang.teach(s4)
        zhang.teach(Subject("超出上限", 1.0))
    except ValueError as e:
        print("多重性校验：", e)


if __name__ == "__main__":
    main()
