# edge-wormholes
- category: final-challenge

## Setting

```
|b |b |b |b |b |b |
|k |kD|k |k |k |kZ|
|kX|k |kD|k |kD|k |
|kY|kD|k |kD|k |k |
|k |kD|kD|k |kD|kW|
|k |kD|kD|kD|kD|kZ|
|kY|k |k |kD|kD|k |
|k |k |kD|k |kD|kW|
|k |kD|k |k |k |kX|
|kS|k |k |k |k |k |
```

- length: 6

## Solution

```
repeat 5:
    if position() == 1:
        repeat 5:   
            right()
    else:
        repeat 5:
            left()
```
