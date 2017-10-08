# yellow-is-not-red
- category: while

## Setting

```
|b |b |b |b |b |
|k |k |k |kD|k |
|k |k |k |y |k |
|k |k |kD|k |k |
|k |kD|k |k |k |
|kD|k |k |k |k |
|k |r |k |k |k |
|k |k |r |k |k |
|k |k |k |r |k |
|k |k |k |k |rS|
```

- length: 6

## Solution

```
while color() == 'r':
    left()
while color() != 'y':
    right()
fly()
fly()
```
