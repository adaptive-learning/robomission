# wave
- category: comparing

## Setting

```
|b |bD|b |b |b |
|k |yD|k |k |k |
|k |k |yD|k |k |
|k |k |k |yD|k |
|k |k |k |yD|k |
|k |k |yD|k |k |
|k |yD|k |k |k |
|k |yD|k |k |k |
|k |k |yD|k |k |
|k |k |k |yD|k |
|k |k |k |yD|k |
|k |k |yS|k |k |
```

- length: 7

## Solution

```
repeat 2:
    while position() < 4:
        right()
    fly()
    while position() > 2:
        left()
    fly()
```
