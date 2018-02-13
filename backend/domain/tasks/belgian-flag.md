# belgian-flag
- category: if

## Setting

```
|b |b |b |b |b |b |
|kY|kA|kW|kA|kA|k |
|kD|k |y |yD|rD|r |
|kD|k |yD|y |r |rD|
|kD|k |y |yD|rD|r |
|kD|k |yD|y |r |rD|
|kW|kA|k |kA|kA|kY|
|k |k |kS|k |k |k |
```

- length: 9

## Solution

```
while color() != 'b':
    if color() == 'k':
        fly()
    if color() == 'y':
        right()
        left()
    if color() == 'r':
        left()
        right()
```
