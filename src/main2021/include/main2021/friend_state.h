#ifndef FRIEND_STATE_H_
#define FRIEND_STATE_H_

#include <iostream>
#include <stdlib.h>
#include <vector>


class Friend{
public:
    Friend();
    void setf_x(float);
    void setf_y(float);
    void setf_z(float);
    void setf_degree(float);
    void setf_action(std::vector<int>*);

    float getf_x();
    float getf_y();
    float getf_z();
    float getf_degree();
    std::vector<int>& getf_action();

private:
    float f_x;
    float f_y;
    float f_z;
    float f_degree;

    std::vector<int> f_action; //[0]:action number; [1]:cup number
};

#endif
