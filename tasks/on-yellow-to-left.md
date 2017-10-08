# on-yellow-to-left
- category: if

## Setting

```
|b |b |b |b |b |
|k |kA|kA|kA|kA|
|kA|y |k |k |k |
|k |k |k |k |k |
|k |k |k |k |k |
|k |k |kA|kA|kA|
|kA|kA|y |k |k |
|k |k |k |k |k |
|k |k |kS|k |k |
```
- length: 4

## Solution

```python
while color() != 'b':
    fly()
    if color() == 'y':
        left()
```
