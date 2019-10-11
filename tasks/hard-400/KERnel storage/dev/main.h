#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>


#define MAX_LIST_ITEMS 1024
#define MAX_OWNER_SIZE 32
#define MAX_NAME_SIZE 72
#define MAX_PASSWORD_SIZE 32
#define MAX_KERNEL_DATA_BUF_SIZE 128

#define NORMAL_EXIT 1
#define ERROR_OPTION_EXIT -1
#define LOGIN_EXIT 2

#define KERNEL_STRUCT_SIZE sizeof( struct kernel )
#define ENTRY_STRUCT_SIZE sizeof( struct entry )

typedef unsigned int DWORD;
typedef unsigned short int WORD;
typedef unsigned char BYTE;

// struct size = 32 + 64 + size_t + DWORD
struct kernel {
	char owner[ MAX_OWNER_SIZE ]; // 32 
	char name[ MAX_NAME_SIZE ];  // 72
	char* data; // + 32+72 = 104
	DWORD is_blocked;
}; 

struct entry {
	struct kernel* kern;
	struct entry* next;
	struct entry* prev;
};

struct entry* head = NULL;
struct entry* cache_entry = NULL;
	
void setup( void );
void auth_menu( void );
int reg( void );
int login( void );
int kernel_storage( void );
void kernel_menu( void );
int kernel_is_exist( char* buf );

int create_kernel( void );
int edit_kernel( void );
int edit_kernel_data( void );
int delete_kernel( void );
int view_kernel( void );
int view_kernel_list( void );

void change_user_desc( void );
void view_user_description( void );

void debug_func( void );
void add_to_cache( struct entry* );
struct entry* get_cache_entry( void );

int check_is_entry_in_cache( char* KernelName );
int edit_last_kernel_data( void );