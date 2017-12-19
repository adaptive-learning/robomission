# letter-e
- category: if-else

## Setting

```
|b |b |b |b |b |
|kD|k |k |k |k |
|kY|kD|k |k |k |
|kD|k |kD|k |k |
|kD|k |k |kY|k |
|kZ|kD|k |k |k |
|kD|k |kD|k |k |
|kD|k |k |kZ|k |
|k |kD|k |k |k |
|k |k |kD|k |k |
|k |k |k |kS|k |
```

- length: 4

## Solution

```
while color() != 'b':
    if position() == 1:
        fly()
    else:
        left()
```
