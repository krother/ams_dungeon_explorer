"""
Write a program that produces numbers from the Fibonacci series.

In the Fibonacci series, each number is the sum of the two preceding ones. The first numbers of the series are:

0, 1, 1, 2, 3, 5, 8, 13, 21, 34
"""

def fibonacci(limit:int) -> int:
    numbers = [0, 1]
    n = 1 
    while len(numbers) <= limit:
        n += 1 
        new = numbers[n - 1] + numbers[n - 2]
        numbers.append(new)
        print(numbers)
    return numbers[-1]


def fibonacci(limit:int) -> int:
    a, b = 0, 1
    for i in range(limit - 1):
        a, b = b, a + b
    return b


def _fibonacci(limit:int) -> int:
    """recursive implementation. Correct, but SLOW"""
    if limit < 2:
        return limit
    return fibonacci(limit - 1) + fibonacci(limit - 2)  # recursive function



text=input("enter number...")
print(fibonacci(limit=int(text)))
