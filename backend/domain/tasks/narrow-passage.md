# narrow-passage
- category: if-else

## Setting

```
|b |b |b |b |b |
|kA|kA|kA|kA|k |
|k |k |k |k |k |
|k |k |k |k |k |
|k |k |k |k |k |
|kA|kA|kA|kA|k |
|k |k |k |k |kW|
|k |k |k |k |k |
|k |kW|k |k |k |
|kA|kA|kA|kA|k |
|k |k |k |k |k |
|k |k |k |k |k |
|k |k |k |k |k |
|kS|k |k |k |k |
```

- length: 4

## Solution

```
while color() != 'b':
    if position() < 5:
        right()
    else:
        fly()
```
