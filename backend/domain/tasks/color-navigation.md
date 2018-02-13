# color-navigation
- category: if-else

## Setting

```
|b |b |b |b |b |
|kD|k |k |kW|k |
|k |yD|k |kD|k |
|k |kD|k |kD|k |
|rD|k |k |k |yD|
|k |yD|k |rD|k |
|k |kD|k |kD|k |
|k |kD|rD|k |k |
|rD|k |kD|k |k |
|kD|k |kD|k |k |
|kW|k |kS|k |k |
```

- length: 6

## Solution

```
while color() != 'b':
    if color() == 'k':
        fly()
    else:
        if color() == 'y':
            left()
        else:
            right()
```
