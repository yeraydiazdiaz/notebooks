"""
Cooperative coroutines, when exactly do we yield to the event loop?

I was under the impression that every `await` yields control back to
the event loop. That is not the case.

Awaiting your own coroutines does *not* yield to the loop, but awaiting
`asyncio.sleep` and other libraries does. Why are they special?

From https://snarky.ca/how-the-heck-does-async-await-work-in-python-3-5/

"One very key point I want to make about the difference between a
generator-based coroutine and an async one is that only generator-based
coroutines can actually pause execution and force something to be sent down
to the event loop"

"""


import asyncio


async def foo():
    print('Executing foo, sleeping...')
    await asyncio.sleep(0)
    print('...foo back from sleeping')
    return 1


async def bar():
    print('Executing bar')
    print('>> bar calling baz, I expected a context switch to foo, instead...')
    baz_result = await baz()
    print('<< bar back from calling baz')
    return baz_result


async def baz():
    print('>>> Executing baz, sleeping, the context switch to foo happens now?')
    await asyncio.sleep(0)
    print('<<< ...baz back from sleeping')
    return 2


async def bar_():
    print('Executing bar_')
    print('>> bar_ calling baz_, I expected a context switch to foo, and indeed...')
    baz_result = await baz_()
    print('<< bar_ back from calling baz_')
    return baz_result


@asyncio.coroutine
def baz_():
    yield  # yields control to the event loop, there's no equivalent for await
    print('>>> Executing baz, sleeping...')
    yield from asyncio.sleep(0)
    print('<<< ...baz back from sleeping')
    return 2


loop = asyncio.get_event_loop()
# group the tasks into a single task to schedule
grouped_task = asyncio.gather(foo(), bar())

results = loop.run_until_complete(grouped_task)
print("The results are: {}".format(results), end='\n\n')

# group the tasks into a single task to schedule
grouped_task = asyncio.gather(foo(), bar_())

results = loop.run_until_complete(grouped_task)
print("The results are: {}".format(results))

