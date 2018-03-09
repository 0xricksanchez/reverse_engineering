## The binary

	$ file neophyte 
	neophyte: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.24, BuildID[sha1]=f382dd94583c7310bc8b3dd538e9e604f5a6ee38, stripped
	
We've got a stripped x86 binary.
Let's try to execute it.

	$ ./neophyte 
	Usage:	
	 ./neophyte_reversing <41 byte flag>

The expected flag seems to have a length of 41 byte (41 characters).

	$ ./neophyte AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
	no
	
When entering a wrong key of the correct length we just get a "no" as a response.

	$ ./neophyte AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA 
	size differs 40 vs 41!
	no

If the key is too short we even get a size warning.
If the key is too long we don't.
We just get the "no", as seen below:

	>>> print 'A'*41+'B'
	AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB
	>>> 

	$ ./neophyte AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB
	no
	


	
## the disassembly

Let's take a look at the disassembly to get a quick overview of what is in front of us.


![main](https://github.com/0x00rick/reverse_engineering/blob/master/neophyte/images/main.png)  


The main routine does all of the print statements if a wrong or missing user input is present.

* at 0x8049251 the "Usage: ...." string is outputted if no argument was given
* at 0x80492d1 we have a check for the length of our input if it differs from a length of 41 characters, we jump to 0x80492d6, which is the "size differs...." block
* at 0x804931b we have the "no" statement,
* at 0x804930d we have the good ending part we wanna reach, which prints "yes".


If we did provide some input we first jump to a code block where a function is called.
I renamed it "mallocator".  
You'll see why shortly.  

![mallocator](https://github.com/0x00rick/reverse_engineering/blob/master/neophyte/images/mallocator.png)

In here a bunch of stuff happens, which might look intimidating at first.

![malloc](https://github.com/0x00rick/reverse_engineering/blob/master/neophyte/images/malloc.png)

We have a really long function, without any control flow splitting or anything.  
But what we do have is a bunch of allocations using `malloc` multiple times.  
41 times in fact.
In each of the 41 allocations the basic procedure will produce a memory chunk looking like this:

	EAX: 		some_address   --> value_v
	EAX+0x4:	some_address+4 --> value_w
	EAX+0x8:	some_address+8 --> value_x
	EAX+0xc:	some_address+12 --> value_y
	EAX+0x10: 	some_address+16 --> value_z

Our register `EAX` always holds some address in the end, which points to some assigned value.
Each `malloc` call has a size argument of 0x14 (20) bytes.


Ultimately this function calls `malloc` 41 times each allocation takes up 24 bytes in total meaning a total of 984 bytes are allocated in memory.
We do not have any control over the size nor the values allocated.

After this is done we enter a loop structure, where an initialized loop counter to 0 is compared to 0x28 (40) and only if that counter is > 0x28 we switch the control flow and continue execution.


![loop](https://github.com/0x00rick/reverse_engineering/blob/master/neophyte/images/loop.png)  

The loop itself is fairly simple and can be broken down in a few points

* get user input from stack
* add loop counter on the address that holds the user input to fetch a new byte every round
* calculate one of the prior allocated values in "mallocator" by using the base address where the allocations starts and adding the loop counter*4 on top of it
* push a byte from the user input and an allocated value to the stack and call a new function, which has the name "overwrite_malloc_math" in my disassembly


So let us take a look at that routine and check what it does with our input and the allocated values.


![mallocm](https://github.com/0x00rick/reverse_engineering/blob/master/neophyte/images/mallocmath.png)


So what does it do?  
The snippet in the screenshot shows a basic overview of it.
In there the current taken allocated byte from the malloc routine is compared to hardcoded values.  
If such a comparison fails control flow jumps to the next code block with a another comparison to another hardcoded value.  
If a comparison is successfull we enter a code block where user input still does not play any role.  
Depending on which code block was entered (which comparison was successfull) 2 of the 5 values in one allocated chunk are loaded into the register and one mathematical operation is done on them (either add, sub, xor, imul or idiv).  
The result is stored in the memory chunk where the 2 values where taken from at one of the positions of these 2 values.

Kinda confusing I know, but in the end it's just a bunch of math operations on 2 values each time, where the result is safely stored in some allocated memory again.

Now here comes the interesting part.  
At the end of this function one of the modified/calculated values is loaded again and compared to the current user input byte.
We want this comparison to succeed so afterwards `mov		eax,0x0` takes place, which we need upon leaving this function.  
This is the case because right after leaving a `test		eax,eax` is taking place, which again needs to yield 0 so the loop counter is incremented by one (check 0x80492ab) .  
This test instruction only yields 0 if eax is 0.  


### disassembly summary

To summarize the findings:  
In each loop iteration we take one byte (one character) from our provided input and some address is loaded at which 5 values were allocated.  
Then a bunch of mathematical operations take place and in the end a new value is compared to our input byte.  

So easy, we just jump right to the comparison part and see what value is expected from us to continue.  
I did that and found the first 5 characters of the flag, which were *OpenC*.  
The next character means trouble tho...


### Why trouble?

See below:


	EAX: 0x61 ('a')
	EBX: 0x0 
	ECX: 0x90 
	EDX: 0xffffffc4 
	ESI: 0xf7fa6000 --> 0x1b1db0 
	EDI: 0xf7fa6000 --> 0x1b1db0 
	EBP: 0xffffce18 --> 0xffffce48 --> 0x0 
	ESP: 0xffffce14 --> 0x61 ('a')
	EIP: 0x80485fc (cmp    edx,eax)
	EFLAGS: 0x206 (carry PARITY adjust zero sign trap INTERRUPT direction overflow)
	[-------------------------------------code-------------------------------------]
	   0x80485f2:	mov    eax,DWORD PTR [ebp+0x8]
	   0x80485f5:	mov    edx,DWORD PTR [eax+0x10]
	   0x80485f8:	movsx  eax,BYTE PTR [ebp-0x4]
	=> 0x80485fc:	cmp    edx,eax
	   0x80485fe:	jne    0x8048607
	   0x8048600:	mov    eax,0x0
	   0x8048605:	jmp    0x804860c
	   0x8048607:	mov    eax,0x1
	[------------------------------------stack-------------------------------------]
	0000| 0xffffce14 --> 0x61 ('a')
	0004| 0xffffce18 --> 0xffffce48 --> 0x0 
	0008| 0xffffce1c --> 0x80492a9 (test   eax,eax)
	0012| 0xffffce20 --> 0x804c080 --> 0x17 
	0016| 0xffffce24 --> 0x61 ('a')
	0020| 0xffffce28 --> 0xffffcef0 --> 0xffffd159 ("XDG_SEAT=seat0")
	0024| 0xffffce2c --> 0xf7e22c0b (<__GI___cxa_atexit+27>:	add    esp,0x10)
	0028| 0xffffce30 --> 0xf7fa63dc --> 0xf7fa71e0 --> 0x0 
	[------------------------------------------------------------------------------]
	Legend: code, data, rodata, value

	Breakpoint 2, 0x080485fc in ?? ()
	gdb-peda$ 


We are right at said comparison statement where our input byte is compared to one of these computed values.
Our input always resides in register `EAX` and the calculated value is loaded into `EDX`.

So I did provide an `0x61 (a)` and expected from me is `0xffffffc4`.
So what is `0xffffffc4`?  
Where did I go wrong?  

Turns out I did not make a mistake.  
This challenge was never intended to be solved the way I approached it.  



## the solution



```python
import angr
import claripy


project = angr.Project("./neophyte")
arg1 = claripy.BVS('arg1', 8*41)
args = ["./neophyte", arg1]
state = project.factory.entry_state(args=args)
pg = project.factory.simgr(state)
pg.explore(find=0x804930d, avoid=(0x804931b, 0x80492ad))
print("Flag: {0}".format(pg.found[0].state.se.eval(arg1, cast_to=str)))

```

Yes this small script solves all our problems!
It uses the power of the angr project and with that the power of symbolic execution.  
This is just the tip of the iceberg what we could do with angr, you should definitely check it out!  

A more documented version can be found in the solve.py script in this repository.  



This produces the following:

	$ python solve.py
	WARNING | 2018-03-09 18:38:03,515 | angr.analyses.disassembly_utils | Your verison of capstone does not support MIPS instruction groups.
	Flag: OpenC�F{IhopeYOUdidThisInADebuggerScript}
	
We can see this one erroneous character, which is exactly at this 6th position I was struggling with before, but this the correct and intended flag.

## Last words
Static Analysis in BinaryNinja and some quick dynamic analysis from within gdb almost revealed all of the mystery of this binary pretty quickly, but this one part of the flag made it difficult if you're not familiar with debugging, or know the power of tools like angr.  




## resources

* [claripy](https://docs.angr.io/docs/claripy.html)
* [angr](https://github.com/angr/angr)


## thanks

Special thanks to OpenCTF for this challenge!
