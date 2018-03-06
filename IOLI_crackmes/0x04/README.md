## binary

	$ file crackme0x04 
	crackme0x04: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.9, not stripped

---


	$ ./crackme0x04 
	IOLI Crackme Level 0x04
	Password: asdf
	Password Incorrect!

## solution

This one does not do much.

The main function is not worth taking a look at.
All it does is take user input again and call a function `check` with it as a function argument.

So lets take a look at the `check` routine.

![check](https://github.com/0x00rick/reverse_engineering/blob/master/IOLI_crackmes/0x04/images/check.png)


It takes the user input and calls `strlen` on it.  
Then a loop is entered, where each byte of the input is looked at individually.
In each iteration one byte from the input is taken and added to a *sum* starting at 0.  
Then afterwards this value is compared to 0xf (15).
If at any point the value of the sum equals 0xf or 15 we win.
So any input like 69, 771, 663 or even 111111111111111 is correct.

If the value is not 0xf at any point of the loop we lose.


	$ ./crackme0x04    
	IOLI Crackme Level 0x04
	Password: 111111111111111
	Password OK!
