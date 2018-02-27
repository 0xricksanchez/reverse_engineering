# Preface
This is a write-up for solving the [devil-swapper RE challenge](https://0x00sec.org/t/challenge-devils-swapper/2225).
It was mostly intended for my personal archive but since it may be interesting to all of you I will try to format it in a clear and most importantly beginner friendly way for people like myself...

**important note:** The introduced tools may vary for each investigated binary. The following were just my choice for the given scenario!

Anyway let's get right into it.

# binary

### Preconditions
Building the binary obviously.

Copied from the challenge which is linked above for people who want to follow what I did:

#### building:
> cat textfile | base64 -d | gunzip > challenge && chmod +x challenge

#### textfile: 
> 
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

## First examination

### Running the file

> $./binary

>Crackme for 0x00sec
Greetings from pico!

>Keep trying...
$



Welp what did I expect..?
Running the file will only reveal that it's not working as intended :) ...

### Checking the file

> $file binary

> $binary: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, BuildID[sha1]=840893e41881866970e0e1a3bbf5673590fe803d, stripped

So I have a stripped 64-bit ELF binary to work on. 

The objective is it to find a secret key and the secret message. Whatever that means to us up to this point.
Next I want to know if there are any strings within the binary which can help me.

### Checking for strings

> $strings binary

> $AVAUATI
[A\A]A^A_]
ATUH
t9H9
w*H)
Z[]A\A]
AUATUSQL
<+=u
[]A\A]
$wFx
$V1z|D
][\A
Crackme for 0x00sec
Greetings from pico!
Keep trying...
/dev/urandom
LD_PRELOAD
valgrind
Purpx qq pbai bcgvbaf!
ntu1~14.04.3) 4.8.4
.shstrtab
.note.gnu.build-id
.text
.data
.rodata
.eh_frame
.bss
.comment
$


There is one particular string in there which could hide some valuable information or hints!
I'm talking about this boy here:

> Purpx qq pbai bcgvbaf!

No question some kind of cipher..
Since 0x00pf said it would be a simple challenge I assumed some form of [caesars ciphers](https://learncryptography.com/classical-encryption/caesar-cipher).
After trying for a while I found out it was indeed one with a keylength of k=13. 
Exactly this kind of cipher is known under a different  name as well : [ROT13](https://en.wikipedia.org/wiki/ROT13)

#### What is the decrypted text?

The answer is:

> Check dd conv options!

So here is the [dd man page](http://man7.org/linux/man-pages/man1/dd.1.html).
Let's look at the possible conv flags:

> Each CONV symbol may be:
* ascii - from EBCDIC to ASCII
* ebcdic - from ASCII to EBCDIC
* ibm  -  from ASCII to alternate EBCDIC
* block - pad newline-terminated records with spaces to cbs-size
* unblock - replace trailing spaces in cbs-size records with newline
* lcase  - change upper case to lower case
* ucase  - change lower case to upper case
* sparse - try to seek rather than write the output for NUL input blocks
* **swab  - swap every pair of input bytes**
* sync  - pad every input block with NULs to ibs-size; when used with
* excl  - fail if the output file already exists
* nocreat - do not create the output file
* notrunc - do not truncate the output file
* noerror - continue after read errors
* fdatasync - physically write output file data before finishing
* fsync - likewise, but also write metadata

Now one could associate the name of the challenge with one of the flags :p ..?

But just swapping every pair of input bytes with 

> $dd if=binary of=binary2 conv=swab 

would not make much sense would it?



## Closer look at the binary 

### Checking the binary within an analysis framework

Anyway we can examine our binary a bit more in detail here.
In this challenge I used [binary ninja](https://binary.ninja/). 
Any other tool of your choice will work as well of course.  

![bninja1](https://github.com/0x00rick/reverse_engineering/devil_swapper/images/bninja1.png)  


We can clearly see that we have a bunch of subroutines and start out with pushing and moving some values which results in the friendly greeting in the main function.
It's getting interesting after that tho!
When the cmp command get's executed we compare some content at the address `0x40051d` with `0x2ba5441`.

> In short: we compare some opcodes to a value!

Afterwards we have a jump condition.
If these compared values are not equal we jump to the branch, which displays "Keep trying". 
This results in a terminated program as we saw when running it earlier.
So the goal probably is to make it take the other route!



#### How?
By swapping only the bytes at the offset 0x40051d to not destroy the binary.

#### How much swapping has to be done?

There is this little command called:

> $readelf -flags binary

This command can show a huge amount of information about an ELF binary.
[Manpage here](https://linux.die.net/man/1/readelf)

From here we can investigate the section headers more closely.

> $readelf -S binary

![headers](https://github.com/0x00rick/reverse_engineering/devil_swapper/images/headers.png)  


If we look closely we can find the exact adress of 0x40051d again:

* .data segment
* adress: 0x30051d
* offset: 0x51d <=> 1309 bytes
* size: 0xa9 bytes <=> 169 bytes
* flags: AX (alloc, execute)

This looks weird at second glance. 
Why?
Because a data segment should hold data, not executable files!
So we can conclude this might be the obfuscated part of the binary.



# Building the new binary

We want to use dd with the conv=swab flag. 
We found out the address, the offset and the size of the segment. 
We can easily build our command now:

> $dd if=binary of=binary bs=1 count=169 skip=1309 seek=1309 conv=swab,notrunc  && chmod +x binary

This swaps exactly these bytes in our binary!

**important note:** Do not attempt to create a new binary file out of this through specifying of=new_binary!


### Let's take a look at our new binary in binary ninja

![bninja2](https://github.com/0x00rick/reverse_engineering/devil_swapper/images/bninja2.png)  

As we can see the graph changed. 
We avoided the "Keep Trying!" message for now. 
Let's see what we get when running the file.

### Running the new binary

>$./binary 
Crackme for 0x00sec
Greetings from pico!

>$ 


Wonderful we are getting greeted by the usual but this time we get a little extra too!
A brand new shell prompt!


### Finding the flag

>$./binary 
Crackme for 0x00sec
Greetings from pico!

>$ abcdefgh
5<<p?>5qqZ
$bcdefgh
bash: bcdefgh: command not found
$

#### Observation

* A first check with a random input shows us that something from our input returns some content!
* Only the first character of the input seems to be accepted.
* After getting a (broken) return value our binary terminates and our normal shell tries to execute the rest of the input


### The flag

So to find the flag one could brute force their way through now.
Only one character input gets validated. 
So around 70 possibilities should exist one can enter as input.
 We can easily bruteforce our way in..

As an alternative one can look at our graph in binary ninja and see where the input gets read & validated through some static analysis, or we tackle this problem with some dynamic analysis through gdb.
Either way sometimes [we just have to use the force](http://i.imgur.com/Kpct3BG.gif) even if it's brute force :p 

### Finish

>./binary 
Crackme for 0x00sec
Greetings from pico!

>$ 1
Well Done!!


# Conclusion
This "small and not so sophisticated" challenge was really fun diving into.
I enjoyed it a lot, even as a rookie in that area.
For people wanting to try out all of this I have a few closing words.
Just do it! I've struggled a lot too, but in the end I learned so much from this challenge.
Knowledge which I can use for my next binary I want to investigate or reverse engineer!
So just bring some time and don't give up easily :) .
Doing this is like puzzling for grown ups with a much higher frustration but also rewarding factor!
