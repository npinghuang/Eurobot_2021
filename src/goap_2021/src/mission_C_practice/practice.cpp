#include <iostream>
#include <stdio.h>
#include<string>
#include "mission_setting.h"
#include "getcup.h"
using namespace std;


mission emergency(0, "emergency", 0);
mission windsock( 1, "windsock", 0);
mission lhouse(2, "lhouse", 0);
mission flag( 3, "flag", 0);
mission anchorN(4, "anchorN", 0);
mission anchorS(5, "anchorS", 0);
mission reef_l( 6, "reef_l", 0);
mission reef_r( 7, "reef_r", 0);
mission reef_p( 8, "reef_p", 0);
mission placecup_h( 9, "placecup_h", 0);
mission placecup_p( 10, "placecup_p", 0);
mission placecup_r( 11, "placecup_r", 0);
mission getcup(12, "getcup", 0);
mission getcup_12( 13, "getcup_12", 0);
mission getcup_34( 14, "getcup_34", 0);

int main(){
    cout<<"Hello World"<<endl;
    cout<<"try"<<endl;
    // printf("getcup class  constructor : %d \n" , getcup.mission_no );
    int action_array11[] = {1,2,3,4,5,6};
    printf("no 1 %d\n", &action_array11[0]);
    printf("no 2 %d\n", &action_array11[1]);
    printf("+1 %d %d\n", (&action_array11 +1), *(&action_array11 +1 ));
    cout<<"++1 "<<(&action_array11 +1)<<" "<<*(&action_array11 +1 ) << " "<< action_array11<<endl;
    // printf("getcup class  : %d, %d \n" , getcup.mission_no, getcup.count);
    int len = *(&action_array11 + 1) - action_array11;
    printf("what %d\n", *action_array11);
    int *ptr;
    ptr = action_array11;
    for ( int i = 0; i < 5; i ++){
        getcup_action( action_array11, getcup.count, len, ptr);
        getcup.count += 1;
    }
    
    printf("check %d\n", len);
    // switch(number){
    //     case 0:
    //         mission emergency;
    //         emergency.mission_no = 0;
    //         emergency.mission_name = 'emergency';
    //         break;
    //     case 1:
    //         mission windsock;
    //         windsock.mission_no = 1;
    //         windsock.mission_name = 'windsock';
    //         break;
    //     case 2:
    //         mission lhouse;
    //         lhouse.mission_no = 2;
    //         lhouse.mission_name = 'lhouse';
    //         break;
    //     case 3:
    //         mission flag;
    //         flag.mission_no = 3;
    //         flag.mission_name = 'flag';
    // }

//    system("pause");
    return 0;
}
