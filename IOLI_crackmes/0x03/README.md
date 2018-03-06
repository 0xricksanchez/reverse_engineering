## binary

	$ file crackme0x03 
	crackme0x03: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.9, not stripped
----
	$ ./crackme0x03 
	IOLI Crackme Level 0x03
	Password: asdf
	Invalid Password!

## solution

This one was a bit tricky when encountering it the first time.
You kinda have to approach it in a backwards way.


	
The main function does not differ much from the crackme before.
It still has the same `0x00052b24` calculation in there, just right afterwards a function call to `test` happens:

![main](https://github.com/0x00rick/reverse_engineering/blob/master/IOLI_crackmes/0x03/images/main.png)


In the test function you're encountered with a compare statement followed by a split control flow, depending on the result.
The present strings do not make much sense, but you can still solve it without knowing what they mean.

![test](https://github.com/0x00rick/reverse_engineering/blob/master/IOLI_crackmes/0x02/images/test.png)

**Why is that?**


Because once you reach the compare statement at `0x8048477` you can quickly find the values which are being compared from within gdb.
It's the `0x00052b24` and our user input.
If they match the `je` is executed, which is the 'good ending.'

**But how can we find out with a static analysis?**

Right after the split control flow in `test` a function called `shift` is called with one of these encrypted looking strings.

So lets take a look at this function.

![shift](https://github.com/0x00rick/reverse_engineering/blob/master/IOLI_crackmes/0x02/images/shift.png)

Basically what it comes down to is that here the `string_length` function is called with one of these weird strings as an argument.
The next steps can be summarized as follows:

* get string length
* init a loop counter (i=0, i<result_of_strlen,i++)
* in each loop iteration substract 0x3 from one of the characters from the weird strings
* when strlen is matched print the result of the substraction.

This can be quickly scripted in python as follows:




	>>> ''.join(unichr(ord(x)-0x3) for x in 'Lqydolg#Sdvvzrug$')
	u'Invalid Password!'
	>>> 

---

	>>> ''.join(unichr(ord(x)-0x3) for x in 'Sdvvzrug#RN$$$#=')
	u'Password OK!!! :'
	>>> 
	
That way we can understand which path in `test` we want to take.