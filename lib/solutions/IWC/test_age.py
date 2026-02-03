from solutions.IWC.queue_solution_legacy import Queue
from solutions.IWC.task_types import TaskDispatch, TaskSubmission
from datetime import datetime



def test_age():
    task1 = TaskSubmission(
        user_id=1,
        provider="id_verification",
        timestamp=datetime.strptime('2025-10-20 12:00:00', "%Y-%m-%d %H:%M:%S")
    )
    task2 = TaskSubmission(
        user_id=1,
        provider="bank_statements",
        timestamp=datetime.strptime('2025-10-20 12:05:00', "%Y-%m-%d %H:%M:%S")
    )

    queue = Queue()
    queue.enqueue(task1)
    queue.enqueue(task2)

    assert queue.age == 300

def test_age_with_one_task():
    task1 = TaskSubmission(
        user_id=1,
        provider="id_verification",
        timestamp=datetime.strptime('2025-10-20 12:00:00', "%Y-%m-%d %H:%M:%S")
    )
    queue = Queue()
    queue.enqueue(task1)


    assert queue.age == 0


def test_age_with_no_task():
    queue = Queue()
    assert queue.age == 0

def test_age_as_strings():
    task1 = TaskSubmission(
        user_id=1,
        provider="id_verification",
        timestamp='2025-10-20 12:00:00'
    )
    task2 = TaskSubmission(
        user_id=1,
        provider="bank_statements",
        timestamp='2025-10-20 12:05:00'
    )

    queue = Queue()
    queue.enqueue(task1)
    queue.enqueue(task2)

    assert queue.age == 300
