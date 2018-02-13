# chessboard
- category: comparing

## Setting

```
|bY|b |b |b |b |
|kD|k |kD|k |k |
|kX|kD|k |kD|k |
|kD|k |kD|k |kY|
|kW|kD|k |kD|k |
|kD|k |kD|k |kX|
|k |kD|k |kD|k |
|k |k |kS|k |kW|
```

- length: 4

## Solution

```
while color() != 'b':
    left()
    if position() == 1:
        fly()
```
