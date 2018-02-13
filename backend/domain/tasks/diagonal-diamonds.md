# diagonal-diamonds
- category: final-challenge

## Setting

```
|b |b |b |b |b |b |
|k |k |k |yD|k |k |
|k |k |k |kW|yD|k |
|k |k |yD|k |k |yD|
|k |yD|k |k |k |k |
|yD|k |k |k |k |k |
|kS|k |k |k |k |kW|
```

- length: 6

## Solution

```
while color() != 'b':
    if color() == 'y':
        if position() < 4:
            right()
        else:
            left()
    else:
        fly()
```
