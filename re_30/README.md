##binary 


	$ file re3022 
	re3022: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.18, BuildID[sha1]=e4f10202a245d933c0146596eab6d2ff114c8b4e, stripped

---
	$ ./re3022 
	Usage: ./crackme password

---
	$ ./re3022 AAAA
	KO

## disassembly

![main](https://github.com/0x00rick/reverse_engineering/blob/master/re_30/images/main.png)

Pretty much every noteworthy event is documented in this screenshot or the binary ninja file.  
The binary takes input upon starting.
There is one input length check, which results in a password length of 8.

Afterwards the password is calculated from a simple formula:

* Take round key (0,10,20,...,80)
* xor that one with current user input byte
* compare that result to a hardcoded value
* repeat 8 times

Since we don't know the user input obviously, we have to change the formula a bit:

```python
    round_key = 0
    password = ''
    for hard_coded_passwd_byte in static_bytes:
        res = op.xor(hard_coded_passwd_byte, round_key)
        password += res
        round_key += 0xa
```
This works since a xor b = c is the same as b xor c = a.
