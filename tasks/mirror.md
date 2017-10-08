# mirror
- category: final-challenge

## Setting

```
|b |b |b |b |b |b |b |
|k |k |kW|kA|kD|k |k |
|k |k |k |kA|k |k |k |
|k |rD|k |kA|k |rD|k |
|k |k |y |kA|y |k |k |
|k |rD|k |kA|k |rD|k |
|k |k |k |kA|k |k |k |
|rD|k |k |kA|k |k |rD|
|k |y |k |kA|k |y |k |
|rD|k |k |kA|k |k |rD|
|k |y |k |kA|k |y |k |
|k |k |y |kA|y |k |k |
|k |k |kS|kA|kW|k |k |
```

- length: 13

## Solution

```
while color() != 'b':
    if color() == 'y':
        if position() < 4:
            left()
        else:
            right()
    if color() == 'r':
        if position() < 4:
            right()
        else:
            left()
    if color() == 'k':
        fly()
```
