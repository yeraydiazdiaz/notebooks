"""
Differences between asyncio's wait and gather.

Gather returns the **ordered results** of the tasks, and by default
raises any exceptions that occur after all coroutines complete. If
`return_exceptions` is set to True the result of the failing coroutine
is the exception object and can be reraised.

Wait returns **unordered Task objects**, exceptions are not reraised and
are left to the caller to deal with upon calling `result()`. Wait return
a tuple of completed, pending Task objects and accepts kwargs to define
when it should return.

"""

import asyncio
import concurrent
from random import random
from itertools import chain


async def coro(i):
    sleep_time = random() * 3
    print("Coro with {}, sleeping for {:.2f} seconds".format(i, sleep_time))
    await asyncio.sleep(sleep_time)
    if i == 5 or i == 7:
        raise Exception("Exception on i = {}".format(i))
    return i

# Wait variations


async def wait():
    tasks = [coro(i) for i in range(10)]
    completed, pending = await asyncio.wait(tasks)
    print("Completed size: {}, pending size {}".format(
        len(completed), len(pending)))
    for task in chain(completed, pending):
        try:
            print(task.result())
        except Exception as e:
            print(e)


async def wait_first_exception():
    tasks = [coro(i) for i in range(10)]
    completed, pending = await asyncio.wait(
        tasks, return_when=concurrent.futures.FIRST_EXCEPTION)
    print("Completed size: {}, pending size {}".format(
        len(completed), len(pending)))
    for task in completed:
        try:
            print(task.result())
        except Exception as e:
            print(e)
    for task in pending:
        task.cancel()


async def wait_first_completed():
    tasks = [coro(i) for i in range(10)]
    completed, pending = await asyncio.wait(
        tasks, return_when=concurrent.futures.FIRST_COMPLETED)
    print("Completed size: {}, pending size {}".format(
        len(completed), len(pending)))
    for task in completed:
        try:
            print(task.result())
        except Exception as e:
            print(e)
    for task in pending:
        task.cancel()

# Gather


async def gather(return_exceptions=False):
    tasks = [coro(i) for i in range(10)]
    completed = await asyncio.gather(
        *tasks, return_exceptions=return_exceptions)
    print("Tasks complete")
    print(completed)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    print(">>> Wait")
    loop.run_until_complete(wait())

    print("\n>>> Wait first completed")
    loop.run_until_complete(wait_first_completed())

    print("\n>>> Wait first exception")
    loop.run_until_complete(wait_first_exception())

    print("\n>>> Gather with Return exceptions set to True")
    loop.run_until_complete(gather(return_exceptions=True))

    print("\n>>> Gather")
    loop.run_until_complete(gather())
    loop.close()
