#ifndef MISSION_SETTING_H
#define MISSION_SETTING_H
#include <string>
using namespace std;

class mission_setting{
    public:
        int mission_no;
        string mission_name;
        int count;
        mission_setting(int num, string name, int count);
        void setting_ (int num, string name, int no );
        
}; //extern mission_setting mi( 333, "global", 333);
#endif 