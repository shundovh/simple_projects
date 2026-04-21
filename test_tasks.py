import os
import pytest
from tasks import add_task, list_tasks, complete_task, delete_task, load_tasks, DATA_FILE


@pytest.fixture(autouse=True)
def clean_data_file():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    yield
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)


def test_add_task():
    add_task("Buy groceries")
    tasks = load_tasks()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Buy groceries"
    assert tasks[0]["done"] is False


def test_list_tasks_empty(capsys):
    list_tasks()
    captured = capsys.readouterr()
    assert "No tasks found" in captured.out


def test_list_tasks_shows_pending(capsys):
    add_task("Write tests")
    list_tasks()
    captured = capsys.readouterr()
    assert "Write tests" in captured.out


def test_complete_task():
    add_task("Read a book")
    complete_task(1)
    tasks = load_tasks()
    assert tasks[0]["done"] is True


def test_complete_task_not_found(capsys):
    complete_task(99)
    captured = capsys.readouterr()
    assert "not found" in captured.out


def test_delete_task():
    add_task("Clean room")
    delete_task(1)
    tasks = load_tasks()
    assert len(tasks) == 0


def test_delete_task_not_found(capsys):
    delete_task(99)
    captured = capsys.readouterr()
    assert "not found" in captured.out


def test_list_all_includes_completed(capsys):
    add_task("Done task")
    complete_task(1)
    list_tasks(show_all=True)
    captured = capsys.readouterr()
    assert "Done task" in captured.out


def test_list_hides_completed_by_default(capsys):
    add_task("Done task")
    complete_task(1)
    capsys.readouterr()  # discard setup output
    list_tasks(show_all=False)
    captured = capsys.readouterr()
    assert "Done task" not in captured.out
