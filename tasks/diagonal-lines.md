# diagonal-lines
- category: final-challenge

## Setting

```
|b |b |bD|b |b |
|k |k |k |k |k |
|rD|k |k |k |k |
|k |y |k |k |k |
|k |k |y |k |k |
|k |k |k |y |k |
|k |k |k |k |rD|
|k |k |k |k |k |
|k |k |k |k |k |
|k |rD|k |k |k |
|k |k |y |k |k |
|k |k |k |rD|k |
|k |k |k |k |k |
|k |kS|k |k |k |
```

- length: 9

## Solution

```
while color() != 'b':
    if color() == 'k':
        right()
        if color() == 'r':
            left()
    if color() == 'y':
        left()
        if color() == 'r':
            right()

```
