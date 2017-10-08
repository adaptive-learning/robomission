# cross-2
- category: final-challenge

## Setting

```
|b |b |b |b |b |
|kD|k |k |k |kW|
|k |kA|kA|kA|k |
|k |kD|k |kD|k |
|k |k |k |k |k |
|k |k |kD|k |k |
|k |k |k |k |k |
|k |kD|k |kD|k |
|k |kA|kA|kA|k |
|kS|k |k |k |kW|
```

- length: 11

## Solution

```
repeat 5:
    if position() != 4:
        fly()
    if position() != 5:
        right()
repeat 5:
    if position() != 2:
        fly()
    if position() != 1:
        left()
fly()
```
