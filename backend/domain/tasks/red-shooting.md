# red-shooting
- category: if

## Setting

```
|b |b |b |b |b |b |
|kA|kA|kA|kA|kA|kM|
|k |k |kW|k |k |k |
|k |y |k |k |k |r |
|kM|kM|kA|k |y |k |
|k |k |kA|k |k |k |
|k |r |kA|y |k |k |
|y |k |kA|k |k |k |
|kS|k |k |kW|k |k |
```

- length: 6
- energy: 2

## Solution

```
while color() != 'b':
    if color() == 'y':
        right()
    if color() == 'r':
        shoot()
    fly()
```
