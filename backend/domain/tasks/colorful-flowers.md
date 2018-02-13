# colorful-flowers
- category: if-else

## Setting

```
|b |b |b |b |b |b |
|k |kW|k |k |k |k |
|k |yD|k |k |k |k |
|rD|k |r |k |k |k |
|k |gD|k |k |yD|k |
|k |k |k |g |k |gD|
|k |yD|k |k |rD|k |
|rD|k |y |k |k |k |
|k |gD|k |k |kW|k |
|k |kS|k |k |k |k |
```

- length: 6

## Solution

```
while color() != 'b':
    if color() == 'r':
        right()
    else:
        if color() == 'g':
            left()
        else:
            fly()
```
