## binary

	$ file crackme0x02 
	crackme0x02: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.9, not stripped
----
	$ ./crackme0x02 
	IOLI Crackme Level 0x02
	Password: asdf
	Invalid Password!

## solution

Again strings does not bring in any results.
So we have to take a look at the assembly again.


![main](https://github.com/0x00rick/reverse_engineering/blob/master/IOLI_crackmes/0x02/images/main.png)


	$ ./crackme0x02
	IOLI Crackme Level 0x02
	Password: 338724
	Password OK :)
