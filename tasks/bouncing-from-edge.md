# bouncing-from-edge
- category: if-else

## Setting

```
|b |b |bD|b |b |
|k |k |k |kD|k |
|k |k |k |k |kD|
|k |k |k |kD|k |
|k |k |k |k |kD|
|k |k |k |kD|k |
|k |k |k |k |kD|
|k |k |k |kD|k |
|k |k |kD|k |k |
|k |kS|k |k |k |
```

- length: 5

## Solution

```
repeat 8:
    if position() == 5:
        left()
    else:
        right()
left()
```
