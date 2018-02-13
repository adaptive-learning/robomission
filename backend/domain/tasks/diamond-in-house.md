# diamond-in-house
- category: while

## Setting

```
|b |b |bA|b |b |
|k |kA|y |kA|k |
|kA|y |y |y |kA|
|y |yA|yA|yA|y |
|k |kA|kX|kA|k |
|kW|kA|kD|kA|kX|
|k |kA|kW|kA|k |
|k |kA|kA|kA|k |
|g |g |g |g |g |
|g |g |g |g |g |
|g |g |g |gS|g |
```

## Solution

```
while color() == 'g':
    left()
while color() != 'y':
    fly()
while color() != 'b':
    left()
```
