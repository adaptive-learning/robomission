# double-track
- category: loops

## Setting

```
|b |b |b |b |b |b |
|kW|kD|k |k |k |k |
|kD|kD|k |k |k |k |
|k |kD|kD|k |k |k |
|k |k |kD|kD|k |k |
|k |k |kD|kD|k |k |
|k |k |kD|kD|k |k |
|k |k |kD|kD|k |k |
|k |k |k |kD|kD|k |
|k |k |k |k |kD|kD|
|k |k |k |k |kD|kD|
|k |k |k |k |kD|kD|
|k |k |k |k |kS|kW|
```

- length: 8

## Solution

```
repeat 2:
    repeat 2:
        repeat 3:
            fly()
        repeat 2:
            left()
    fly()
fly()
```
