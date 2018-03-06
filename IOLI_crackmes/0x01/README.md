## binary

	$ file crackme0x01 
	crackme0x02: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.9, not stripped
----
	$ ./crackme0x01   
	IOLI Crackme Level 0x01
	Password: asdf
	Invalid Password!


## solution

The same trick with strings does not work anymore.
The password is not a printable string anymore: 

	$ strings crackme0x01 
	/lib/ld-linux.so.2
	__gmon_start__
	libc.so.6
	printf
	scanf
	_IO_stdin_used
	__libc_start_main
	GLIBC_2.0
	PTRh
	IOLI Crackme Level 0x01
	Password: 
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
	crackme0x01.c
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
	__i686.get_pc_thunk.bx
	main
	_init
	
So where is the password?

	Dump of assembler code for function main:
	   0x080483e4 <+0>:	push   ebp
	   0x080483e5 <+1>:	mov    ebp,esp
	   0x080483e7 <+3>:	sub    esp,0x18
	   0x080483ea <+6>:	and    esp,0xfffffff0
	   0x080483ed <+9>:	mov    eax,0x0
	   0x080483f2 <+14>:	add    eax,0xf
	   0x080483f5 <+17>:	add    eax,0xf
	   0x080483f8 <+20>:	shr    eax,0x4
	   0x080483fb <+23>:	shl    eax,0x4
	   0x080483fe <+26>:	sub    esp,eax
	   0x08048400 <+28>:	mov    DWORD PTR [esp],0x8048528
	   0x08048407 <+35>:	call   0x804831c <printf@plt>
	   0x0804840c <+40>:	mov    DWORD PTR [esp],0x8048541
	   0x08048413 <+47>:	call   0x804831c <printf@plt>
	   0x08048418 <+52>:	lea    eax,[ebp-0x4]
	   0x0804841b <+55>:	mov    DWORD PTR [esp+0x4],eax
	   0x0804841f <+59>:	mov    DWORD PTR [esp],0x804854c
	   0x08048426 <+66>:	call   0x804830c <scanf@plt>
	   0x0804842b <+71>:	cmp    DWORD PTR [ebp-0x4],0x149a	; not much changed cmprd to 0x00 except this
	   0x08048432 <+78>:	je     0x8048442 <main+94>
	   0x08048434 <+80>:	mov    DWORD PTR [esp],0x804854f
	   0x0804843b <+87>:	call   0x804831c <printf@plt>
	   0x08048440 <+92>:	jmp    0x804844e <main+106>
	   0x08048442 <+94>:	mov    DWORD PTR [esp],0x8048562
	   0x08048449 <+101>:	call   0x804831c <printf@plt>
	   0x0804844e <+106>:	mov    eax,0x0
	   0x08048453 <+111>:	leave  
	   0x08048454 <+112>:	ret    
	End of assembler dump.
	gdb-peda$ 


Something (our user input) is compared to 0x149a.
If we convert that hex number to an int we get 5274.

	$ ./crackme0x01 
	IOLI Crackme Level 0x01
	Password: 5274
	Password OK :)

