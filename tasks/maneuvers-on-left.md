# maneuvers-on-left
- category: comparing

## Setting

```
|bM|bM|b |b |b |
|kM|kZ|k |k |k |
|kM|kM|k |k |k |
|kM|kD|k |k |k |
|kX|kY|kW|kY|kZ|
|kM|kM|k |k |k |
|kD|kM|k |k |k |
|kW|kM|k |k |k |
|kM|kM|kS|kX|k |
```

- length: 6

## Solution

```
while color() != 'b':
    fly()
    if position() <= 2:
        fly()
        shoot()
        fly()
```
