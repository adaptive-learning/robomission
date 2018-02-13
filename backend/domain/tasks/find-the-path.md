# find-the-path
- category: repeat

## Setting

```
|b |bA|b |bA|b |
|kM|kM|kA|k |kM|
|kM|k |kA|k |kM|
|k |kA|k |kA|k |
|kA|kM|kM|kA|kA|
|k |k |kM|k |k |
|k |kA|k |kA|k |
|kM|kM|kM|k |kM|
|kA|k |kA|kM|kA|
|k |k |kS|k |k |
```

- length: 4

## Solution

```
repeat 3:
    left()
    shoot()
    right()
```
