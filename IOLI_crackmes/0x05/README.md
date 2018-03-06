## binary

	$ file crackme0x05 
	crackme0x05: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.9, not stripped

---

	$ ./crackme0x05 
	IOLI Crackme Level 0x05
	Password: asdf
	Password Incorrect!

## solution


The main function does not bring anything new to the table here.


![check](https://github.com/0x00rick/reverse_engineering/blob/master/IOLI_crackmes/0x05/images/check.png)


The check function is similar built compared to before.
Just this time the sum of the user input check against 0x10 (16) instead of 0xf (15).
If we pass that check a function called `parell` is called with our input as the function argument.

![parell](https://github.com/0x00rick/reverse_engineering/blob/master/IOLI_crackmes/0x04/images/parell.png)

In the parell function, the program reads the user input as a whole integer. Once the input string contains other symbols rather than digits, it will output “incorrect password”.



	$ ./crackme0x05 
	IOLI Crackme Level 0x05
	Password: 22222222
	Password OK!
