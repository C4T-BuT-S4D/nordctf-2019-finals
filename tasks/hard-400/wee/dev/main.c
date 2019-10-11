int sigret()
{
	__asm__ __volatile__ (
		"mov $0xF, %rax\n\t"
		"syscall"
	);
};

int main()
{
	char buf[ 64 ];

	register char* ptr asm( "rsi" ) = &buf[0];

	__asm__ __volatile__ (
		"xor %rdi, %rdi\n\t"
		"mov $0x512, %rdx\n\t"
		"xor %rax, %rax\n\t"
		"syscall"
	);
};

int _start()
{
	__asm__ __volatile__ (
		"mov $37, %rax\n\t"
		"mov $60, %rdi\n\t"
		"syscall"
	);

	main();
	
	__asm__ __volatile__ (
		"mov $0x3C, %rax\n\t"
		"syscall"
	);
};

char *bin_sh = "/bin/sh\0";
