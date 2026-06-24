from tools import (
    get_time,
    get_date,
    multiply
)

print(
    "\nTesting Tools\n"
)

print(
    get_time.invoke({})
)

print(
    get_date.invoke({})
)

print(
    multiply.invoke(
        {
            "a": 10,
            "b": 5
        }
    )
)