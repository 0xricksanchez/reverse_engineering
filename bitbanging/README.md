

# binary

	$ file bin
	bin: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=917a8066affea23dc0c37a01c9004f8efa4e4c25, not stripped


We've got an unstripped x64 binary. Let's see how it behaves upon running:

	$ ./bin   
	Usage: ./bin [key]

We need to provide  a key!

	$ ./bin asdf  
	The key has to be a number!

So we've got some more information about the needed input now.

	$ ./bin 111111
	Wrong length!
	
We even get feedback about the length, we could bruteforce the length by providing any number from length 1 to n.
Let's take a look at the disassembly instead.


![input_length](https://github.com/0x00rick/reverse_engineering/blob/master/bitbanging/images/input_length.png)

Okay so we need to provide a number of length 4.  
If only one input is accepted that leaves us with a 1 in 10^4 probability.
Let's dig some further into the disassembly.



		gdb-peda$ disassemble main
		Dump of assembler code for function main:
		   0x00000000004005f6 <+0>:	push   rbp
		   0x00000000004005f7 <+1>:	mov    rbp,rsp
		=> 0x00000000004005fa <+4>:	sub    rsp,0x20
		   0x00000000004005fe <+8>:	mov    DWORD PTR [rbp-0x14],edi
		   0x0000000000400601 <+11>:	mov    QWORD PTR [rbp-0x20],rsi
		   0x0000000000400605 <+15>:	cmp    DWORD PTR [rbp-0x14],0x2
		   0x0000000000400609 <+19>:	je     0x40062e <main+56>			# continue if input was provided
		   0x000000000040060b <+21>:	mov    rax,QWORD PTR [rbp-0x20]
		   0x000000000040060f <+25>:	mov    rax,QWORD PTR [rax]
		   0x0000000000400612 <+28>:	mov    rsi,rax
		   0x0000000000400615 <+31>:	mov    edi,0x400854				# otherwise load Usage: ... string
		   0x000000000040061a <+36>:	mov    eax,0x0
		   0x000000000040061f <+41>:	call   0x4004c0 <printf@plt>			# print Usage: ... string
		   0x0000000000400624 <+46>:	mov    edi,0x1
		   0x0000000000400629 <+51>:	call   0x4004e0 <exit@plt>			# exit binary
		   0x000000000040062e <+56>:	mov    rax,QWORD PTR [rbp-0x20]			# continue execution here if input was provided
		   0x0000000000400632 <+60>:	add    rax,0x8
		   0x0000000000400636 <+64>:	mov    rax,QWORD PTR [rax]			# load input into RAX
		   0x0000000000400639 <+67>:	mov    rdi,rax					# mov input into RDI as calling argument (check x64 ABI!)
		   0x000000000040063c <+70>:	call   0x4004b0 <strlen@plt>			# call string_length() on our input
		   0x0000000000400641 <+75>:	cmp    rax,0x4					# check if it has length 4
		   0x0000000000400645 <+79>:	je     0x40065b <main+101>			# if yes continue execution
		   0x0000000000400647 <+81>:	mov    edi,0x400865				# otherwise load "Wrongth length!" into EDI
		   0x000000000040064c <+86>:	call   0x4004a0 <puts@plt>			# print that string
		   0x0000000000400651 <+91>:	mov    edi,0x1
		   0x0000000000400656 <+96>:	call   0x4004e0 <exit@plt>			# end program afterwards
		   0x000000000040065b <+101>:	mov    DWORD PTR [rbp-0x4],0x0			# set RBP-0x4 to 0
		   0x0000000000400662 <+108>:	jmp    0x400690 <main+154>			# continue execution at main+154
		   0x0000000000400664 <+110>:	mov    rax,QWORD PTR [rbp-0x20]			# main+110 is here
		   0x0000000000400668 <+114>:	add    rax,0x8					# pointer to our input
		   0x000000000040066c <+118>:	mov    rdx,QWORD PTR [rax]
		   0x000000000040066f <+121>:	mov    eax,DWORD PTR [rbp-0x4]			# sets EAX to current loop iteration
		   0x0000000000400672 <+124>:	cdqe   
		   0x0000000000400674 <+126>:	add    rax,rdx
		   0x0000000000400677 <+129>:	movzx  eax,BYTE PTR [rax]			# move first byte of input into RAX (higgest bit)
		   0x000000000040067a <+132>:	movsx  eax,al
		   0x000000000040067d <+135>:	lea    edx,[rax-0x30]				# loads input into edx
		   0x0000000000400680 <+138>:	mov    eax,DWORD PTR [rbp-0x4]
		   0x0000000000400683 <+141>:	cdqe   						# expands it to a quad word (4bytes to 8bytes)
		   0x0000000000400685 <+143>:	mov    DWORD PTR [rax*4+0x601060],edx	# inserts input into an array (see below for visualization)
		   0x000000000040068c <+150>:	add    DWORD PTR [rbp-0x4],0x1
		   0x0000000000400690 <+154>:	cmp    DWORD PTR [rbp-0x4],0x3			# main+154 is here!, use RBP-0x4 as loop condition
		   0x0000000000400694 <+158>:	jle    0x400664 <main+110>			# if it is <=3 jmp to main+110
		   0x0000000000400696 <+160>:	mov    DWORD PTR [rbp-0x4],0x0			#continue execution here after array is filled in first loop!
		   0x000000000040069d <+167>:	jmp    0x4006d8 <main+226>			#directly jump to main+226
		   0x000000000040069f <+169>:	mov    eax,DWORD PTR [rbp-0x4]			# main+169 is here.
		   0x00000000004006a2 <+172>:	cdqe   
		   0x00000000004006a4 <+174>:	mov    eax,DWORD PTR [rax*4+0x601060]	# load an input byte depending on loop iteration into EAX
		   0x00000000004006ab <+181>:	test   eax,eax
		   0x00000000004006ad <+183>:	js     0x4006c0 <main+202>			# pre emptive loop exit if test input_byte,input_byte fails
		   0x00000000004006af <+185>:	mov    eax,DWORD PTR [rbp-0x4]			# otherwise load loop counter into EAXeax
		   0x00000000004006b2 <+188>:	cdqe   
		   0x00000000004006b4 <+190>:	mov    eax,DWORD PTR [rax*4+0x601060]	# load current input_byte into EAX again
		   0x00000000004006bb <+197>:	cmp    eax,0x9					# compare if it to 9 
		   0x00000000004006be <+200>:	jle    0x4006d4 <main+222>			# if it is <= 9 (meaning it is a number!) continue loop
		   0x00000000004006c0 <+202>:	mov    edi,0x400873				# otherwise move "The key has to be a number!" into edo
		   0x00000000004006c5 <+207>:	call   0x4004a0 <puts@plt>			# print that string
		   0x00000000004006ca <+212>:	mov    edi,0x1
		   0x00000000004006cf <+217>:	call   0x4004e0 <exit@plt>			# and exit the binary 
		   0x00000000004006d4 <+222>:	add    DWORD PTR [rbp-0x4],0x1			# add +1 to loop counter and continue loop at main+226
		   0x00000000004006d8 <+226>:	cmp    DWORD PTR [rbp-0x4],0x3			# main+226 is here another loop condition check with 3 iterations
		   0x00000000004006dc <+230>:	jle    0x40069f <main+169>			# if iteration <= 3 jump to main+168
		   0x00000000004006de <+232>:	mov    eax,DWORD PTR [rip+0x20097c]        # 0x601060 <array>	# if all 4 bytes are verified as numbers MSB is loaded into EAX
		   0x00000000004006e4 <+238>:	cmp    eax,0x5					# and compared to 0x5 
		   0x00000000004006e7 <+241>:	jne    0x4007b6 <main+448>			# if its not equal to 0x5 we jump to main+448, meaning our first digit should be a 5!
		   0x00000000004006ed <+247>:	mov    eax,DWORD PTR [rip+0x200971]        # 0x601064 <array+4>		# load second input byte into EAX
		   0x00000000004006f3 <+253>:	neg    eax					# negate EAX, meaning: 0 - EAX and put the result into EAX
		   0x00000000004006f5 <+255>:	mov    edx,eax					# move that value into EDX
		   0x00000000004006f7 <+257>:	mov    eax,DWORD PTR [rip+0x200967]        # 0x601064 <array+4>		# load 2nd input byte into EAX again
		   0x00000000004006fd <+263>:	add    eax,0x1					# add 1 on our 2nd input byte
		   0x0000000000400700 <+266>:	and    eax,edx					# to a bitwise AND with the negative of our 2nd input byte and our 2nd input byte+1 (check below!)
		   0x0000000000400702 <+268>:	and    eax,0x4					# do another bitewise and of the prior result with 0x4
		   0x0000000000400705 <+271>:	test   eax,eax						
		   0x0000000000400707 <+273>:	je     0x4007a2 <main+428>			# jumps if TEST EAX, EAX results in a set zero flag
		   0x000000000040070d <+279>:	mov    eax,DWORD PTR [rip+0x200955]        # 0x601068 <array+8> 		# load 3rd input byte
		   0x0000000000400713 <+285>:	cmp    eax,0x6					# compare it to 6
		   0x0000000000400716 <+288>:	je     0x40078e <main+408>			# if is equal to 6 goto a bad exit, so 3rd input has to be !=6
		   0x0000000000400718 <+290>:	mov    eax,DWORD PTR [rip+0x20094a]        # 0x601068 <array+8> load 3rd input byte again
		   0x000000000040071e <+296>:	cmp    eax,0x5					# check against 5
		   0x0000000000400721 <+299>:	je     0x40078e <main+408>			# if its equal to 5 goto a bad exit again, so it has to be !=5 too!
		   0x0000000000400723 <+301>:	mov    eax,DWORD PTR [rip+0x20093f]        # 0x601068 <array+8>		# load 3rd input byte
		   0x0000000000400729 <+307>:	neg    eax					# oh its the same routine as above!
		   0x000000000040072b <+309>:	mov    edx,eax
		   0x000000000040072d <+311>:	mov    eax,DWORD PTR [rip+0x200935]        # 0x601068 <array+8>
		   0x0000000000400733 <+317>:	add    eax,0x1
		   0x0000000000400736 <+320>:	and    eax,edx
		   0x0000000000400738 <+322>:	and    eax,0x2					# just this time we need to make sure it passes the and eax, 0x2 followed by a test
		   0x000000000040073b <+325>:	test   eax,eax
		   0x000000000040073d <+327>:	je     0x40078e <main+408>
		   0x000000000040073f <+329>:	mov    eax,DWORD PTR [rip+0x200927]        # 0x60106c <array+12>		load 4th input byte 
		   0x0000000000400745 <+335>:	cmp    eax,0x8					# compare it to 8
		   0x0000000000400748 <+338>:	je     0x40077a <main+388>			# bad exit if it is 8, so it has to be !=8 
		   0x000000000040074a <+340>:	mov    eax,DWORD PTR [rip+0x20091c]        # 0x60106c <array+12>	# and to make it more annoying another check for the 4th byte
		   0x0000000000400750 <+346>:	neg    eax					# again the same routine 
		   0x0000000000400752 <+348>:	mov    edx,eax
		   0x0000000000400754 <+350>:	mov    eax,DWORD PTR [rip+0x200912]        # 0x60106c <array+12>
		   0x000000000040075a <+356>:	add    eax,0x1
		   0x000000000040075d <+359>:	and    eax,edx
		   0x000000000040075f <+361>:	and    eax,0x8					# just another test condition again
		   0x0000000000400762 <+364>:	test   eax,eax
		   0x0000000000400764 <+366>:	je     0x40077a <main+388>
		   0x0000000000400766 <+368>:	mov    edi,0x40088f				# This one is the congrats message and the desired exit
		   0x000000000040076b <+373>:	call   0x4004a0 <puts@plt>
		   0x0000000000400770 <+378>:	mov    edi,0x0
		   0x0000000000400775 <+383>:	call   0x4004e0 <exit@plt>			# until here
		   0x000000000040077a <+388>:	mov    edi,0x40089d				# Everything from here and below are "bad exits" we want to avoid!
		   0x000000000040077f <+393>:	call   0x4004a0 <puts@plt>
		   0x0000000000400784 <+398>:	mov    edi,0x1
		   0x0000000000400789 <+403>:	call   0x4004e0 <exit@plt>
		   0x000000000040078e <+408>:	mov    edi,0x4008ab
		   0x0000000000400793 <+413>:	call   0x4004a0 <puts@plt>
		   0x0000000000400798 <+418>:	mov    edi,0x1
		   0x000000000040079d <+423>:	call   0x4004e0 <exit@plt>
		   0x00000000004007a2 <+428>:	mov    edi,0x4008ab
		   0x00000000004007a7 <+433>:	call   0x4004a0 <puts@plt>
		   0x00000000004007ac <+438>:	mov    edi,0x1
		   0x00000000004007b1 <+443>:	call   0x4004e0 <exit@plt>
		   0x00000000004007b6 <+448>:	mov    edi,0x4008ab						
		   0x00000000004007bb <+453>:	call   0x4004a0 <puts@plt>				
		   0x00000000004007c0 <+458>:	mov    edi,0x1
		   0x00000000004007c5 <+463>:	call   0x4004e0 <exit@plt>				
		End of assembler dump.
		gdb-peda$ 




## Input to array

The array insertion in the first loop looks like the following with the input *1234* :

	gdb-peda$ x/8x 0x601060
	0x601060 <array>:	0x0000000200000001	0x0000000400000003
	0x601070 <array+16>:	0x0000000000000000	0x0000000000000000
	
Each byte of the input was inserted into the array, starting with the most significant bit from the input (1) at the lowest array position.
Each byte has a full 8 byte if space in the array.



## Calculating the 2nd input byte!

		   0x00000000004006ed <+247>:	mov    eax,DWORD PTR [rip+0x200971]        # 0x601064 <array+4>
		   0x00000000004006f3 <+253>:	neg    eax
		   0x00000000004006f5 <+255>:	mov    edx,eax
		   0x00000000004006f7 <+257>:	mov    eax,DWORD PTR [rip+0x200967]        # 0x601064 <array+4>
		   0x00000000004006fd <+263>:	add    eax,0x1
		   0x0000000000400700 <+266>:	and    eax,edx
		   0x0000000000400702 <+268>:	and    eax,0x4
		   0x0000000000400705 <+271>:	test   eax,eax
		   0x0000000000400707 <+273>:	je     0x4007a2 <main+428>
		   
This snipped from the above code block is used to calculate the 2nd input byte.
So First we load our 2nd provided digit into EAX.
Next up we negate that number in a `0 - EAX` manner and put the result into EDX.
Then we load our original 2nd input byte again and add 1 to it.

The next instruction is the "gimmick" of this binary !
Let's see what we can do here.
We have to provide a number, between 1 and 9 to pass all prior checks!


If we negate any possible number our 2nd input byte maps to following (only least significant bit is important):

- 1 -> f -> 1111
- 2 -> e -> 1110
- 3 -> d -> 1101
- 4 -> c -> 1110
- 5 -> b -> 1011
- 6 -> a -> 1010
- 7 -> 9 -> 1001
- 8 -> 8 -> 1000
- 9 -> 7 -> 0111

So if we provide a 1 as our 2nd input byte we get an f in this step and so on..


So next up our 2nd input is pulled back into EAX again and 1 is added.
This corresponds to the following possible mapping: 

- 1 -> 2 -> 0010
- 2 -> 3 -> 0011
- 3 -> 4 -> 0100
- 4 -> 5 -> 0101
- 5 -> 6 -> 0110
- 6 -> 7 -> 0111
- 7 -> 8 -> 1000
- 8 -> 9 -> 1001
- 9 -> a -> 1010


Then the 2nd input byte +1 is compared bitwise  to the negative version of our 2nd input byte.
The result of that comparison resides in EAX.

Directly following is another `AND eax, 0x4` and the result from this is self tested against with `TEST eax, eax`.

So we need to find an appropriate input, which can pass this testing chain resulting in the `TEST eax, eax` not setting the zero flag so the jump equal can take place!



This can only be the case if the 2nd input is 3 OR 4!
Let's see why.

Let's visualize this with the 2nd input being 3:

0x3 gets negated to 0xfffffffd, from which only the LSB is relevant so 0xd.
0xd corresponds to 1101 in binary.
If we do the first `and` operation now we have:

            1101 (0xd)
	AND	0100 (0x3 +1)
		_____________
		0100 (0x4)

So the result for that is 0100. Next up follows `and eax, 0x4`. We can rewrite this as `and 0x4, 0x4`. Why?
Because the EAX there is the result of bitwise and operation with the negated 2nd input and the 2nd input +1.
Hence `and 0x4, 0x4` obviously results in 0x4 again, which let's us pass the following `TEST EAX, EAX` check.


The same math can be done if our input for the 2nd byte is 4. Check it yourselfs :) !



## Calculating the 3th input byte!

The calculation is the same procedure as in the 2nd input byte.
Also we have an additional restriction/hint that the number cannot be an 5 or 6.

For this 3rd input byte 

- 1 -> f -> 1111
- 2 -> e -> 1110
- 9 -> 7 -> 0111


When we  do the bitwise and between the negative input value and with input+1 we get:

	1+1 =   0010   	           2+1 =    0011  		9+1 = 	 1010
	    AND 1111       		AND 1110     		     AND 0111
	  	________     		    ______      		______
	   	0010        	 	    0010        		 0010


All these inputs result in an EAX of 0x2, which let's us pass the following `and eax, 0x2` and `test eax, eax` check.
same!


## Calculating the 4th input byte!

Once again the same calculation routine as two times before.
I'll cut it short this time. an input of 7 let's us pass the following check


## MISC notes
A few notes for the assembly above:

> Note: TEST sets the zero flag ZF, when the result of the bitwise AND operation is zero. If two operands are equal their bitwise AND is zero *only* when both are zero...
TEST also sets the sign flag SF, when the most significant bit is set in the result and the parity flag PF, when the number of set bits is even.


In the case here we do TEST EAX,EAX on our input bytes, the result will never be 0, except we enter a 0 of course. 
The following Jump Sign (JS) will just take place if the most significant bit is set after the TEST operation, meaning the result of that is negative.

> Jump if Equals (JE) tests the zero flag and jumps if the flag is set. JE is an alias of JZ [Jump if Zero] so the disassembler cannot select one based on the opcode. JE is named such because the zero flag is set if the arguments to CMP are equal.



## password

5[3,4][1,2,9]7


	$ ./bin 5317
	Congrats man!


