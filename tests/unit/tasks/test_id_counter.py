import pytest

from src.tasks.task import Task


def test_check_id_for_task_class():
    class T1(Task):
        pass

    class T2(Task):
        pass

    t1 = T1("task1", "first task")
    t2 = T2("task2", "second task")
    with pytest.raises(Exception):
        T1("task1", "first task")

    assert t1.id != t2.id
