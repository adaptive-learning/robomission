# follow-colors
- category: if

## Setting

```
|b |b |b |b |b |
|kA|kA|k |k |k |
|k |y |kA|kA|k |
|k |k |r |kA|kA|
|kA|kA|kA|r |k |
|k |k |y |k |k |
|k |k |kS|k |k |
```

- length: 7

## Solution

```
while color() != 'b':
    if color() == 'k':
        fly()
    if color() == 'y':
        right()
    if color() == 'r':
        left()
```
