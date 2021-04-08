#ifndef STATE_H_
#define STATE_H_

#include <iostream>
#include <stdlib.h>
#include <vector>

enum STATE {FALSE = 0, SUCCESS, DOING, emerg};

class State{
public:
    State(float, float, float, int);

    float getx();
    float gety();
    float getz();
    float getth();

    std::vector<int>& get_hand();
    std::vector<int>& get_list();
    std::vector<int>& get_color();
    int get_cup();
    bool get_ns();
    bool get_team();
    bool emergOrNot();
    float get_time();
    int get_script();
    int get_status(); 
    int get_score(); 

    int get_p_state();
    int get_m_state();

    void setpos(float, float, float, float);
    void set_hand(std::vector<int>*);
    void set_list(std::vector<int>*);
    void set_color(std::vector<int>*);
    void set_script(int);
    void set_cup(int, int);
    void updatecup(int);
    void set_ns(bool);
    void set_team(bool);
    void set_time(float);
    void set_status(int);
    void set_p_state(int);
    void set_m_state(int);
    void set_emerg(bool);
    void set_score(int, int);
    // bool findWay();

private:
    float my_x;
    float my_y;
    float my_z;
    float degree;

    std::vector<int> actionList;
    std::vector<int> cup_color;
    std::vector<int> hand;
    int cup;
    bool ns;
    bool team;
    bool emerg;
    float time;
    int script;
    int status;
    int planer_state;
    int mission_state;
    int score;
    int red;
    int green;
};    


#endif
