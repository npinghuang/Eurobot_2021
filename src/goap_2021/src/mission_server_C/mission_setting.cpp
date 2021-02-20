#include "mission_setting.h"
#include<stdio.h>
#include<string>
using namespace std;

// mission::mission(int num, string name){
//     mission_no = num;
//     mission_name = name;
//     printf("hi there");
// }
void mission_setting::setting_(int num, string name, int no ){
    mission_no = num;
    mission_name = name;
    count = no;
    printf("hi there : %d \n", mission_no);
}

mission_setting::mission_setting(int num, string name, int count){
    setting_( num, name, count );
    // printf("constructor");
}


