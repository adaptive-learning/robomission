# diamonds-with-signals
- category: if

## Setting

```
|b |b |b |b |bA|
|k |k |k |kD|kA|
|k |k |y |k |kA|
|k |k |k |kA|kA|
|k |k |k |kD|kA|
|k |k |y |k |kA|
|k |k |k |k |kA|
|k |k |k |kA|kA|
|k |k |k |k |kA|
|k |k |k |kD|kA|
|k |k |y |k |kA|
|k |k |kS|k |kA|
```

- length: 5

## Solution

```
while color() != 'b':
    fly()
    if color() == 'y':
        right()
        left()
```
