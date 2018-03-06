## binary 

	$ file ./crackme0x00 
	./crackme0x00: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.9, not stripped
----
	$ ./crackme0x00 
	IOLI Crackme Level 0x00
	Password: asdf
	Invalid Password!


## solution

As an entry challenge this one doesn't pose much of a challenge.
A simple usage of `strings` on the binary reveals a program.

> Note: strings - print the strings of printable characters in files.



	$ strings crackme0x00 
	/lib/ld-linux.so.2
	__gmon_start__
	libc.so.6
	printf
	strcmp
	scanf
	_IO_stdin_used
	__libc_start_main
	GLIBC_2.0
	PTRh
	IOLI Crackme Level 0x00
	Password: 
	250382
	Invalid Password!
	Password OK :)
	GCC: (GNU) 3.4.6 (Gentoo 3.4.6-r2, ssp-3.4.6-1.0, pie-8.7.10)
	GCC: (GNU) 3.4.6 (Gentoo 3.4.6-r2, ssp-3.4.6-1.0, pie-8.7.10)
	GCC: (GNU) 3.4.6 (Gentoo 3.4.6-r2, ssp-3.4.6-1.0, pie-8.7.10)
	GCC: (GNU) 3.4.6 (Gentoo 3.4.6-r2, ssp-3.4.6-1.0, pie-8.7.10)
	GCC: (GNU) 3.4.6 (Gentoo 3.4.6-r2, ssp-3.4.6-1.0, pie-8.7.10)
	GCC: (GNU) 3.4.6 (Gentoo 3.4.6-r2, ssp-3.4.6-1.0, pie-8.7.10)
	GCC: (GNU) 3.4.6 (Gentoo 3.4.6-r2, ssp-3.4.6-1.0, pie-8.7.10)
	.symtab
	.strtab
	.shstrtab
	.interp
	.note.ABI-tag
	.gnu.hash
	.dynsym
	.dynstr
	.gnu.version
	.gnu.version_r
	.rel.dyn
	.rel.plt
	.init
	.text
	.fini
	.rodata
	.eh_frame
	.ctors
	.dtors
	.jcr
	.dynamic
	.got
	.got.plt
	.data
	.bss
	.comment
	crtstuff.c
	__CTOR_LIST__
	__DTOR_LIST__
	__JCR_LIST__
	completed.1
	__do_global_dtors_aux
	frame_dummy
	__CTOR_END__
	__DTOR_END__
	__FRAME_END__
	__JCR_END__
	__do_global_ctors_aux
	crackme0x00.c
	_GLOBAL_OFFSET_TABLE_
	__init_array_end
	__init_array_start
	_DYNAMIC
	data_start
	__libc_csu_fini
	_start
	__gmon_start__
	_Jv_RegisterClasses
	_fp_hw
	_fini
	__libc_start_main@@GLIBC_2.0
	_IO_stdin_used
	scanf@@GLIBC_2.0
	__data_start
	__dso_handle
	__libc_csu_init
	printf@@GLIBC_2.0
	__bss_start
	_end
	_edata
	strcmp@@GLIBC_2.0
	__i686.get_pc_thunk.bx
	main
	_init


It is kinda obvious that `250382` must be the password.


	$ ./crackme0x00
	IOLI Crackme Level 0x00
	Password: 250382
	Password OK :)
	
But why is that?
Lets take a quick look at the assembly:

	gdb-peda$ disassemble main
	Dump of assembler code for function main:
	   0x08048414 <+0>:	push   ebp
	   0x08048415 <+1>:	mov    ebp,esp
	   0x08048417 <+3>:	sub    esp,0x28
	   0x0804841a <+6>:	and    esp,0xfffffff0
	   0x0804841d <+9>:	mov    eax,0x0
	   0x08048422 <+14>:	add    eax,0xf
	   0x08048425 <+17>:	add    eax,0xf
	   0x08048428 <+20>:	shr    eax,0x4
	   0x0804842b <+23>:	shl    eax,0x4
	   0x0804842e <+26>:	sub    esp,eax
	   0x08048430 <+28>:	mov    DWORD PTR [esp],0x8048568	;move a string into esp
	   0x08048437 <+35>:	call   0x8048340 <printf@plt>		; print said string to console
	   0x0804843c <+40>:	mov    DWORD PTR [esp],0x8048581	;same stuff
	   0x08048443 <+47>:	call   0x8048340 <printf@plt>		; here again
	   0x08048448 <+52>:	lea    eax,[ebp-0x18]
	   0x0804844b <+55>:	mov    DWORD PTR [esp+0x4],eax
	   0x0804844f <+59>:	mov    DWORD PTR [esp],0x804858c	; %s for scanf is specified
	   0x08048456 <+66>:	call   0x8048330 <scanf@plt>		; scanf is called
	   0x0804845b <+71>:	lea    eax,[ebp-0x18]	; user input is stored in eax
	   0x0804845e <+74>:	mov    DWORD PTR [esp+0x4],0x804858f	; hard coded password is loaded into esp+0x4
	   0x08048466 <+82>:	mov    DWORD PTR [esp],eax	; password is loaded into esp
	   0x08048469 <+85>:	call   0x8048350 <strcmp@plt>	; string compare function takes 2 arguments esp and esp+0x4, returns 0 if equal
	   0x0804846e <+90>:	test   eax,eax		; strcmp result stored in eax, if 0 test  eax,eax yields 0
	   0x08048470 <+92>:	je     0x8048480 <main+108>	; then this jump is taken to good exit
	   0x08048472 <+94>:	mov    DWORD PTR [esp],0x8048596
	   0x08048479 <+101>:	call   0x8048340 <printf@plt>
	   0x0804847e <+106>:	jmp    0x804848c <main+120>
	   0x08048480 <+108>:	mov    DWORD PTR [esp],0x80485a9
	   0x08048487 <+115>:	call   0x8048340 <printf@plt>
	   0x0804848c <+120>:	mov    eax,0x0
	   0x08048491 <+125>:	leave  
	   0x08048492 <+126>:	ret    
	End of assembler dump.
	gdb-peda$ 


