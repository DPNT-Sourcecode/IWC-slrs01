from solutions.IWC.queue_solution_legacy import Queue
from solutions.IWC.task_types import TaskDispatch, TaskSubmission
from datetime import datetime


# id = IWC_R5_S7_001, req = enqueue({"provider":"companies_house","timestamp":"2025-10-20 12:00:00","user_id":2}), resp = 1
# id = IWC_R5_S7_002, req = enqueue({"provider":"bank_statements","timestamp":"2025-10-20 12:01:00","user_id":1}), resp = 2
# id = IWC_R5_S7_003, req = enqueue({"provider":"id_verification","timestamp":"2025-10-20 12:02:00","user_id":2}), resp = 3
# id = IWC_R5_S7_004, req = enqueue({"provider":"bank_statements","timestamp":"2025-10-20 12:07:00","user_id":2}), resp = 4
# id = IWC_R5_S7_005, req = enqueue({"provider":"companies_house","timestamp":"2025-10-20 12:08:00","user_id":1}), resp = 5
# id = IWC_R5_S7_006, req = enqueue({"provider":"id_verification","timestamp":"2025-10-20 12:09:00","user_id":1}), resp = 6
# id = IWC_R5_S7_007, req = dequeue(), resp = {"provider":"companies_house","user_id":2}
# id = IWC_R5_S7_008, req = dequeue(), resp = {"provider":"bank_statements","user_id":1}
# id = IWC_R5_S7_009, req = dequeue(), resp = {"provider":"id_verification","user_id":2}
# id = IWC_R5_S7_010, req = dequeue(), resp = {"provider":"companies_house","user_id":1}
# id = IWC_R5_S7_011, req = dequeue(), resp = {"provider":"id_verification","user_id":1}
# id = IWC_R5_S7_012, req = dequeue(), resp = {"provider":"bank_statements","user_id":2}


def test_something():
    task1 = TaskSubmission(
        user_id=2,
        provider="companies_house",
        timestamp='2025-10-20 12:00:00'
    )
    task2 = TaskSubmission(
        user_id=1,
        provider="bank_statements",
        timestamp='2025-10-20 12:01:00'
    )
    task3 = TaskSubmission(
        user_id=2,
        provider="id_verification",
        timestamp='2025-10-20 12:02:00'
    )
    task4 = TaskSubmission(
        user_id=2,
        provider="bank_statements",
        timestamp='2025-10-20 12:07:00'
    )
    task5 = TaskSubmission(
        user_id=1,
        provider="companies_house",
        timestamp='2025-10-20 12:08:00'
    )
    task6 = TaskSubmission(
        user_id=1,
        provider="id_verification",
        timestamp='2025-10-20 12:09:00'
    )


    queue = Queue()
    queue.enqueue(task1)
    queue.enqueue(task2)
    queue.enqueue(task3)
    queue.enqueue(task4)
    queue.enqueue(task5)
    queue.enqueue(task6)

    assert queue.dequeue() == TaskDispatch(provider="companies_house", user_id=2)
    assert queue.dequeue() == TaskDispatch(provider="bank_statements", user_id=1)
    assert queue.dequeue() == TaskDispatch(provider="id_verification", user_id=2)
    assert queue.dequeue() == TaskDispatch(provider="bank_statements", user_id=2)
    assert queue.dequeue() == TaskDispatch(provider="companies_house", user_id=1)
    assert queue.dequeue() == TaskDispatch(provider="id_verification", user_id=1)




def test_bank_first_if_same_timestamp():
    task1 = TaskSubmission(
        user_id=1,
        provider="companies_house",
        timestamp='2025-10-20 12:00:00'
    )
    task2 = TaskSubmission(
        user_id=1,
        provider="bank_statements",
        timestamp='2025-10-20 12:00:00'
    )
    task3 = TaskSubmission(
        user_id=6,
        provider="id_verification",
        timestamp='2025-10-20 12:06:00'
    )

    queue = Queue()
    queue.enqueue(task1)
    queue.enqueue(task2)
    queue.enqueue(task3)

    assert queue.dequeue() == TaskDispatch(provider="bank_statements", user_id=1)
    assert queue.dequeue() == TaskDispatch(provider="companies_house", user_id=1)
    assert queue.dequeue() == TaskDispatch(provider="id_verification", user_id=6)



def test_rule_of_3_with_bank_statement_prio():
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

    assert queue.dequeue() == TaskDispatch(provider="bank_statements", user_id=1)
    assert queue.dequeue() == TaskDispatch(provider="companies_house", user_id=2)
    assert queue.dequeue() == TaskDispatch(provider="id_verification", user_id=2)
    assert queue.dequeue() == TaskDispatch(provider="bank_statements", user_id=2)



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




