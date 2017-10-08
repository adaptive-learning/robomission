# edge-to-edge
- category: comparing

## Setting

```
|b |b |b |b |b |
|k |kD|k |k |k |
|k |k |kD|k |k |
|k |k |k |kD|k |
|k |k |k |k |kD|
|k |k |k |kD|k |
|k |kW|kD|k |k |
|k |kD|kD|k |k |
|kD|k |k |kD|k |
|k |kD|k |k |kD|
|k |k |kD|kD|k |
|k |k |kD|kW|k |
|k |kS|k |k |k |
```

- length: 5

## Solution

```
while color() != 'b':
    while position() < 5:
        right()
    while position() > 1:
        left()
```
