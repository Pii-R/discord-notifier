import pytest

from src.tasks.task import Task


def test_check_id_for_task_class():
    class T1(Task):
        def prepare_tasks(self):
            pass

    class T2(Task):
        def prepare_tasks(self):
            pass

    t1 = T1("task1", "first task")
    t2 = T2("task2", "second task")
    with pytest.raises(Exception):
        T1("task1", "first task")

    assert t1.id != t2.id
    assert isinstance(t1.id, int)
    assert isinstance(t2.id, int)
