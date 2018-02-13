# stop-on-red
- category: while

## Setting

```
|b |b |b |b |b |
|k |k |k |k |k |
|k |k |k |k |k |
|k |k |k |k |k |
|kA|kA|kM|kA|kA|
|k |k |rD|k |k |
|k |k |k |k |k |
|k |k |k |k |k |
|k |k |k |k |k |
|k |k |kS|k |k |
```
- energy: 1
- length: 5

## Solution

```
while color() != 'r':
    fly()
shoot()
while color() != 'b':
    fly()
```
