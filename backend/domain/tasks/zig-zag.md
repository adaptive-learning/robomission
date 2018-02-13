# zig-zag
- category: while

## Setting

```
|b |b |b |b |b |
|kA|k |kA|k |kA|
|k |kA|k |kA|k |
|kA|k |kA|k |kA|
|k |kA|k |kA|k |
|kA|k |kA|k |kA|
|k |kA|k |kA|k |
|kA|k |kA|k |kA|
|k |k |kS|k |k |
```
- length: 3

## Solution

```python
while color() != 'b':
    right()
    left()
```
