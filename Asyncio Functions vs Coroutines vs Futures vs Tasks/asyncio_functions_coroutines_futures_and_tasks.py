import asyncio


def callback(f):
    print("Callback: {}".format(f.result()))


async def coro():
    print("Executing coroutine")
    await asyncio.sleep(0.25)
    return "Done executing coroutine"

loop = asyncio.get_event_loop()

print("# Functions vs Coroutines vs Futures vs Tasks\n")
print("> Coroutines are just functions:")
print("{} vs. {}".format(type(callback), type(coro)))

print("> Invoking a coroutine produces a coroutine object")
coroutine = coro()
print(coroutine)

print("> `ensure_future` schedules the coroutine object and wraps it in a `Task`, a subclass of `Future`")
task = asyncio.ensure_future(coroutine)
print(task)

print("> You can add callbacks to Task objects")
task.add_done_callback(callback)

print("> `ioloop.run_until_complete` will start the loop and run the task, closing the loop when it's done")
print("Returned value is: " + loop.run_until_complete(task))

print("> Notice the callback was invoked first")
