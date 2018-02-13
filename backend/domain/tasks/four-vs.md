# four-vs
- category: loops

## Setting

```
|b |b |b |b |b |
|k |kY|kD|k |k |
|k |kX|kD|kD|k |
|k |kW|kD|kD|kD|
|k |k |gD|kD|kD|
|k |k |kD|gD|kD|
|k |kY|kD|kD|gD|
|k |kX|kD|gD|k |
|k |kW|gD|k |k |
|k |kS|k |k |k |
```

- length: 5

## Solution

```
repeat 4:
    repeat 3:
        right()
    repeat 3:
        left()
```
