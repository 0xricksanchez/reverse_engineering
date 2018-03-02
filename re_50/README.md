## Binary

	re50: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=0333e23e0d2046a0ceb6b920faebaa0b6ee45f15, stripped
	
---

	$ ./re50 
	Usage : ./crackme password



## The disassembly

The binary itself does not provide much to fiddle around with.

The main function first checks of we did provide a password upon starting the crackme.
If not it exits right away.

![main](https://github.com/0x00rick/reverse_engineering/blob/master/re_50/images/main.png)

If we did provide a password we directly get to the only operation routine which we need to solve.
First what was meant to be a password length check takes places to see if our input has 0x15 (21) characters. This check is broken in my binary. Maybe i fetched a broken version (check `0x8048746`).

Next up we land in a loop which does mainly 2 things:

![routine](https://github.com/0x00rick/reverse_engineering/blob/master/re_50/images/juice.png)


### First

The binary loads the address `0x8048550` into eax and adds the current loop counter on it.
So depending on the loop iteration we end up with `0x8048551`, `0x8048552`, ... , until `0x8048565`.   
We always check the **contents** at the new address and take the LSB of it.


### Secondlly

We take a byte of our user provided input and XOR it against some hard coded stored values at `0x8049b90`.   
Afterwards we compare that result against the value of the first step above.
This happens in each round until a length of 21 characters.

## The math to do

What it comes down to in the end is:

	which_user_input XORed content_byte_at_calculated_round_address = hard_coded_round_byte_value
	

Luckily we can transform the xor math like this:

	? xor b = c <=> b xor c = ?
	
Since we can read out the values for b adn c from memory we can write a simple python script to calculate the correct input:

```python
#!/usr/bin/env python

import operator as op

# gdb-peda$ x/25xb 0x8049b90
fixed_list = [0x34, 0xd6, 0xa8, 0xe2, 0x88, 0x77, 0xaa, 0x04,
              0x9e, 0x98, 0x33, 0x82, 0xda, 0x54, 0x8f, 0x1b,
              0x45, 0x5b, 0x37, 0xbb, 0x1d]

# gdb-peda$ x/32xb 0x8048550
xor_values = [0x55, 0x89, 0xe5, 0x83, 0xec, 0x28, 0xc7, 0x45,
              0xf0, 0xc7, 0x45, 0xf4, 0xeb, 0x20, 0xc7, 0x44,
              0x24, 0x04, 0x01, 0x8b, 0x45]
result = ''

for (x, y) in zip(fixed_list, xor_values):
    print('xoring {} and {}'.format(hex(x), hex(y)))
    key_part = op.xor(x, y)
    print('result: {} ({})'.format(unichr(key_part), hex(key_part)))
    result += unichr(key_part)
print(result)
```
