from celery import Celery


@task(name="sum_two_numbers")
def add(x, y):
    return x + y
