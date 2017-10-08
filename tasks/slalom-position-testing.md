# slalom-position-testing
- category: comparing

## Setting

```
|b |bD|b |b |b |
|kD|k |k |k |k |
|k |kD|k |k |k |
|kD|k |k |k |k |
|k |kD|k |k |k |
|k |k |kD|k |k |
|k |kD|k |k |k |
|k |k |kD|k |k |
|k |k |k |kS|k |
```

- length: 5

## Solution

```
while color() != 'b':
    left()
    if position() > 1:
        left()
    right()
```
