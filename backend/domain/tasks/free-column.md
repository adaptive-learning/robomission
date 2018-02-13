# free-column
- category: comparing

## Setting

```
|bA|bA|bA|b |bA|
|kA|kW|kA|kM|kA|
|kA|k |kA|kZ|kA|
|kA|k |kA|kA|kX|
|kA|k |kA|kA|kM|
|kZ|kX|kY|kA|k |
|kM|kA|kM|kA|kM|
|k |kA|k |kA|k |
|kM|kA|kM|kA|kM|
|kW|kA|kS|kA|kY|
```
- energy: 8
- length: 4

## Solution

```
while color() != 'b':
    if position() != 2:
        shoot()
    fly()
```
