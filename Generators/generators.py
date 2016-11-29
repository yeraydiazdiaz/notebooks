"""
What are generators?

"""

print("# Standard generator")


def generator():
    for i in range(2):
        yield i
    print("Generator done! Raising StopIteration")


my_gen = generator()
print(next(my_gen))
print(next(my_gen))
try:
    print(next(my_gen))
except StopIteration as e:
    print("Caught StopIteration, loops do this automatically: {}".format(e))


print("\n# Generator with input using send, requires `next` and `gen.send`")


def generator_with_input():
    i = yield
    for j in range(5):
        yield i * j
    print("Generator done! Raising StopIteration")


my_gen = generator_with_input()
next(my_gen)
my_gen.send(3)
print("For loop interating on the generator, should not raise StopIteration")
for i in my_gen:
    print(i)


print("\n# Generator yielding from another generator")


def parent_generator():
    yield from generator()
    for i in range(2, 4):
        yield i


my_gen = parent_generator()
print("For loop interating on the generator")
print("Yields all results from `generator` first and then its own results")
for i in my_gen:
    print(i)
