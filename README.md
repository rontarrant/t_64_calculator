# T-64 Calculator
A calculator designed from the ground up as a coding companion for retro programmers. Specifically, it's aimed at those who still love and write for the Commodore C-64.
What it can do:
- add, subtract, multiply, and divide...
- 8-bit numbers, and
- 16-bit numbers in three bases...
- hexadecimal,
- decimal, and
- binary,
- it can also:
- shift left, or
- shift right by a specified number of positions (although, more than 7 in 8-bit mode and you'll always end up with 0),
- and logic operations:
- AND,
- OR,
- XOR, and
- NOT,
- and it handles:
- signed numbers, and
- unsigned numbers.

You'll notice, too, that there are three number fields at the top. That's so you can see your work as you work. I originally designed it this way so I could see if binary  logic operations worked properly, but left it because... well, I think it's kind of neat.

The colours may strike you as odd, but everything except the background colour is from the C-64 palette... or as close as I could get with current digital colour technology.

To run:
- install:
  - Python,
  - PySide6,
  - icecream (used only for debugging, so feel free to comment all those ic() lines out),
  - dataclasses? (is that part of the standard install for Python?),
- type: python main.py
