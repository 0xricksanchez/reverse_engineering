# Preface

This write up are my thoughts and steps to analyze a given unknown binary.  
I want to understand the binary to a point where I can freely write about it. So here it is.

I'm always open for you pointing out mistakes or giving feedback to me

## Disclaimer:
I won't look at the assembly code to patch my way through to the end.  
The goal will be to find the flag(s) to reach the "finish line" as it was intended.

The steps taken in the following can probably be done in a different order as well.


# Binary Analysis

## First assessment 

### Binary format
Let's take a look at the binary:

![file_cmd]()

We got a 32-bit [non stripped](https://stackoverflow.com/questions/22682151/difference-between-a-stripped-binary-and-a-non-stripped-binary-in-linux) ELF binary. 
This sounds okay, since we still have the debugging symbols available.  

### Strings

Let's run strings against it

> $ strings binary

    ....
    /lib/ld-linux.so.2
    libc.so.6
    _IO_stdin_used
    exit
    fopen
    __isoc99_sscanf
    puts
    __stack_chk_fail
    stdin
    tolower
    printf
    fgets
    strlen
    sleep
    strcmp
    ...
    Welcome to the Poly Bomb. Three levels to solve and you get a key at the completion of each level. Good Luck...
    Good Job with Phase One on to the next
    Wow you solved phase two??? On to the next
    Woot You solved the binary bomb
    Tick...Tick...Tick...
    ...
    some ASCII ART HERE
    ...
    H0Tf00D:<
    %d %d %d %d %d %d
    Key problem contact ctf-owner@isis.poly.edu
    ;*2$"
    BinaryBomb:(
    GCC: (Ubuntu/Linaro 4.7.3-1ubuntu1) 4.7.3
    .symtab
    .strtab
    .shstrtab
    ....


So at the beginning we seem to have some function strings which might get called.
We already can assume that we have to deal with different read/print and input compare functions.
Another function which stands out is **tolower**, which casts every input to lowercase.

Next we get a rough idea what we are dealing with here. 
Some kind of bomb defuse scenario ;) with 3 phases.
I intentionally omitted the ascii art since its not of major importance and would not help us reverse the binary.  

Following this we have some weird and shady looking strings we might wanna keep in mind for the next steps.

Last some binary intern strings are displayed like symbol table or string table..


#### First conclusion
From this first rough assessment we should keep in mind the following facts:

* It's a non stripped ELF binary, putting it in tools like IDA or BinaryNinja will make life easy!
* We have 3 phases, so 3 flags to find!
* since it's an ELF binary we could run **readelf -a 0x01 against it to get more information


## Second assessment

After the first recon phase we have a rough idea what we are dealing with here.
Let's fire up our favorite dissassembler and take a look at the binary.

### In depth analysis

Time for some fun in depth analysis.
Since we still have all the debugging symbols we can easily navigate through the binary.


![main_no_com]()

We can clearly see that we have 3 phases with a preceeding **readLine** which will ask for our input to solve the respective phase.
If we solved everything **win** gets called.
In the beginning a function named **sphinx** is called though..

Since I omitted the ASCII art before I will just solve the riddle of the sphinx.
This function prepares the ASCII art which is shown to us in the beginning.

>It's a gigantic question mark made out of M's if anyone was wondering/interested
______________
### Phase 1
####Static analysis


![phase1]()

Ok what do we see here.
Some address 0x804b048 is moved into ebp-0xc.
Then the same address is copied from ebp-0xc into eax, which was holding OUR input before that!
Afterwards a bunch of move and add operations are taking place.

If you're already a little bit familiar with it RE you can notice that the content that copied into eax is looked at byte for byte and each byte is changed.
This happens 6 times if you look closely.

#### Dynamic analysis
This phase isn't a big challenge.
We just have to look how the content that was copied in eax is changed before it get's compared.


![p1_in_eax]

![p1_after_changepost]

So we see that the content was "BinaryBomb:(" and it got changed to "=bJd{cBomb:(".

#### Flag 1

=bJd{cBomb:(

______________

### Phase 2

#### Static analysis


![phase2]


So next phase now.. The start is quite unspectacular. 
We read in the user input and set ebp-0x74 to 0. 
Then we compare ebp-0x74 to 0x7. If it's <= 0x7 we enter the left big code block.
When we're done with the code block we jump back to the compare statement again.
Looks familiar right?
We have a loop structure here which loops 8 times!

But what does it do?
We can see a lot of mov(zx/sx) operations, some arithmetic right shift (sar) and some
integer division(idiv) as well as a bunch of additions(add).

So let's examine the more interesting parts.

    0x080488d0	movzx 	eax, byte [eax]
    0x080488d3	mov 	ecx, eax

This basically takes the first byte of our input and saves it in ecx!

    0x080488eb  sar     edx,0x1f         // 0x1f = 31



So we do a right shift of 31 bits on edx here.
This will always zero out the edx in this case here.


**Why is that important?**

Let's take a look at the next interesting operation

    0x080488e3	mov	    ebx, dword [modulus]    // ebx is set to 10 here 
    ...
    0x080488ee	idiv 	ebx


The idiv operation looks harmless but it might be a little confusing what it actually does!

> idiv 	<ebx>
eax = eax / <ebx>
edx = edx % <ebx>

So eax holds the quotient and edx will hold the remainder after this operation.


With this in mind the following line may make more sense now

    0x080488f0	mov	    eax, edx 
    0x080488f2	add 	eax, ecx


eax holds the remainder of the integer division.
ecx is holding one byte of the input we provided and did the integer division on.
Now we're adding these.

How can we interpret this?
Basically we are doing some kind of shift/encryption of the input.
Recall that we enter this loop 8 times.
So we're changing 8 bytes of our input!

Let's briefly look at what happens after we finish looping!

    0x0804893e	 mov 	  dword [esp], 0x8049ab4
    0x08048945   call	  strcmp

So we're comparing our shifted input to something at the address 0x8049ab4
As we could already see in binary ninja, the string that lies here is **"H0Tf00D:<"**.
If we match this string we solved phase2!


**So how do we get the flag?**

2 possibilities  come to mind right away.

* First: try to map every input to the appropriate output by using dynamic analysis methods
* Second: Look at the mathematical operations done and reverse those.



I've gone with the second approach during my reversing.
Let's map "H0Tf00D:<" to the corresponding integer values:

> H = 72 = 0x48
0 = 48 = 0x30
T = 84 = 0x54
f = 102 = 0x66
D = 68 = 0x44
: = 58 = 0x3a

So why am I not mapping **"<"** ?
Look at the length of this string. It has a length of 9, but we're looping just 8 times!
So "<" will be a part of our flag. More precise it will be the last character of the flag!

After a while I found a possible solution:

> G'Me'';1<

So basically you want to take the integer values, do the full integer division and take the remainder and add it onto the integer value you did the division on.
So for example:

> "G" = 71 
71 % 10 = 1 	// ebx = 10
71 + 1 = 72 = "H"


#### Dynamic analysis

We just solved it. No need to look at it during runtime. You can do so yourself to confirm if I wasn't lying to you ;) .


#### Flag 2

G'Me'';1<

______________

### Phase 3

#### Static analysis

So as always let's take a look at the last phase for this binary!


![phase3]

At first glance phase 3 might not look much more difficult compared to phase 2.
If we look closer we can see another function call this time around though: **sanitize**.

Also we can identify 2 seperate loops. 

Let's take q quick peak at the **sanitize** function


![p3_sanitize]

So first some values are getting moved around, a **strlen** function call follows to get the length of our provided input.
When returning len(input) is stored in eax. ebx was probably set to 0 before the **strlen** call.
So it seems like we're entering the loop as many times as our input is long!

The next block seems to just check if the current input byte is not equal to 0x20 = SPACE.
When this is not the case we enter the third bigger block in the loop.
This one seems to cast the current input byte to lowercase!

As a conclusion we can note that the no matter what we input it will be casted to lower case.
We can focus on providing lower case input then in the first place!

Back in phase 3 there is another call of **strlen** for our now lower case input.
It gets pushed to [ebp-0x10] and then compared to 0x4!

    0x080489a4	mov 	dword [ebp-0x10], eax
    0x080489a7	cmp 	dword [ebp-0x10], 0x4

We can conclude another thing now.
Our input has to have a length > 4, because if its <= 4 we jump right to **explode_bomb**

Next eax is set to 0!

    0x080489b2	mov 	dowrd [ebp-0x14], 0x0
    0x080489b9	jmp	0x80489f1
    0x080489f1	mov	eax, dword [ebp-0x14]

Now we have another comparison. Eax with was freshly set to 0x0 is compared to [ebp-0x10] which is holding the length of our input.

`0x80489f4	 cmp 	eax, dword [ebp-0x10]`

If eax is < len(input) we enter the first loop. 
What happens here should be obvious by now. 
We are looping over every input byte again.

But for what reason?

#### Dynamic Analysis

I'm switching to dynamic analysis now since it will be easier to follow and show what is happening in the two loops.
I set a breakpoint right before entering the first loop.



![1stloop]

We notice that I provided ABCDefgh as input and abcdefgh is now on the stack and I passed the check against 0x4.
Our made assumptions earlier were correct up to this point.

I set another breakpoint at the compare statement:

`0x080489e3	 cmp	eax, dword [ebp-0xc]`

![p3_enter_1st_loop]

So what do we see here. 
A bunch of things, just try to follow me :) .

* eax = 0x63 = "c"
* edx = 0x2 (3rd input byte)
* addr of ebp-0xc = 0xffffd23c = 0x62 = "b"

So the third input byte is compared to the second input byte at this point.
If they are no equal we continue the loop, otherwise the bomb explodes.

If we continue until we reach this breakpoint again what do we expect to see now?
I'm sure you know already by here is the breakdown again:

* eax = 0x64 = "d"
* edx = 0x3 (4th input byte)
* addr of ebp-0xc = 0xffffd23c = 0x63 = "c"

So in the end it is getting tested if byte n is different from byte n+1.
If that's the case we finish this loop without a big bang ;) .

So onto the next loop.

I set another breakpoint at the start of it at 0x08048a20

    0x08048a20	cmp	dword [ebp-0x10], 0x1 	// cmp input length to 1
    0x08048a24	jg	0x80489fb		        // if >1 enter loop

Here we got a few more interesting statements to look at:

       0x080489fb	mov    eax, dword[ebp+0x8]		  // loads our input into eax
       0x080489fe	movzx  edx, byte [eax]			  // loads first byte of it in edx
       0x08048a01	mov    eax, dword [ebp-0x10]	  // len(input) = eax
       0x08048a04	lea    ecx, [eax-0x1]			  // len(inpit-1) = ecx
       0x08048a07	mov    eax, dword [ebp+0x8]	      // loads our input into eax again
       0x08048a0a	add    eax, ecx				      // eax looks at last input element
       0x08048a0c	movzx  eax, byte [eax]			  // set that last element as eax
       0x08048a0f	cmp    dl, al                     // see below :)
       0x08048a11	je     0x8048a18 <phase_3+161>		
       0x08048a13	call   0x8048b3b <explode_bomb>   // bang ;(
       0x08048a18	add    dword [ebp+0x8],0x1 		
       0x08048a1c	sub    dword [ebp-0x10], 0x2	  // subtract 2 of len(input)

The most important instruction to understand here is at address 0x08048a0f.
What happens here is basically this:

Compare 1st and nth element and check if equal, if yes continue
Compare 2nd and nth-1 element and check if equal, if yes continue.
...

This happens until we reach the middle element of our input and the check above with len(input) > 1 fails.
That's the conditions to leave the loop and if that happens we solved phase 3.

Let's conclude what we know!


#### Flag 3

* Has to have more than 4 characters
* In the end operations on lowercase(input) will be done
* 2 following characters must be distinct from each other
* We need a palindrome
* e.g.: abcba

So you can choose a flag on your own ;) .

______________

# Proof



![poc]

______________

# Conclusion

I hope this binary analysis was somewhat helpful and easy to understand.
I know it was a bit longer, and probably took some time to read through, but I didn't feel like splitting this little binary into 3 separate articles.
If you have any questions shoot them.


