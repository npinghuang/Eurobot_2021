#ifndef MISSION_SETTING_H
#define MISSION_SETTING_H
#include <string>
using namespace std;

class mission{
    public:
        int mission_no;
        string mission_name;
        int count;
        mission(int num, string name, int count);
        void setting_ (int num, string name, int no );
        
};
#endif 