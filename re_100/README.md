## binary

	r101: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.24, BuildID[sha1]=0f464824cc8ee321ef9a80a799c70b1b6aec8168, stripped

____

	$ ./r101      
	Enter the password: asdf
	Incorrect password!

So this time we are prompted to enter a password after starting the binary.
Also we got a stripped 64-bit one at hand.


### main

![main](https://github.com/0x00rick/reverse_engineering/blob/master/re_100/images/main.png)


Not much to see in the main function.  
I think the picture says it all already.


### check password


![passwd1](https://github.com/0x00rick/reverse_engineering/blob/master/re_100/images/passwd1.png)



The first part of the check_passwd function moves around some values.
This is our provided input from `rdi` into `[rbp-0x38]`, as well as 3 weird/encrypted looking strings right above it into `[rbp-0x20]`, `[rbp-0x18]` and `[rbp-0x10]`.


![passwd2](https://github.com/0x00rick/reverse_engineering/blob/master/re_100/images/passwd2.png)
![passwd3](https://github.com/0x00rick/reverse_engineering/blob/master/re_100/images/passwd3.png)

Here in big part the fun happens.
First we have  initialize a loop counter to 0 and check if it is below 0xb (11).
This reveals the potential password length right away. 

Next up a multitude of additions, substractions, mutliplications and shift+rotates takes places.
It looks rather confusing at first, but in the end not too much happens honestly.
I'll try my best to explain it somewhat precisely for anyone stumbling upon this writeup.


### interesting operation [rbp+rax*8-0x20]

rbp stays always the same in each operation, since it is not messed with:

	gdb-peda$ x $rbp
	0x7fffffffdb30:	0x00007fffffffdc50
	gdb-peda$

#### 0th iteration:

right before the 'interesting operation `rax = 0x0`. This leaves the equation with this:

	>>> hex(0x7fffffffdb30-0x20)
	'0x7fffffffdb10'

0x7fffffffdb10' points to an address 0x400914 that holds the string "Dufhbmf".


#### 1st iteration:

rax = 0x1

	>>> hex(0x7fffffffdb30+0x1*8-0x20)
	'0x7fffffffdb18'

0x7fffffffdb18' points to address  0x40091c that holds the string "pG`imos".


#### 2nd iteration 


rax = 0x2

	>>> hex(0x7fffffffdb30+0x2*8-0x20)
	'0x7fffffffdb20'
	
0x7fffffffdb20 points to 0x400924 that hold "ewUglpt".


#### 3rd iteration:

Okay what now? 
The first 3 iterations revealed that `[rbp+rax*8-0x20]` pointed to the stored "encrypted" strings.
There is no follow up on this now tho!

	rax = 0x3
	rdx = 0x55555556
	[...]
	imul edx = 0x55555556 * 0x3 = 0x100000002
	
This result is stored in eax!
eax holds up to 8 bit which in this case is only 0x00000002
=> eax = 0x00000002

the following sar, sub, mov and add operations end up with rax being 0 again right before `[rbp+rax*8-0x20]`.
Meaning in the 4th iteration the result here once again points to yields the same as in the 1st iteration:

rax = 0x0 


	>>> hex(0x7fffffffdb30-0x20)
	'0x7fffffffdb10'
	
0x7fffffffdb10' points to address  0x400914 that holds the string "Dufhbmf".
	
**What is different now compared to the first iteration?**

The character from one of the weird strings is chosen as follows:

	add 	rax,rsi
	movzx 	eax, byte [rax]
	
rsi always is the address from one of the weird strings:

In loop iteration 0,3,6 and 9 the address of "Dufhbmf" is calculated.
In loop iteration 1,4,7 and 10 the address of "pG`imos" is calculated.
In loop iteration 2,5,8 and 11 the address of "ewUglpt" is calculated.

This is the case because the multiplication and adding/substraction always yields 0x0, 0x1, or 0x2 right before `[rbp+rax*8-0x20]`...


### ... but here is the catch:

the value of rax in:

	-> 0x40076b add 	rax,rsi <-
	   0x40076e movzx 	eax, byte [rax]
	

that determines the chosen character from one of the strings depends on the loop iteration too, but it does not simply represent a loop counter from 0 to 11.

Instead `rax` holds 0 in the first 3 iterations. 
This results in an addition with 0, so the addition yields `rsi` again, which holds the address of one of the weird strings.
Furthermore the `movzx 	eax, byte [rax]` gets the 0th position of each of the 3 strings (most significant bit):  "Dufhbmf", "pG`imos", "ewUglpt" (so 'D',  'p' or 'e') for the later substraction of:

	character_from_one_of_the_weird_strings - user_input has to yield 1 at 0x400787 and following.


In the same manner rax holds 2 in the 3rd to 5th iteration, 4 in the 6th to 8th iteration and 6 in the 9th to 11th iteration.
Meaning in those iterations the 2nd ('f',  '`' or 'U'), 4th ('b', 'm' or 'l') and 6th ('f', 's', 't') position of each of the three weird strings is taken for the substraction.


### Final problem to solve

What it finally comes down to is a joke and shown below :D :

- 'D' <-> 0x44:	0x44 - x = 0x1	=> x = 0x43 <-> 'C'
- 'p' <-> 0x70:	  0x70 - x = 0x1	=> x = 0x69 <-> 'o'
- 'e' <-> 0x65:	  0x65 - x = 0x1	=> x = 0x64 <-> 'd'
- 'f' <-> 0x66:	  0x66 - x = 0x1	=> x = 0x65 <-> 'e'
- '`' <-> 0x60:	  0x60 - x = 0x1	=> x = 0x59 <-> '_'
- 'U' <-> 0x55:	  0x55 - x = 0x1	=> x = 0x54 <-> 'T'
- 'b' <-> 0x62:	  0x62 - x = 0x1	=> x = 0x61 <-> 'a'
- 'm' <-> 0x6d:	0x6d - x = 0x1	=> x = 0x6c <-> 'l'
- 'l' <-> 0x6c:	0x6c - x = 0x1	=> x = 0x6b <-> 'k'
- 'f' <-> 0x66:	0x66 - x = 0x1	=> x = 0x65 <-> 'e'
- 's' <-> 0x73:	0x73 - x = 0x1	=> x = 0x72 <-> 'r'
- 't' <-> 0x74:	0x74 - x = 0x1	=> x = 0x73 <-> 's'


=> leaving us with the password: 'Code_Talkers'


