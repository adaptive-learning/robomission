# two-diamonds
- category: if

## Setting

```
|b |b |b |b |
|kA|kA|k |kA|
|kW|k |k |k |
|k |k |k |k |
|kD|k |kD|k |
|kM|y |kM|y |
|k |k |k |k |
|k |k |k |k |
|k |k |k |kW|
|k |k |k |k |
|k |kS|k |k |
```

- length: 4

## Solution

```
while color() != 'b':
    fly()
    if color() == 'y':
        left()
```
