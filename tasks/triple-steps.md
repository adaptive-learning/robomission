# triple-steps
- category: if-else

## Setting

```
|b |b |b |b |b |b |
|k |k |k |kD|k |k |
|k |k |kD|k |k |k |
|k |yD|k |k |k |k |
|k |k |kD|k |k |kX|
|k |k |k |kD|kD|k |
|k |k |k |kD|kX|k |
|kW|k |yD|k |k |k |
|k |kD|k |kD|k |k |
|k |k |kD|k |kD|k |
|k |k |k |kS|k |kW|
```

- length: 6

## Solution

```
repeat 5:
    if color() != 'y':
        repeat 3:
            left()
    else:
        repeat 3:
            right()
```
