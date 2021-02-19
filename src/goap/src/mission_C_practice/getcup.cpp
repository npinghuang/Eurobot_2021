#include <iostream>
#include <stdio.h>
#include<string>
#include "getcup.h"
using namespace std;
    
void getcup_action( int action[], int count, int length, int *ptr){
    
    // int len = *(action + 1) - action;
    // printf("so slow!! %d\n", len);- action
    printf("size of %d\n", &action[0] );
    printf("size of lala %d\n", *(action + 1));
    printf("size of la %d\n", *((&action +1) - 1));
    for ( int i = count; i < length; i++){
        printf("action %d : %d\n", i, action[i]);
        printf("action pointer %d : %d\n", i, *(ptr + i));
    }
}