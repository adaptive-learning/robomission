# letter-d
- category: final-challenge

## Setting

```
|b |b |b |b |b |b |
|y |yY|yD|rZ|r |r |
|y |yD|y |r |rD|r |
|y |yD|y |r |rD|r |
|y |yD|y |r |r |rD|
|r |rD|r |y |y |yD|
|r |rD|r |y |yD|y |
|r |rD|r |y |yD|y |
|r |rD|rZ|yY|y |y |
|k |kS|k |k |k |k |
```

- length: 6

## Solution

```
while color() != 'b':
    fly()
    if position() > 3:
        if color() == 'y':
            right()
        else:
            left()
```
