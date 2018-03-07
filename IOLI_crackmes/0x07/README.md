## binary

	$ file crackme0x07             
	crackme0x07: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.9, stripped
	
We're dealing with a stripped binary now!


	$ ./crackme0x07 
	IOLI Crackme Level 0x07
	Password: asdf
	Password Incorrect!
	
The overall scheme has not changed tho.

## solution

	$ LOLO= ./crackme0x07
	IOLI Crackme Level 0x07
	Password: 6262
	Password OK!
	
This was exactly the same binary as in 0x06 just the stripped version, meaning all function and symbol names are replaced by an "randomized string".
In gdb this looks like the following:

	=> 0x0804867d:	push   ebp
	   0x0804867e:	mov    ebp,esp
	   0x08048680:	sub    esp,0x88
	   0x08048686:	and    esp,0xfffffff0
	   0x08048689:	mov    eax,0x0
	   0x0804868e:	add    eax,0xf
	   0x08048691:	add    eax,0xf
	   0x08048694:	shr    eax,0x4
	   0x08048697:	shl    eax,0x4
	   0x0804869a:	sub    esp,eax
	   0x0804869c:	mov    DWORD PTR [esp],0x80487d9
	   0x080486a3:	call   0x80483b8 <printf@plt>
	   0x080486a8:	mov    DWORD PTR [esp],0x80487f2
	   0x080486af:	call   0x80483b8 <printf@plt>
	   0x080486b4:	lea    eax,[ebp-0x78]
	   0x080486b7:	mov    DWORD PTR [esp+0x4],eax
	   0x080486bb:	mov    DWORD PTR [esp],0x80487fd
	   0x080486c2:	call   0x8048398 <scanf@plt>
	   0x080486c7:	mov    eax,DWORD PTR [ebp+0x10]
	   0x080486ca:	mov    DWORD PTR [esp+0x4],eax
	   0x080486ce:	lea    eax,[ebp-0x78]
	   0x080486d1:	mov    DWORD PTR [esp],eax
	   0x080486d4:	call   0x80485b9
	   0x080486d9:	mov    eax,0x0
	   0x080486de:	leave  
	   0x080486df:	ret    


This is the main function as before, but as you might notice the function call to "check" at `0x080486d4` is now just a mere jump to an addres without any nice label next to it.
