from solutions.IWC.queue_solution_legacy import Queue
from solutions.IWC.task_types import TaskDispatch, TaskSubmission
from datetime import datetime


# id = IWC_R5_S6_001, req = enqueue({"provider":"bank_statements","timestamp":"2025-10-20 12:00:00","user_id":1}), resp = 1
# id = IWC_R5_S6_002, req = enqueue({"provider":"companies_house","timestamp":"2025-10-20 12:01:00","user_id":2}), resp = 2
# id = IWC_R5_S6_003, req = enqueue({"provider":"id_verification","timestamp":"2025-10-20 12:06:00","user_id":2}), resp = 3
# id = IWC_R5_S6_004, req = enqueue({"provider":"bank_statements","timestamp":"2025-10-20 12:07:00","user_id":2}), resp = 4

def test_strings():
    task1 = TaskSubmission(
        user_id=1,
        provider="bank_statements",
        timestamp='2025-10-20 12:00:00'
    )
    task2 = TaskSubmission(
        user_id=2,
        provider="companies_house",
        timestamp='2025-10-20 12:01:00'
    )
    task3 = TaskSubmission(
        user_id=2,
        provider="id_verification",
        timestamp='2025-10-20 12:06:00'
    )
    task4 = TaskSubmission(
        user_id=2,
        provider="bank_statements",
        timestamp='2025-10-20 12:07:00'
    )

    queue = Queue()
    queue.enqueue(task1)
    queue.enqueue(task2)
    queue.enqueue(task3)
    queue.enqueue(task4)

    assert queue.dequeue() == TaskDispatch(provider="companies_house", user_id=1)
    assert queue.dequeue() == TaskDispatch(provider="credit_check", user_id=1)
    assert queue.dequeue() == TaskDispatch(provider="bank_statements", user_id=1)
    assert queue.dequeue() == TaskDispatch(provider="id_verification", user_id=1)



def test_seond_oldest_bank_with_credit_check():
    task1 = TaskSubmission(
        user_id=1,
        provider="companies_house",
        timestamp=datetime.strptime('2025-10-20 12:07:00', "%Y-%m-%d %H:%M:%S")
    )
    task2 = TaskSubmission(
        user_id=1,
        provider="id_verification",
        timestamp=datetime.strptime('2025-10-20 12:07:00', "%Y-%m-%d %H:%M:%S")
    )
    task3 = TaskSubmission(
        user_id=1,
        provider="bank_statements",
        timestamp=datetime.strptime('2025-10-20 12:01:00', "%Y-%m-%d %H:%M:%S")
    )
    task4 = TaskSubmission(
        user_id=1,
        provider="credit_check",
        timestamp=datetime.strptime('2025-10-20 12:00:00', "%Y-%m-%d %H:%M:%S")
    )

    queue = Queue()
    queue.enqueue(task1)
    queue.enqueue(task2)
    queue.enqueue(task3)
    queue.enqueue(task4)

    assert queue.dequeue() == TaskDispatch(provider="companies_house", user_id=1)
    assert queue.dequeue() == TaskDispatch(provider="credit_check", user_id=1)
    assert queue.dequeue() == TaskDispatch(provider="bank_statements", user_id=1)
    assert queue.dequeue() == TaskDispatch(provider="id_verification", user_id=1)



def test_bank_second_oldest():
    task1 = TaskSubmission(
        user_id=1,
        provider="companies_house",
        timestamp=datetime.strptime('2025-10-20 12:07:00', "%Y-%m-%d %H:%M:%S")
    )
    task2 = TaskSubmission(
        user_id=1,
        provider="bank_statements",
        timestamp=datetime.strptime('2025-10-20 12:01:00', "%Y-%m-%d %H:%M:%S")
    )
    task3 = TaskSubmission(
        user_id=2,
        provider="companies_house",
        timestamp=datetime.strptime('2025-10-20 12:00:00', "%Y-%m-%d %H:%M:%S")
    )

    queue = Queue()
    queue.enqueue(task1)
    queue.enqueue(task2)
    queue.enqueue(task3)

    assert queue.dequeue() == TaskDispatch(provider="companies_house", user_id=2)
    assert queue.dequeue() == TaskDispatch(provider="bank_statements", user_id=1)
    assert queue.dequeue() == TaskDispatch(provider="companies_house", user_id=1)


def test_bank_is_oldest():
    task1 = TaskSubmission(
        user_id=1,
        provider="bank_statements",
        timestamp=datetime.strptime('2025-10-20 12:00:00', "%Y-%m-%d %H:%M:%S")
    )
    task2 = TaskSubmission(
        user_id=1,
        provider="companies_house",
        timestamp=datetime.strptime('2025-10-20 12:01:00', "%Y-%m-%d %H:%M:%S")
    )
    task3 = TaskSubmission(
        user_id=1,
        provider="id_verification",
        timestamp=datetime.strptime('2025-10-20 12:07:00', "%Y-%m-%d %H:%M:%S")
    )

    queue = Queue()
    queue.enqueue(task1)
    queue.enqueue(task2)
    queue.enqueue(task3)

    assert queue.dequeue() == TaskDispatch(provider="bank_statements", user_id=1)
    assert queue.dequeue() == TaskDispatch(provider="companies_house", user_id=1)
    assert queue.dequeue() == TaskDispatch(provider="id_verification", user_id=1)




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
    queue.enqueue(task4)

    assert queue.dequeue() == TaskDispatch(provider="id_verification", user_id=1)
    assert queue.dequeue() == TaskDispatch(provider="id_verification", user_id=2)
    assert queue.dequeue() == TaskDispatch(provider="companies_house", user_id=3)
    assert queue.dequeue() == TaskDispatch(provider="bank_statements", user_id=2)



