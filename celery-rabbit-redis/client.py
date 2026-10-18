import time

from celery.result import AsyncResult

from worker import random_number, app

time.sleep(5)

result_future = random_number.delay(100)
result = AsyncResult(result_future.id, app=app)

print('Submitted task with ID:', result.id)
print('Task state:', result.state)

while True:
    if result.ready():
        print('Task completed with result:', result.get())
        break
    else:
        print('Task state:', result.state)
        time.sleep(1)