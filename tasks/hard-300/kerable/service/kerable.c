#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>


int login() {
    char username[128];
    char password[128];

    puts("[?] Please, enter username:");
    scanf("%128s", username);
    getchar();

    puts("[?] Please, enter password:");
    scanf("%128s", password);
    getchar();

    if (strcmp(username, "ker") || 
        strcmp(password, "sup3r_$eCre7_h34p_p@s$w()rD"))
        puts("[-] Invalid login.");
    else
        puts("[+] Hmm. Login is correct, but I still don't trust you. Good bye!");

    return 0;
}


void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}


int main(int argc, char** argv, char** envp) {
    setup();

    login();
    
    return 0;
}
