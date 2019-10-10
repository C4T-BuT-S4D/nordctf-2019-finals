#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void show_flag() {
    FILE *fp = fopen("flag.txt", "r");
    if (fp == NULL) {
        printf ("There is no flag file.\n");
        exit(1);
    }
    char flag[36];
    fgets(flag, 37, fp);
    puts(flag);
    exit(1);
}

void incorrect(){
    puts("Incorrect :(");
    exit(1);
}

int count_dashes(char *str) {
    int amount = 0;
    for (int i = 0; i < strlen(str); i++) {
        if (str[i] == '-')
            amount += 1;
    }
    return amount;
}

void clean(char *str){
    int length = strlen(str);
    for (int i = 0; i < length; i++){
        str[i] = '\x00';
    }
}
void split(char *str, char result[5][5]) {
    char var[5] = "";
    int pointer = 0;

    for (int i = 0; i < strlen(str); i++){
        if (i == 23){
            var[strlen(var)] = str[i];
            var[strlen(var) + 1] = '\x00';
        }
        if (str[i] == '-' || i == 23){
            strcpy(result[pointer],var);
            clean(var);
            pointer++;
        } else {
            var[strlen(var)] = str[i];
            var[strlen(var) + 1] = '\x00';
        }
    }
}

int func1(char * check) {
    int number = 0;
    int decimals = 1;

    for (int i = 0; i < strlen(check); i++){
        number += (check[i] - 48) * decimals;
        decimals *= 10;
    }

    if (number != 9367)
        return 0;
    return 1;
}

int func2(char * check) {
    char op[32] = "key is the music, not 17.29.1337";
    int first = (check[0] - 48) * 10 + (check[3] - 48);
    int second = (check[2] - 48) * 10 + (check[1] - 48);

    char result[32];
    sprintf(result, "key is the music, not %d.%d.1337", first, second);

    if (strncmp(op, result, 32))
        return 0;
    return 1;
}

const char * stupid_hash(char *str) {
    int arr[4];
    for (int i = 0; i < 4; i++)
        arr[i] = str[i] % 6;
    static char result[5];
    sprintf(result, "%d%d%d%d", arr[0], arr[1], arr[2], arr[3]);
    return result;
}

int in(char *str, char symbol) {
    for (int i = 0; i < strlen(str); i++){
        if (str[i] == symbol)
            return 1;
    }
    return 0;
}

int func3(char * check) {
    int number = 0;
    int sixteens = 1;
    int decimals = 1;
    for (int i = 0; i < strlen(check); i++){
        if (in("abcdef", check[i])) {
            number += (check[i] - 'a' + 10) * sixteens;
            sixteens *= 16; 
        } else if(in("0123456789", check[i])) {
            number += (check[i] - '0') * decimals;
            decimals *= 10;
        } else {
            incorrect();
        }
    }

    char result[10];
    sprintf(result, "%d", number);

    if (strncmp(result, stupid_hash("good"), 4))
        return 0;
    return 1;
}

int func4(char * check) {
    check[0] ^= 123;
    check[1] ^= 86;
    check[2] ^= 64;
    check[3] ^= 84;

    if (strncmp(check, "Nord", 4))
        return 0;
    return 1;
}

int func5(char * check) {
    long long int number = 1;
    for (int i = 0; i < 4; i++){
        number *= check[i];
    }
    
    if (number != 8446032)
        return 0;
    return 1;
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    char input[25] = "";
    printf("Give me your license: ");
    fgets(input, 25, stdin);

    if (strlen(input) != 24)
        incorrect();
    if (count_dashes(input) != 4)
        incorrect();

    char pieces[5][5];
    split(input, pieces);

    int return1 = func1(pieces[0]);
    int return2 = func2(pieces[1]);
    int return3 = func3(pieces[2]);
    int return4 = func4(pieces[3]);
    int return5 = func5(pieces[4]);

    if ((return1 & return2 & return3 & return4 & return5) == 1)
        show_flag();
    else 
        incorrect();
}