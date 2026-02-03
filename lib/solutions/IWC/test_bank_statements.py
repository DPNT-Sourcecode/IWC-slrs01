from solutions.IWC.queue_solution_legacy import Queue
from solutions.IWC.task_types import TaskDispatch, TaskSubmission
from datetime import datetime



# 1. Enqueue: user_id=1, provider="id_verification", timestamp='2025-10-20 12:00:00' -> 1 (queue size)
# 2. Enqueue: user_id=2, provider="bank_statements", timestamp='2025-10-20 12:01:00' -> 2 (queue size)
# 3. Enqueue: user_id=3, provider="companies_house", timestamp='2025-10-20 12:07:00' -> 3 (queue size)
# 4. Dequeue -> {"user_id": 1, "provider": "id_verification"}
# 5. Dequeue -> {"user_id": 2, "provider": "bank_statements"}
# 6. Dequeue -> {"user_id": 3, "provider": "companies_house"}


def test_time_sesative_bank_statements():
    task1 = TaskSubmission(
        user_id=1,
        provider="id_verification",
        timestamp=datetime.strptime('2025-10-20 12:00:00', "%Y-%m-%d %H:%M:%S")
    )
    task2 = TaskSubmission(
        user_id=2,
        provider="bank_statements",
        timestamp=datetime.strptime('2025-10-20 12:01:00', "%Y-%m-%d %H:%M:%S")
    )
    task3 = TaskSubmission(
        user_id=3,
        provider="companies_house",
        timestamp=datetime.strptime('2025-10-20 12:07:00', "%Y-%m-%d %H:%M:%S")
    )

    queue = Queue()
    queue.enqueue(task1)
    queue.enqueue(task2)
    queue.enqueue(task3)

    assert queue.dequeue() == TaskDispatch(provider="id_verification", user_id=1)
    assert queue.dequeue() == TaskDispatch(provider="bank_statements", user_id=2)
    assert queue.dequeue() == TaskDispatch(provider="companies_house", user_id=3)

def test_time_sesative_bank_statments_with_later():

    task1 = TaskSubmission(
        user_id=1,
        provider="id_verification",
        timestamp=datetime.strptime('2025-10-20 12:00:00', "%Y-%m-%d %H:%M:%S")
    )
    task2 = TaskSubmission(
        user_id=2,
        provider="bank_statements",
        timestamp=datetime.strptime('2025-10-20 12:15:00', "%Y-%m-%d %H:%M:%S")
    )
    task3 = TaskSubmission(
        user_id=2,
        provider="id_verification",
        timestamp=datetime.strptime('2025-10-20 12:02:00', "%Y-%m-%d %H:%M:%S")
    )
    task4 = TaskSubmission(
        user_id=3,
        provider="companies_house",
        timestamp=datetime.strptime('2025-10-20 12:03:00', "%Y-%m-%d %H:%M:%S")
    )

    queue = Queue()
    queue.enqueue(task1)
    queue.enqueue(task2)
    queue.enqueue(task3)

    assert queue.dequeue() == TaskDispatch(provider="id_verification", user_id=1)
    assert queue.dequeue() == TaskDispatch(provider="bank_statements", user_id=2)
    assert queue.dequeue() == TaskDispatch(provider="companies_house", user_id=3)

