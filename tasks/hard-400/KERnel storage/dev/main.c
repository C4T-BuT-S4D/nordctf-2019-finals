#include "main.h"

char username[ MAX_OWNER_SIZE ];
char password[ MAX_PASSWORD_SIZE ];
char *user_description = NULL;

int main( int argc, char* argv[], char* envp[] )
{
	setup();

	while ( 1 )
	{
		puts( "----- KERnel storage -----" );
		auth_menu();

		int option;
		scanf( "%d", &option );

		switch( option )
		{
			case 1:
				login();
				exit( LOGIN_EXIT );
			case 2:
				reg();
				break;
			case 3:
				exit( -1 );
				break;
			default:
				exit( ERROR_OPTION_EXIT );
		}
	}

	return 0;
};

void setup( void )
{
	setvbuf( stdout, 0, 2, 0 );
  	setvbuf( stderr, 0, 2, 0 );
  	setvbuf( stdin,  0, 2, 0 );

  	alarm( 10 );
};

void auth_menu( void )
{
	puts( "[1] Login" );
	puts( "[2] Register" );
	puts( "[3] Exit" );
	printf( "> " );
};

int login( void )
{
	char InpUsername[ MAX_OWNER_SIZE ];
	char InpPassword[ MAX_PASSWORD_SIZE ];

	printf( "[?] login: " );
	int nbytes = read( 0, InpUsername, MAX_OWNER_SIZE );

	InpUsername[ nbytes - 1 ] = '\0';

	if ( strcmp( InpUsername, username ) )
	{
		puts( "[-] login error!" );
		return 0;
	}

	printf( "[?] password: " );
	nbytes = read( 0, InpPassword, MAX_PASSWORD_SIZE );

	InpPassword[ nbytes - 1 ] = '\0';

	if ( strcmp( InpPassword, password ) )
	{
		puts( "[-] password error!" );
		return 0;
	}

	kernel_storage();

	return 1;
};

int reg( void )
{
	printf( "[?] Enter login: " );

	int nbytes = read( 0, username, MAX_OWNER_SIZE );
	username[ nbytes - 1 ] = '\0';

	printf( "[?] Enter password: " );
	
	nbytes = read( 0, password, MAX_PASSWORD_SIZE ); 
	password[ nbytes - 1 ] = '\0';

	return 1;
};

int kernel_storage( void )
{
	while ( 1 )
	{
		puts( "----- KERnel storage -----" );
		kernel_menu();

		int option;
		scanf( "%d", &option );

		switch ( option )
		{
			case 1:
				create_kernel();
				break;
			case 2:
				edit_kernel();
				break;
			case 3:
				delete_kernel();
				break;
			case 4:
				view_kernel();
				break;
			case 5:
				view_kernel_list();
				break;
			case 6:
				return NORMAL_EXIT;
				break;
			case 7:
				change_user_desc();
				break;
			case 8:
				view_user_description();
				break;
			case 9:
				edit_last_kernel_data();
				break;
			default:
				return ERROR_OPTION_EXIT;
		}
	}		
};

void kernel_menu( void )
{
	puts( "[1] Create kernel" );
	puts( "[2] Edit kernel" );
	puts( "[3] Delete kernel" );
	puts( "[4] View kernel" );
	puts( "[5] View kernel list" );
	puts( "[6] Exit" );
	printf( "> " );
};

int create_kernel( void )
{	
	// prepeare entry data
	printf( "[?] Enter kernel name: " );
	
	char TmpKernelName[ MAX_NAME_SIZE ];
	int kernel_name_size = read( 0, TmpKernelName, MAX_NAME_SIZE );
	TmpKernelName[ kernel_name_size - 1 ] = '\0';

	if ( kernel_is_exist( &TmpKernelName[ 0 ] )  )
	{
		printf( "[-] Error! Kernel with same name is exist!\n" );
		return 0;
	}

	printf( "[?] Enter kernel description (version, build, etc): " );
	
	char *TmpKernelData = (char*) malloc( MAX_KERNEL_DATA_BUF_SIZE );
	int nbytes = read( 0, TmpKernelData, MAX_KERNEL_DATA_BUF_SIZE );
	TmpKernelData[ nbytes - 1 ] = '\0';

	printf( "[?] This kernel is private (Y/N): " );

	char TmpKernelPrivBuf[ MAX_KERNEL_DATA_BUF_SIZE ];
	nbytes = read( 0, TmpKernelPrivBuf, MAX_KERNEL_DATA_BUF_SIZE );
	TmpKernelPrivBuf[ nbytes - 1 ] = '\0';

	int is_private_kernel = 0;

	if ( TmpKernelPrivBuf[ 0 ] == 'Y' )
		is_private_kernel = 1;

	struct kernel* new_kernel = (struct kernel*) malloc( KERNEL_STRUCT_SIZE );
	
	strncpy( new_kernel->owner, username, strlen( username ) );
	strncpy( new_kernel->name, TmpKernelName, kernel_name_size );
	
	new_kernel->is_blocked = is_private_kernel;
	new_kernel->data = TmpKernelData;

	struct entry* new_entry = (struct entry*) malloc( ENTRY_STRUCT_SIZE );
	new_entry->kern = new_kernel;
	new_entry->next = head;
	new_entry->prev = NULL;

	if ( head != NULL )
		head->prev = new_entry;

	head = new_entry;
	
	add_to_cache( new_entry );

	return 1;
};

int edit_kernel( void )
{
	char kernel_name[ MAX_NAME_SIZE ];
	printf( "Enter kernel name: " );

	int nbytes = read( 0, kernel_name, MAX_NAME_SIZE );
	kernel_name[ nbytes - 1 ] = '\0';

	if ( !kernel_is_exist( kernel_name ) )
	{
		printf( "[-] Error! Kernel with name <%s> is not exist!\n", 
			kernel_name );

		return 0;
	}
	
	struct entry* pHeader = NULL;

	if ( check_is_entry_in_cache( kernel_name ) )
	{
		pHeader = get_cache_entry();
	}
	else 
	{
		while ( pHeader != NULL )
		{
			if ( !strcmp( pHeader->kern->name, kernel_name ) )
			{
				if ( strcmp( pHeader->kern->owner, username ) )
				{
					puts( "[-] Error! You not owner of this kernel!" );
					return 0;
				}
				else 
				{
					break;
				}
			}

			pHeader = pHeader->next;
		}
	}

	printf( "[?] Enter new kernel description: " );
	nbytes = read( 0, pHeader->kern->data, MAX_KERNEL_DATA_BUF_SIZE );

	if ( nbytes > 0 )
		pHeader->kern->data[ nbytes - 1 ] = '\0';
	else
		return 0;
};

int delete_kernel( void )
{
	char kernel_name[ MAX_NAME_SIZE ];
	printf( "Enter kernel name: " );

	int nbytes = read( 0, kernel_name, MAX_NAME_SIZE );
	kernel_name[ nbytes - 1 ] = '\0';

	if ( !kernel_is_exist( kernel_name ) )
	{
		printf( "[-] Error! Kernel with name <%s> is not exist!\n", 
			kernel_name );

		return 0;
	}

	struct entry* pHeader = head;
	struct entry* deleted_entry = NULL;

	while ( pHeader != NULL )
	{
		if ( !strcmp( pHeader->kern->name, kernel_name ) )
		{
			if ( strcmp( pHeader->kern->owner, username ) )
			{
				puts( "[-] Error! You not owner of this kernel!" );
				return 0;
			}
			else 
			{
				deleted_entry = pHeader;
				break;
			}
		}

		pHeader = pHeader->next;
	}

	add_to_cache( deleted_entry );

	if ( deleted_entry == NULL )
		return 0;

	if ( deleted_entry == head )
		head = deleted_entry->next;
		
	if ( deleted_entry->next != NULL )
		deleted_entry->next->prev = deleted_entry->prev;

	if ( deleted_entry->prev != NULL )
		deleted_entry->prev->next = deleted_entry->next;

	free( deleted_entry->kern->data );
	free( deleted_entry->kern );
	free( deleted_entry );

	return 1;
};

int view_kernel( void )
{
	char kernel_name[ MAX_NAME_SIZE ];
	printf( "Enter kernel name: " );

	int nbytes = read( 0, kernel_name, MAX_NAME_SIZE );
	kernel_name[ nbytes - 1 ] = '\0';

	if ( !kernel_is_exist( kernel_name ) )
	{
		printf( "[-] Error! Kernel with name <%s> is not exist!\n", 
			kernel_name );

		return 0;
	}

	if ( check_is_entry_in_cache( kernel_name ) )
	{
		struct entry* pHeader = get_cache_entry();

		printf( "-- Kernel [%s] --\n", pHeader->kern->name );
		printf( "Owner: %s\n", pHeader->kern->owner );
		printf( "Desc: %s\n", pHeader->kern->data );
		printf( "Private: %d\n", pHeader->kern->is_blocked );
		puts( "------------------" );

		return 1;
	}

	struct entry* pHeader = head;

	while ( pHeader != NULL )
	{
		if ( !strcmp( pHeader->kern->name, kernel_name ) )
		{
			if ( strcmp( pHeader->kern->owner, username ) )
			{
				puts( "[-] Error! You not owner of this kernel!" );
				return 0;
			}
			else 
			{
				printf( "-- Kernel [%s] --\n", pHeader->kern->name );
				printf( "Owner: %s\n", pHeader->kern->owner );
				printf( "Desc: %s\n", pHeader->kern->data );
				printf( "Private: %d\n", pHeader->kern->is_blocked );
				puts( "------------------" );
				add_to_cache( pHeader );
			}
		}

		pHeader = pHeader->next;
	}

	return 1;
};

int view_kernel_list( void )
{
	struct entry* pHeader = head;
	int idx = 0;

	while ( pHeader != NULL )
	{
		if ( !strcmp( pHeader->kern->owner, username ) )
		{
			printf( "-- Kernel [%d] --\n", idx );
			printf( "Name: %s\n", pHeader->kern->name );
			printf( "Owner: %s\n", pHeader->kern->owner );
			printf( "Desc: %s\n", pHeader->kern->data );
			printf( "Private: %d\n", pHeader->kern->is_blocked );
			printf( "------------------\n" );

			add_to_cache( pHeader );
			idx += 1;
		}

		pHeader = pHeader->next;
	}

	if ( idx == 0 )
	{
		puts( "[?] List is empty!" );
	}

	return 1;
};

int edit_last_kernel_data( void )
{
	puts( "{!!} Warning" );
	puts( "{!!} This is untested function" );
	puts( "{!!} Be careful on use it" );


	struct entry* pHeader = get_cache_entry();
	if ( pHeader == NULL )
		return 0;

	printf( "{?} Enter new description of last used kernel: " );
	int nbytes = read( 0, pHeader->kern->data, MAX_KERNEL_DATA_BUF_SIZE );

	if ( nbytes > 0 )
		pHeader->kern->data[ nbytes - 1 ] = '\0';
	else
		return 0;

	return 1;
};

int kernel_is_exist( char* buf )
{
	struct entry* pHeader = head;

	while ( pHeader != NULL ) 
	{
		if ( !strcmp( pHeader->kern->name, buf ) )
		{	
			add_to_cache( pHeader );
			return 1;
		}

		pHeader = pHeader->next;
	}

	return 0;
};

void change_user_desc( void )
{
	puts( "{!!} Warning" );
	puts( "{!!} This is untested function" );
	puts( "{!!} Be careful on use it" );

	printf( "{?} Enter the size of description: " );
	int desc_size = 0;
	scanf( "%d", &desc_size );

	if ( desc_size != 0 && desc_size > 0 && desc_size < 1024 )
	{
		if ( user_description != NULL )
			free( user_description );

		user_description = (char*) malloc( desc_size );

		if ( user_description != NULL )
		{
			printf( "{?} Enter the new description: " );
			int nbytes = read( 0, user_description, desc_size );
			user_description[ nbytes - 1 ] = '\0';
 		}
		else
		{
			puts( "{-} Error in memory allocation!" );
		}
	}
	else
	{
		puts( "{-} Error description size!" );
	}
};

void view_user_description( void )
{
	puts( "{!!} Warning" );
	puts( "{!!} This is untested function" );
	puts( "{!!} Be careful on use it" );

	if ( user_description != NULL )
		printf( "{+} User description: %s\n", user_description );
	else
		printf( "{+} User description: NULL\n" );
};

void debug_func( void )
{
	
	long long int file = 0x006775626564;

	__asm__ __volatile__ (  
		"xor %rax, %rax\n\t" 
		"inc %rax\n\t"
		"inc %rax\n\t"
		"xor %rdx, %rdx"
	); // syscall open 2 

  	register char*    path        asm( "rdi" ) = (char*) &file;
  	register char*    flags       asm( "rsi" ) = O_RDONLY;
  
  	__asm__ __volatile__ ( 
  		"syscall\n\t"
  		"mov %rax, %rdi\n\t" 
  		"xor %rax, %rax"
  	);
 
  	register char*    buf          asm( "rsi" ) = username;
  	register int    count          asm( "rdx" ) = MAX_KERNEL_DATA_BUF_SIZE;

  	__asm__ __volatile__ (
  		"syscall\n\t" 
  		"mov %rax, %rdx\n\t"
  		"xor %rax, %rax\n\t"
  		"xor %rdi, %rdi\n\t"
  		"inc %rdi\n\t"
  		"mov %rdi, %rax\n\t" 
  		"syscall" 
  	); // syscall write 1 
};

void add_to_cache( struct entry* tmpEntry )
{
	if ( tmpEntry != NULL )
		cache_entry = tmpEntry;
};

struct entry* get_cache_entry( void )
{
	return cache_entry;
}

int check_is_entry_in_cache( char* KernelName )
{
	if ( cache_entry == NULL )
		return 0;

	if ( !strcmp( KernelName, cache_entry->kern->name ) )
		return 1;
	else
		return 0;
};