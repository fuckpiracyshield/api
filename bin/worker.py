from piracyshield_component.config import Config

from piracyshield_service.task.worker import TaskWorkerService

# available tasks list
from piracyshield_service.task.tasks.test import test_task_caller

service = TaskWorkerService()

service.start()
