# yellow-squares
- category: if

## Setting

```
|b |b |b |b |b |
|k |k |yM|yM|k |
|k |k |yM|yD|k |
|k |kW|k |k |k |
|yM|yM|k |yM|yM|
|yM|yD|k |yD|yM|
|k |k |k |kW|k |
|k |yM|yM|k |k |
|k |yD|yM|k |k |
|k |k |k |k |k |
|k |kS|k |k |k |
```
- energy: 4
- length: 4

## Solution

```
while color() != 'b':
    fly()
    if color() == 'y':
        shoot()
```
