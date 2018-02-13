# two-color-tracks
- category: final-challenge

## Setting

```
|b |b |b |b |b |b |
|k |kW|k |k |y |k |
|kD|k |k |k |k |kD|
|k |y |k |k |r |k |
|k |y |k |k |y |k |
|k |k |kD|k |k |kD|
|k |r |k |k |r |k |
|k |y |k |k |y |k |
|k |k |kD|kD|k |k |
|k |r |k |k |y |k |
|k |y |k |k |y |k |
|kD|k |k |kD|k |k |
|k |y |k |k |y |k |
|k |y |k |k |y |k |
|k |kS|k |k |kW|k |
```

- length: 10

## Solution

```
repeat 2:
    fly()
    repeat 4:
        fly()
        if color() == 'y':
            left()
            right()
        else:
            right()
            left()
fly()
```
