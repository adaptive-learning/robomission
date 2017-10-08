# two-bit-instructions
- category: final-challenge

## Setting

```
|b |b |b |b |b |b |
|kA|kW|kA|kA|kM|kA|
|kA|kD|kA|kA|kM|kA|
|k |k |yD|k |r |k |
|k |k |y |k |k |yD|
|k |k |k |k |k |y |
|k |rD|k |k |k |k |
|k |y |k |k |r |k |
|k |k |k |k |y |k |
|rD|k |k |k |k |k |
|y |k |k |k |r |k |
|kS|k |k |k |kW|k |
```
- energy: 2
- length: 10

## Solution

```
while color() != 'b':
    if color() == 'y':
        fly()
        if color() == 'y':
            left()
        else:
            right()
    else:
        if color() == 'r':
            shoot()
        else:
            fly()
```
