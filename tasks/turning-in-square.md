# turning-in-square
- category: final-challenge

## Setting

```
|b |b |b |b |b |
|kW|k |k |k |kX|
|k |k |k |k |k |
|k |gD|gD|gD|k |
|k |yD|yD|yD|k |
|k |gD|gD|gD|k |
|k |k |k |k |k |
|k |k |k |k |k |
|k |kW|kS|kX|k |
```

- length: 10

## Solution

```
while color() != 'b':
    fly()
    if color() == 'y':
        if position() == 3:
            left()
            left()
        if position() == 2:
            repeat 3:
                right()
```
