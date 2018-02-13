# diamond-lines
- category: comparing

## Setting

```
|b |b |b |b |bD|
|k |k |k |kD|k |
|k |k |kD|k |k |
|k |k |kD|k |k |
|k |kD|k |k |k |
|kW|k |k |k |kW|
|k |k |k |kD|k |
|k |k |kD|k |k |
|k |k |kD|k |k |
|k |kD|k |k |k |
|kS|k |k |k |k |
```

- length: 4

## Solution

```
while color() != 'b':
    if position() == 3:
        fly()
    right()
```
