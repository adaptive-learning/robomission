# triple-slalom
- category: final-challenge

## Setting

```
|b |b |b |b |b |b |
|kW|k |k |k |k |k |
|rD|k |k |k |rD|k |
|k |yD|k |kX|k |yD|
|yD|k |k |rD|yD|k |
|k |yD|k |k |yD|yD|
|yD|k |k |yD|yD|k |
|k |yD|k |k |yD|yD|
|kS|k |k |kW|kX|k |
```

- length: 6

## Solution

```
repeat 3:
    while color() != 'r':
        right()
        left()
    fly()
fly()    
```
