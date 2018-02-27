## Preface
Yo!
Life kept me more than busy, but now I've got a little more time on my hands.
I decided to do a write up on the following binary, because it taught me some new things,
compared to the easy reversemes I did before.
Furthermore it showed my that I get rusty with reversing really fast... :(


#### Required Skills

* gdb
* reading disassembly dump
* basic understanding of stack overflows
* scripting

####  Binary download
The binary can be found in this repo.


### Initial Analysis

It's a 32-bit ELF binary, not stripped. So far nothing interesting pops up.

`$ file bomb
bomb: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.15, BuildID[sha1]=e6a360ee322cefe6f3bb6110b5b587bc891d08fe, not stripped`

### First run

It's a multi stage binary with 4 phases.

![run]()

## Analysis

### Phase1 - Yellow

This one was really simple, even for the start.
I loaded the binary in binaryninja and took a look at the yellow routine.
Everything before that was rather uninteresting.
For the sake of easiness here the gdb dump :) : 

    gdb-peda$ disassemble yellow
    Dump of assembler code for function yellow:
       0x08049719 <+0>:	push   ebp
       0x0804971a <+1>:	mov    ebp,esp
       0x0804971c <+3>:	sub    esp,0x8
       0x0804971f <+6>:	call   0x80496e8 <yellow_preflight>
       0x08049724 <+11>:	movzx  eax,BYTE PTR ds:0x804c24c
       0x0804972b <+18>:	cmp    al,0x38
       0x0804972d <+20>:	jne    0x804977c <yellow+99>
       0x0804972f <+22>:	movzx  eax,BYTE PTR ds:0x804c24d
       0x08049736 <+29>:	cmp    al,0x34
       0x08049738 <+31>:	jne    0x804977c <yellow+99>
       0x0804973a <+33>:	movzx  eax,BYTE PTR ds:0x804c24e
       0x08049741 <+40>:	cmp    al,0x33
       0x08049743 <+42>:	jne    0x804977c <yellow+99>
       0x08049745 <+44>:	movzx  eax,BYTE PTR ds:0x804c24f
       0x0804974c <+51>:	cmp    al,0x37
       0x0804974e <+53>:	jne    0x804977c <yellow+99>
       0x08049750 <+55>:	movzx  eax,BYTE PTR ds:0x804c250
       0x08049757 <+62>:	cmp    al,0x31
       0x08049759 <+64>:	jne    0x804977c <yellow+99>
       0x0804975b <+66>:	movzx  eax,BYTE PTR ds:0x804c251
       0x08049762 <+73>:	cmp    al,0x30
       0x08049764 <+75>:	jne    0x804977c <yellow+99>
       0x08049766 <+77>:	movzx  eax,BYTE PTR ds:0x804c252
       0x0804976d <+84>:	cmp    al,0x36
       0x0804976f <+86>:	jne    0x804977c <yellow+99>
       0x08049771 <+88>:	movzx  eax,BYTE PTR ds:0x804c253
       0x08049778 <+95>:	cmp    al,0x35
       0x0804977a <+97>:	je     0x804978b <yellow+114>
       0x0804977c <+99>:	mov    eax,ds:0x804c124
       0x08049781 <+104>:	shl    eax,0xa
       0x08049784 <+107>:	mov    ds:0x804c124,eax
       0x08049789 <+112>:	jmp    0x80497a1 <yellow+136>
       0x0804978b <+114>:	mov    DWORD PTR [esp],0x804a1f4
       0x08049792 <+121>:	call   0x80487b4 <puts@plt>
       0x08049797 <+126>:	mov    DWORD PTR ds:0x804c124,0x0
       0x080497a1 <+136>:	leave
       0x080497a2 <+137>:	ret
    End of assembler dump.
    gdb-peda$

This basically reads in your input from stdin after selecting 'yellow' and compares it character for character with a "fixed" sequence.
So Just convert all these 0x3Y values to ASCII and enter it as a password.

**Note:** If you're using IDA you can select the hex values and press 'R' to directly convert them in IDA!  


![yellow_done]()


### Phase 2 - Green

So next up to the next phase. Same routine again. Let's first look at the disassembly

    gdb-peda$ disassemble green
    Dump of assembler code for function green:
       0x08049904 <+0>:	push   ebp
       0x08049905 <+1>:	mov    ebp,esp
       0x08049907 <+3>:	sub    esp,0x38
       0x0804990a <+6>:	mov    eax,gs:0x14
       0x08049910 <+12>:	mov    DWORD PTR [ebp-0x4],eax
       0x08049913 <+15>:	xor    eax,eax
       0x08049915 <+17>:	mov    DWORD PTR [ebp-0x8],0x1
       0x0804991c <+24>:	lea    eax,[ebp-0x14]
       0x0804991f <+27>:	mov    DWORD PTR [esp],eax
       0x08049922 <+30>:	call   0x80498d4 <green_preflight>
       0x08049927 <+35>:	mov    DWORD PTR [esp+0x8],0x8
       0x0804992f <+43>:	lea    eax,[ebp-0x14]
       0x08049932 <+46>:	mov    DWORD PTR [esp+0x4],eax
       0x08049936 <+50>:	mov    DWORD PTR [esp],0x804a2c0
       0x0804993d <+57>:	call   0x80487d4 <strncmp@plt>
       0x08049942 <+62>:	test   eax,eax
       0x08049944 <+64>:	jne    0x804998e <green+138>
       0x08049946 <+66>:	mov    DWORD PTR [esp],0x804a2fc
       0x0804994d <+73>:	call   0x80487b4 <puts@plt>
       0x08049952 <+78>:	mov    eax,DWORD PTR [ebp-0x8]
       0x08049955 <+81>:	and    eax,0x1
       0x08049958 <+84>:	test   eax,eax
       0x0804995a <+86>:	sete   al
       0x0804995d <+89>:	movzx  eax,al
       0x08049960 <+92>:	mov    DWORD PTR [ebp-0x8],eax
       0x08049963 <+95>:	mov    DWORD PTR [esp],0x7a120
       0x0804996a <+102>:	call   0x8048724 <usleep@plt>
       0x0804996f <+107>:	mov    DWORD PTR [esp],0x804a33c
       0x08049976 <+114>:	call   0x80487b4 <puts@plt>
       0x0804997b <+119>:	mov    eax,DWORD PTR [ebp-0x8]
       0x0804997e <+122>:	and    eax,0x1
       0x08049981 <+125>:	test   eax,eax
       0x08049983 <+127>:	sete   al
       0x08049986 <+130>:	movzx  eax,al
       0x08049989 <+133>:	mov    DWORD PTR [ebp-0x8],eax
       0x0804998c <+136>:	jmp    0x804999a <green+150>
       0x0804998e <+138>:	mov    eax,ds:0x804c12c
       0x08049993 <+143>:	add    eax,eax
       0x08049995 <+145>:	mov    ds:0x804c12c,eax
       0x0804999a <+150>:	mov    eax,DWORD PTR [ebp-0x8]
       0x0804999d <+153>:	test   eax,eax
       0x0804999f <+155>:	jne    0x80499ad <green+169>
       0x080499a1 <+157>:	mov    eax,ds:0x804c12c
       0x080499a6 <+162>:	sar    eax,1
       0x080499a8 <+164>:	mov    ds:0x804c12c,eax
       0x080499ad <+169>:	mov    eax,DWORD PTR [ebp-0x4]
       0x080499b0 <+172>:	xor    eax,DWORD PTR gs:0x14
       0x080499b7 <+179>:	je     0x80499be <green+186>
       0x080499b9 <+181>:	call   0x8048784 <stack_chk_fail@plt>
       0x080499be <+186>:	leave
       0x080499bf <+187>:	ret
    End of assembler dump.
    gdb-peda$


#### Phase2 - Green - Points of interest

    0x08049936 <+50>:	mov    DWORD PTR [esp],0x804a2c0
    0x0804993d <+57>:	call   0x80487d4 <strncmp@plt>

First one is here!
We have a suspicious looking address loaded into ESP with a following strncmp.
Let's check whats stored at this address:

    gdb-peda$ x/s 0x804a2c0
    0x804a2c0 <password>:	"dcaotdae"

This looks pretty specific! Another password? Let's check it:

![green_over]()  

So something is not right here..
The password is correct but not accepted as is..
Back to the drawing board...

I looked at the disassembly dump but couldn't make much sense out of it..
Until I dug deeper into the internals.

So to summarize it:


* the subroutine "green_preflight" is reading 20 bytes of input into a buffer
* strncmp compares up to 'n' specified characters from two provided strings.
* strncmp returns 0 if this comparison yields s1 is similar to s2
* len(s1) = ('dcaotdae') = 8d
* right before the strncmp call a 0x8 is pushed into ESP+8, which is the 'n' I mentioned earlier

This means the fixed string we found, which has a length of 8 is compared to our input for 8 characters.
From that it results that the strncmp yields 0 for the following too:

* s1 = dcaotdae
* s2 = dcaotdaeAAA

##### How does this help us?
It doesn't..... Yet!

If we continue checking this function after a successful strncmp, we can find the following:

A value is moved into eax and then AND'ed with 1 followed by test to check if eax results in 0!
A few instructions earlier this pushed value to EAX was set to 1!

So to make this text less confusing:

* We have a value set to 1 at the beginning of the green function. Let that be 'FLAG'
* This FLAG is copied into eax
* We use AND eax, 1 => the result is stored in eax again
* Next we use TEST eax, eax
* Followed by a sete al

=> the TEST instruction performs a bitwise AND on two operands.
=> The flags SF, ZF, PF are modified while the result of the AND is discarded.

`TEST sets the zero flag, ZF, when the result of the AND operation is zero. If two operands are equal, their bitwise AND is zero when both are zero.
TEST also sets the sign flag, SF, when the most significant bit is set in the result, and the parity flag, PF, when the number of set bits is even.`

So here we do the following:

    mov eax, flag   ; eax set to 1
    and eax, 1      ; yields 1
    test eax, eax   ; doesn't set any flag
    sete al         ; eax = 0 because it sets the byte in the operand to 1 if ZF is set, otherwise sets the operand to 0.

This happens two times in a row, which basically is the "override" mechanism.
Then at the end, depending on the value in flag, the outcome is determined.
If flag is 0 we solved this level,
If it is 1, like it is when we enter "dcaotdae" to solve this level, our answer is not accepted!

#### So what now man...?

Okay to make the long story short. I downloaded not a simple crackme but rather an "exploitme".
So to solve this level we have to override the flag to 0!
I didn't put any time into solving these yet so I took long to find this out...
On top of that I couldn't find a solution in bninja.
So I decided to take a look at this in IDA.

I won't show the disassembly here again, since it pretty much looks the same.
Anyway after I found out I can view the positions of variables of a function on the stack I solved this level.

![ida_stack]()

**Summary**

* We need 0 in the flag
* we read 20 bytes into the buffer
* flag is at an offset of 12 bytes from the buffer.

Therefore, if we write 12 bytes into the buffer, the null terminator will overflow into the flag and make it zero!

![green_done]()


### Phase3 - Blue


First let's take a look at the disassembly:


    gdb-peda$ disassemble blue
    Dump of assembler code for function blue:
       0x080499f1 <+0>:	push   ebp
       0x080499f2 <+1>:	mov    ebp,esp
       0x080499f4 <+3>:	sub    esp,0x18
       0x080499f7 <+6>:	call   0x80499c0 <blue_preflight>
       0x080499fc <+11>:	mov    DWORD PTR [ebp-0x4],0x804c160     ; 'graph'
       0x08049a03 <+18>:	mov    eax,DWORD PTR [ebp-0x4]
       0x08049a06 <+21>:	mov    eax,DWORD PTR [eax+0x4]
       0x08049a09 <+24>:	mov    DWORD PTR [ebp-0x8],eax
       0x08049a0c <+27>:	mov    DWORD PTR [ebp-0xc],0x0
       0x08049a13 <+34>:	jmp    0x8049a84 <blue+147>
       0x08049a15 <+36>:	mov    DWORD PTR [ebp-0x10],0x0
       0x08049a1c <+43>:	mov    eax,DWORD PTR [ebp-0xc]
       0x08049a1f <+46>:	movzx  eax,BYTE PTR [eax+0x804c24c]
       0x08049a26 <+53>:	movsx  eax,al
       0x08049a29 <+56>:	mov    DWORD PTR [ebp-0x14],eax
       0x08049a2c <+59>:	cmp    DWORD PTR [ebp-0x14],0x4c         ; 'L'
       0x08049a30 <+63>:	je     0x8049a40 <blue+79>
       0x08049a32 <+65>:	cmp    DWORD PTR [ebp-0x14],0x52         ; 'R'
       0x08049a36 <+69>:	je     0x8049a4a <blue+89>
       0x08049a38 <+71>:	cmp    DWORD PTR [ebp-0x14],0xa          ; 'line feed'
       0x08049a3c <+75>:	je     0x8049a55 <blue+100>
       0x08049a3e <+77>:	jmp    0x8049a5e <blue+109>
       0x08049a40 <+79>:	mov    eax,DWORD PTR [ebp-0x4]
       0x08049a43 <+82>:	mov    eax,DWORD PTR [eax]
       0x08049a45 <+84>:	mov    DWORD PTR [ebp-0x4],eax
       0x08049a48 <+87>:	jmp    0x8049a71 <blue+128>
       0x08049a4a <+89>:	mov    eax,DWORD PTR [ebp-0x4]
       0x08049a4d <+92>:	mov    eax,DWORD PTR [eax+0x8]
       0x08049a50 <+95>:	mov    DWORD PTR [ebp-0x4],eax
       0x08049a53 <+98>:	jmp    0x8049a71 <blue+128>
       0x08049a55 <+100>:	mov    DWORD PTR [ebp-0x10],0x1
       0x08049a5c <+107>:	jmp    0x8049a71 <blue+128>
       0x08049a5e <+109>:	mov    DWORD PTR [ebp-0x10],0x1
       0x08049a65 <+116>:	mov    DWORD PTR [esp],0x804a3bb        ; 'boom'
       0x08049a6c <+123>:	call   0x80487b4 <puts@plt>             ; print boom stuff
       0x08049a71 <+128>:	cmp    DWORD PTR [ebp-0x10],0x0         ; from here on down a lot of stuff happens to eax
       0x08049a75 <+132>:	jne    0x8049a8a <blue+153>             
       0x08049a77 <+134>:	mov    eax,DWORD PTR [ebp-0x4]
       0x08049a7a <+137>:	mov    eax,DWORD PTR [eax+0x4]
       0x08049a7d <+140>:	xor    DWORD PTR [ebp-0x8],eax          ; manipulating of eax
       0x08049a80 <+143>:	add    DWORD PTR [ebp-0xc],0x1
       0x08049a84 <+147>:	cmp    DWORD PTR [ebp-0xc],0xe
       0x08049a88 <+151>:	jle    0x8049a15 <blue+36>
       0x08049a8a <+153>:	mov    DWORD PTR [esp],0x804a3c0
       0x08049a91 <+160>:	call   0x8048744 <printf@plt>
       0x08049a96 <+165>:	mov    eax,ds:0x804c240
       0x08049a9b <+170>:	mov    DWORD PTR [esp],eax
       0x08049a9e <+173>:	call   0x8048734 <fflush@plt>
       0x08049aa3 <+178>:	mov    DWORD PTR [esp],0x1
       0x08049aaa <+185>:	call   0x80487a4 <sleep@plt>
       0x08049aaf <+190>:	mov    DWORD PTR [esp],0x804a3eb
       0x08049ab6 <+197>:	call   0x80487b4 <puts@plt>
       0x08049abb <+202>:	mov    DWORD PTR [esp],0x7a120
       0x08049ac2 <+209>:	call   0x8048724 <usleep@plt>
       0x08049ac7 <+214>:	mov    eax,ds:0x804a384             ; comparison of eax to "0x40475194"@0x804a384  
       0x08049acc <+219>:	cmp    DWORD PTR [ebp-0x8],eax
       0x08049acf <+222>:	jne    0x8049aec <blue+251>
       0x08049ad1 <+224>:	mov    DWORD PTR [esp],0x804a3fc
       0x08049ad8 <+231>:	call   0x80487b4 <puts@plt>
       0x08049add <+236>:	mov    eax,ds:0x804c140
       0x08049ae2 <+241>:	sub    eax,0x1
       0x08049ae5 <+244>:	mov    ds:0x804c140,eax
       0x08049aea <+249>:	jmp    0x8049af9 <blue+264>
       0x08049aec <+251>:	mov    eax,ds:0x804c140
       0x08049af1 <+256>:	add    eax,0x1
       0x08049af4 <+259>:	mov    ds:0x804c140,eax
       0x08049af9 <+264>:	leave  
       0x08049afa <+265>:	ret    
    End of assembler dump.
    gdb-peda$


Right at the start there's an interesting instruction:

       0x080499fc <+11>:	mov    DWORD PTR [ebp-0x4],0x804c160

* If we take a look at this in IDA the address 0x804c160 is translated to "graph"!

This L(eft) and R(ight) thing made me think of something like a node in a tree structure.

One thing I learned through research here
One can create such a custom data structure in IDA with **SHIFT+F9**:

![ida_struct]()  

Then select the memory address range you want to convert to that newly added data structure and press **ALT+Q**.
This can organize the disassembly a lot more if needed.
Anyway the decompilation helped me more here and looks something like this:

    int blue()
    {
      int result; // eax@13
      int v1; // [sp+4h] [bp-14h]@2
      signed int v2; // [sp+8h] [bp-10h]@2
      signed int i; // [sp+Ch] [bp-Ch]@1
      void *node_value; // [sp+10h] [bp-8h]@1
      void **node; // [sp+14h] [bp-4h]@1

      blue_preflight();
      node = graph;
      node_value = graph[1];
      for ( i = 0; i <= 14; ++i )
      {
        v2 = 0;
        v1 = *(&buffer + i);
        switch ( v1 )
        {
          case 76:
            node = (void **)*node;
            break;
          case 82:
            node = (void **)node[2];
            break;
          case 10:
            v2 = 1;
            break;
          default:
            v2 = 1;
            puts("boom");
            break;
        }
        if ( v2 )
          break;
        node_value = (void *)((unsigned int)node[1] ^ (unsigned int)node_value);
      }
      printf("\x1B[46m \x1B[0m\x1B[36m PROGRAMMING GATE ARRAY... ");
      fflush(stdout);
      sleep(1u);
      puts("SUCCEEDED\x1B[0m");
      usleep(0x7A120u);
      if ( node_value == (void *)solution )
      {
        puts("\x1B[46m \x1B[0m\x1B[36m VOLTAGE REROUTED FROM REMOTE DETONATION RECEIVER \x1B[0m");
        result = wire_blue-- - 1;
      }
      else
      {
        result = wire_blue++ + 1;
      }
      return result;
    }

      **


So basically this level reads a 15 byte buffer and performs an action for each character of the buffer.
The allowed characters are 'L', 'R', and '\n'.
This yields:

* If it encounters an ‘L’, it goes to the node pointed to by Node->left.
* If it encounters an ‘R’, it goes to the node pointed to by Node->right.
* If it encounters a newline (‘\n’), it stops.
* For each iteration, it xors the current Node->value with the first nodes value.


So we have to find a sequence of L’s and R’s which results in the correct final value of 0x40475194.
This can easily be done in IDA with an IDAPython script to brute force a possible combination.
Basically it is just a python script, which can be directly run in IDA via **ALT+F7**:

    '''The number of possible combinations is 14 L or R’s because 1 byte is for ‘\n’ and the final byte for the string terminator, therefore 2^14 which is 16384 possible combinations.'''
    def evaluate(string):
        ea = 0x0804c160
        x = 0x47bbfa96

        for i in string:
            if i == 'L':
                ea = Dword(ea)

            if i == 'R':
                ea = Dword(ea+8)

            if i == '\n':
                break

            x = Dword(ea+4) ^ x

        return x

    ans = 0x40475194

    for i in xrange(2 ** 14):
        string = ''.join(map(lambda a: 'L' if int(a) else 'R', bin(i)[2:]))
        if evaluate(string) == ans:
            print string

This outputs a ton of combinations, which I don't wanna copy & paste here.
One possible solution to finish this phase is 'LLRR'.

![blue_done]()  



### Phase4 - Red

If you made it up to here: Welcome to the last Phase!
Don't worry this one is way shorter.
We will be done soon!


    gdb-peda$ disassemble red
    Dump of assembler code for function red:
       0x08049831 <+0>:	push   ebp
       0x08049832 <+1>:	mov    ebp,esp
       0x08049834 <+3>:	sub    esp,0x18
       0x08049837 <+6>:	call   0x80497a4 <red_preflight>
       0x0804983c <+11>:	mov    DWORD PTR [ebp-0x4],0x804a29c       ; ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
       0x08049843 <+18>:	mov    DWORD PTR [ebp-0x8],0x0
       0x0804984a <+25>:	jmp    0x80498ba <red+137>
       0x0804984c <+27>:	mov    eax,DWORD PTR [ebp-0x8]
       0x0804984f <+30>:	movzx  edx,BYTE PTR [eax+0x804c24c]
       0x08049856 <+37>:	mov    eax,ds:0x804c26c
       0x0804985b <+42>:	and    eax,0x1f
       0x0804985e <+45>:	add    eax,DWORD PTR [ebp-0x4]
       0x08049861 <+48>:	movzx  eax,BYTE PTR [eax]
       0x08049864 <+51>:	cmp    dl,al
       0x08049866 <+53>:	je     0x8049877 <red+70>
       0x08049868 <+55>:	mov    eax,ds:0x804c128
       0x0804986d <+60>:	add    eax,0x1
       0x08049870 <+63>:	mov    ds:0x804c128,eax
       0x08049875 <+68>:	jmp    0x80498ca <red+153>
       0x08049877 <+70>:	mov    eax,ds:0x804c26c
       0x0804987c <+75>:	mov    edx,eax
       0x0804987e <+77>:	shr    edx,0x5
       0x08049881 <+80>:	mov    eax,ds:0x804c268
       0x08049886 <+85>:	shl    eax,0x1b
       0x08049889 <+88>:	or     eax,edx
       0x0804988b <+90>:	mov    ds:0x804c26c,eax
       0x08049890 <+95>:	mov    eax,ds:0x804c268
       0x08049895 <+100>:	mov    edx,eax
       0x08049897 <+102>:	shr    edx,0x5
       0x0804989a <+105>:	mov    eax,ds:0x804c264
       0x0804989f <+110>:	shl    eax,0x1b
       0x080498a2 <+113>:	or     eax,edx
       0x080498a4 <+115>:	mov    ds:0x804c268,eax
       0x080498a9 <+120>:	mov    eax,ds:0x804c264
       0x080498ae <+125>:	shr    eax,0x5
       0x080498b1 <+128>:	mov    ds:0x804c264,eax
       0x080498b6 <+133>:	add    DWORD PTR [ebp-0x8],0x1
       0x080498ba <+137>:	cmp    DWORD PTR [ebp-0x8],0x12
       0x080498be <+141>:	jle    0x804984c <red+27>
       0x080498c0 <+143>:	mov    DWORD PTR ds:0x804c128,0x0
       0x080498ca <+153>:	leave  
       0x080498cb <+154>:	ret    
    End of assembler dump.
    gdb-peda$

As one can see in the dump above we have a bunch of shift lefts, shift rights as well as and's in there.


![pred]()  

The decompilation of the function looks like this:

    unsigned int red()
    {
      unsigned int result; // eax@1
      signed int i; // [sp+10h] [bp-8h]@1

      result = red_preflight();
      for ( i = 0; i <= 18; ++i )
      {
        if ( *(&buffer + i) != aAbcdefghjklmnp[r2 & 0x1F] )
          return wire_red++ + 1;
        r2 = ((unsigned int)r2 >> 5) | (r1 << 27);
        r1 = ((unsigned int)r1 >> 5) | (r0 << 27);
        result = (unsigned int)r0 >> 5;
        r0 = (unsigned int)r0 >> 5;
      }
      wire_red = 0;
      return result;
    }

    **

red_preflight calls rand() three times without seeding the random number generator which results in the same values.
These values are used to fill an array r[3].
We can write a python script to solve this riddle once again:


    data_set = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

    r = [0x6B8B4567, 0x327B23C6, 0x643C9869]
    c = ""

    for i in range(19):
        c += data_set[r[2] & 0x1f]
        r[2] = (r[2] >> 5) | (r[1] << 27)
        r[1] = (r[1] >> 5) | (r[0] << 27)
        result = r[0] >> 5
        r[0] = r[0] >> 5

    print(c)

.

    $ python ./red_solve.py
    KDG3DU32D38EVVXJM64

 
![red_done]()  




## Final words
I found this binary and thought it was a simple reverseme, which I wanted to do first to get back on track.
It turned out this thing was more of a exploitme which brought me closer to IDA!
It was fun trying things out, but in the end it showed me a couple of things:

* I'm a scrub
* I need to learn IDA along the way
* Exploiting is something I'd like to know more about but don't know jack shit about

