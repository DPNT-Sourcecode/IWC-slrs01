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
    
