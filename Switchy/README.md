## binary

	$ file switchy
	switchy: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.24, BuildID[sha1]=ed173f80ccccc36c7c25b5093a93f67e28bc0acc, not stripped

----
	$ ./switchy 
	i������������iQ�F


Running the binary gives us some garbage output...

	$ ./switchy afds
	i������������iQ�F
	
Providing any input upon executing does not change that behavior.

If we take the garbage output as a possible indicator for the correct password we can see that it has a length 0f 20 characters...

Up until now it is unsure whether or not the binary takes any input from the user. To find out let's check the disassembly!

## disassembly

![main](https://github.com/0x00rick/reverse_engineering/blob/master/switchy/images/main1.png)

The function prologue in main makes clear there is no interaction with user input whatsoever.
Our only hint so far is still the 20 char long garbage output.
Next thing which  is standing out is that the main function can be viewed as a changing of the following behavior:

* load some predefined value into EAX and push it on the stack
* call a function with that loaded value
* when returning to main push `%c` and the return value from the function on the stack
* call `printf` and print the result to console
* clear the stream buffer via `fflush`
* repeat 35 times

This part seems fishy. The output looked 20 characters long but `printf` is called 35 times.
This is a new indicator that the real flag has a length of 35 characters.

So let us first check where the function argument values are taken from:


![func_args](https://github.com/0x00rick/reverse_engineering/blob/master/switchy/images/func_args.png)

The snipped shows these values are stored starting from address `0x804b050`. The last value is stored at `0x804b144`.
Next let us take a look at the called function.

![switchy](https://github.com/0x00rick/reverse_engineering/blob/master/switchy/images/switchy.png)

The picture shows that this function has a not a lot of depth, but a wide spread in control flow, meaning there is not too much going on once one path was taken.

**ENHANCE**

![switchy_calc](https://github.com/0x00rick/reverse_engineering/blob/master/switchy/images/switchy_calc.png)

The function takes its function argument and first substracts `0x14` from it. Then prepares the stack as seen in the screenshot.
The `ja` is never taken so control flow always ends up at `0x804848d`.
Here the function argument is loaded into EAX again.
Next up the most important step takes place.
The value in EAX is used to determine the contents of ECX by doing:

	
	ECX = contents @ [function_arg * 4 + 0x8048f40]
	

This resulting value in ECX is taken for control flow redirection via `jmp ECX`.
	
![jumpy](https://github.com/0x00rick/reverse_engineering/blob/master/switchy/images/jumpy.png)

The whole jump table can be seen in the `.rodata` section defining every jump for all 20 cases.

One example for the first taken jump is the following:

![example_case](https://github.com/0x00rick/reverse_engineering/blob/master/switchy/images/example_case.png)

All cases are all structured the same way.

* Two predefined values are loaded into EAX and ECX
* xor those values, ending up with the result in EAX
* jump to `0x80486bf`

The results for each of the first 20 rounds are depicted below:

* r1: case 0x9 -> xoring yields 0x63 'c' -> dl holds 0x63
* r2: case 0xe -> xoring yields 0xffffffdb -> dl holds 0xffffffdb
* r3: case 0x6 -> xoring yields 0x7d '}' -> dl holds 0x7d
* r4: case 0x2 -> xoring yields 0xffffffdb -> dl holds 0xffffffdb
* r5: case 0x13 -> xoring yields 0xffffff97 -> dl holds 0xffffff97
* r6: case 0x10 -> xoring yields 0xffffffea -> dl holds 0xffffffea
* r7: case 0x12 -> xoring yields 0x4c 'L' -> dl holds 0x4c
* r8: case 0xa -> xoring yields 0xffffffc9 -> dl holds 0xffffffc9
* r9: case 0x11 -> xoring yields 0x26 '&' -> dl holds 0x26
* r10: case 0x4 -> xoring yields 0xe -> dl holds 0xe
* r11: case 0xb -> xoring yields 0x7 -> dl holds 0x7
* r12: case 0x1 -> xoring yields 0xffffffb7 -> dl holds 0xffffffb7
* r13: case 0xc -> xoring yields 0xd '\r' -> dl holds 0xd
* r14: case 0x5 -> xoring yields 0x69 'i' -> dl holds 0x69
* r15: case 0xd -> xoring yields 0xffffffae -> dl holds 0xffffffae
* r16: case 0x3 -> xoring yields 0x1f -> dl holds 0x1f
* r17: case 0x1 -> xoring yields 0xffffffb7 -> dl holds 0xffffffb7
* r18: case 0x3 -> xoring yields 0x1f -> dl holds 0x1f
* r19: case 0x0 -> xoring yields 0xfffffffc -> dl holds 0xfffffffc
* r20: case 0x2 -> xoring yields 0xffffffdb -> dl holds 0xffffffdb
* to be continued...

The resulting values do not make a lot of sense.
The least are valid printable characters.

So what is the solution/password/flag??



## solution

Let's take a closer look at the values taken for the xor operations.
These are located in the `.data` section of the binary and are neatly placed one after another.

![xor1](https://github.com/0x00rick/reverse_engineering/blob/master/switchy/images/xor_vals1.png)

The hex values may not look not like anything valuable, except the obvious weirdness of the negative ones!
So what about the ascii representation?

![xor2](https://github.com/0x00rick/reverse_engineering/blob/master/switchy/images/xor_vals2.png)

We can see a bunch of them have a valid ascii representation, but the current order does not make any sense...

When paying close attention during the dynamic analysis one can find the following hint:
Only the EAX register holds a hex value that has an ascii representation.

Example 1:

	[----------------------------------registers-----------------------------------]
	EAX: 0x7b ('{')
	EBX: 0x0 
	ECX: 0xffffffec 
	EDX: 0x0 
	ESI: 0xf7fa6000 --> 0x1b1db0 
	EDI: 0xf7fa6000 --> 0x1b1db0 
	EBP: 0xffffcd48 --> 0xffffce78 --> 0x0 
	ESP: 0xffffcd38 --> 0x13 
	EIP: 0x8048695 (xor    eax,ecx)
	EFLAGS: 0x297 (CARRY PARITY ADJUST zero SIGN trap INTERRUPT direction overflow)
	[-------------------------------------code-------------------------------------]
	   0x8048682:	jmp    0x80486bf
	   0x8048687:	movsx  eax,BYTE PTR ds:0x804b04a
	   0x804868e:	movsx  ecx,BYTE PTR ds:0x804b04b
	=> 0x8048695:	xor    eax,ecx
	   0x8048697:	mov    dl,al
	   0x8048699:	mov    BYTE PTR [ebp-0x1],dl
	   0x804869c:	jmp    0x80486bf
	   0x80486a1:	movsx  eax,BYTE PTR ds:0x804b04c
	[------------------------------------stack-------------------------------------]
	[...]


Example 2:

	[----------------------------------registers-----------------------------------]
	EAX: 0x73 ('s')
	EBX: 0x0 
	ECX: 0xffffff99 
	EDX: 0x0 
	ESI: 0xf7fa6000 --> 0x1b1db0 
	EDI: 0xf7fa6000 --> 0x1b1db0 
	EBP: 0xffffcd48 --> 0xffffce78 --> 0x0 
	ESP: 0xffffcd38 --> 0x10 
	EIP: 0x8048647 (xor    eax,ecx)
	EFLAGS: 0x297 (CARRY PARITY ADJUST zero SIGN trap INTERRUPT direction overflow)
	[-------------------------------------code-------------------------------------]
	   0x8048634:	jmp    0x80486bf
	   0x8048639:	movsx  eax,BYTE PTR ds:0x804b044
	   0x8048640:	movsx  ecx,BYTE PTR ds:0x804b045
	=> 0x8048647:	xor    eax,ecx
	   0x8048649:	mov    dl,al
	   0x804864b:	mov    BYTE PTR [ebp-0x1],dl
	   0x804864e:	jmp    0x80486bf
	   0x8048653:	movsx  eax,BYTE PTR ds:0x804b046
	[------------------------------------stack-------------------------------------]
	[...]


### Flag

One can get to the flag when inspecting the EAX register every time the xor operation takes place.
This basically happens under the following conditions:

* gdb-peda$ b *0x8048497
* gdb-peda$ r
* gdb-peda$ si 3
* and check EAX

This way, we get the flag `flag{switch jump pogo pogo bounce}`.

## Credits

Thanks to [OptenToAll](https://ctftime.org/team/9135) for this challenge!