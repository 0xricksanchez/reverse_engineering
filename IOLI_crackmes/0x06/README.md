## binary

	$ file crackme0x06
	crackme0x06: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.9, not stripped
	
---

	$ ./crackme0x06   
	IOLI Crackme Level 0x06
	Password: asdf
	Password Incorrect!
	
## solution

This binary does not look majorly different from 0x05 again. 
It has a little twist, which might go unnoticed!

The binary takes an environment variable upon executing and uses it later on in the `dummy` function.

> Note: Environment variables are a set of dynamic named values that can affect the way running processes will behave on a computer.

But later more.

Again we have a `main` function that reads in our user input, and stores said environment variable too.
A function call to `check` follows, where once again the sum of the user input is checked against 0x10 (16) as before.
If that is the case the `parell` function is called.
In there `sscanf` is used again to load the user input as an integer. and right afterwards a function call to a method `dummy` happens.
Here is the new part:

![dummy](https://github.com/0x00rick/reverse_engineering/blob/master/IOLI_crackmes/0x06/images/dummy.png)


In here the user input is totally ignored.  
But instead a mysterious string "LOLO" is appearing.
If you missed the part with the environment variable this function looks weird at first, since some random looking stuff is loaded into the registers and compared to "LOLO" with `strncmp`.
In my first attempt this was "XDG_SEAT=seat0", which made no sense to me.
Then it hit me! 
This one is an environment variable too and actually the first one on my current system when printing all of them to console:

	$ env
	XDG_SEAT=seat0
	XDG_SESSION_ID=c2
	LC_IDENTIFICATION=de_DE.UTF-8
	LC_TELEPHONE=de_DE.UTF-8
	DISPLAY=:0
	UNITY_DEFAULT_PROFILE=unity
	QT_LINUX_ACCESSIBILITY_ALWAYS_ON=1
	UPSTART_JOB=unity7
	JOB=unity-settings-daemon
	GNOME_KEYRING_CONTROL=
	[...]
	
So then I tried starting my binary set with "LOLO" as an env variable.



	$ LOLO= ./crackme0x06
	IOLI Crackme Level 0x06
	Password: 6262
	Password OK!

