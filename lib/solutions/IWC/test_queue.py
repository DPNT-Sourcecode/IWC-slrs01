from solutions.IWC.queue_solution_legacy import Queue
from solutions.IWC.task_types import TaskDispatch, TaskSubmission
from datetime import datetime

# 1. Enqueue: user_id=1, provider="companies_house",   timestamp='2025-10-20 12:00:00'  -> 1 (queue size)  
# 2. Enqueue: user_id=2, provider="bank_statements",   timestamp='2025-10-20 12:00:00'  -> 2 (queue size)  
# 3. Enqueue: user_id=1, provider="id_verification",   timestamp='2025-10-20 12:00:00'  -> 3 (queue size)  
# 4. Enqueue: user_id=1, provider="bank_statements",   timestamp='2025-10-20 12:00:00'  -> 4 (queue size)

def test_rule_of_three():
    task1 = TaskSubmission(
        user_id=1,
        provider="companies_house",
        timestamp=datetime.strptime('2025-10-20 12:00:00', "%Y-%m-%d %H:%M:%S")
    )

    task2 = TaskSubmission(
        user_id=2,
        provider="companies_house",
        timestamp=datetime.strptime('2025-10-20 12:00:00', "%Y-%m-%d %H:%M:%S")
    )
    task3 = TaskSubmission(
        user_id=1,
        provider="id_verification",
        timestamp=datetime.strptime('2025-10-20 12:00:00', "%Y-%m-%d %H:%M:%S")
    )
    task4 = TaskSubmission(
        user_id=1,
        provider="bank_statements",
        timestamp=datetime.strptime('2025-10-20 12:00:00', "%Y-%m-%d %H:%M:%S")
    )

    queue = Queue()

    queue.enqueue(task1)
    queue.enqueue(task2)
    queue.enqueue(task3)
    queue.enqueue(task4)

    assert queue.dequeue() == TaskDispatch(provider="companies_house", user_id=1)
    assert queue.dequeue() == TaskDispatch(provider="id_verification", user_id=1)
    assert queue.dequeue() == TaskDispatch(provider="bank_statements", user_id=1)
    assert queue.dequeue() == TaskDispatch(provider="companies_house", user_id=2)
