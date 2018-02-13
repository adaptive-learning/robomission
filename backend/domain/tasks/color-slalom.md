# color-slalom
- category: loops

## Setting

```
|b |b |b |b |b |
|k |rD|k |k |k |
|k |k |k |k |k |
|k |k |k |k |k |
|k |k |k |k |yD|
|k |k |k |k |k |
|k |k |k |k |k |
|k |rD|k |k |k |
|k |k |k |k |k |
|k |k |k |yD|k |
|k |k |k |k |k |
|k |k |k |k |k |
|kS|k |k |k |k |
```

- length: 6

## Solution

```
repeat 2:
    while color() != 'y':
        right()
    while color() != 'r':
        left()
fly()
```
