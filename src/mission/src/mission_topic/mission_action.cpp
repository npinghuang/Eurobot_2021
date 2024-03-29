#include "mission/mission_action.h"
#include<stdio.h>
// #include<string>
#include <vector>
using namespace std;

const int action_0[1] = { 9 };
const float action_1[4] = { 1, 2, 3, 4 };
const int action_2[1] = { 999 };
const int action_3[1] = { 9999 };
const int action_4[1] = { 999 };
const int action_5[1] = { 999 };
const int action_6[1] = { 999 };
const int action_7[1] = { 999 };
const int action_8[1] = { 999 };
const int action_9[1] = { 999 };
const int action_10[1] = { 999 };
const int action_11[1] = { 999 };
const int action_12[1] = { 999 };
const int action_13[1] = { 999 };
const int action_14[1] = { 999 };

// const std::vector<int> values{1,2,3,4,5};
extern const std::vector<vector<float>> action1_planer_blue{
        {1.800, .150, 90},
        {1.800, .850, 90},
    };
extern const std::vector<vector<float>> action1_planer_yellow{
        {1.800, 2.800, 90},
        {1.800, 2.100, 90},
    };
extern const std::vector<int> action1_ST2_blue{66, 77};
extern const std::vector<int> action1{ 2,1,1,2} ;//insicator planer or ST2;
// const int action_planer_1[2][4] = { { 1, 2, 3, 4}, { 5, 6, 7, 8}};
extern const std::vector<vector<float>> action2_planer_blue{
        {.100, .225, 0},
        {.150, .225, 0}
    };
extern const std::vector<vector<float>> action2_planer_yellow{
        {.100, 2.750, 0},
        {.150, 2.750, 0}
    };
extern const std::vector<int> action2_ST2_blue{1, 2, 3, 4};
extern const std::vector<int> action2{ 2, 2, 1, 2, 1, 2, 1, 1} ;

extern const std::vector<vector<float>> action9_planer_blue{
        {1.85, 1.8, 0},
        {1.8, 1.8, 0},
        {1.65, 1.8, 180}
    };
extern const std::vector<vector<float>> action9_planer_yellow{
        {.100, 2.750, 0},
        {.150, 2.750, 0}
    };
extern const std::vector<int> placecup_hand{51, 12, 3264, 768};
    // { 1, 2, 7, 5},
    // { 8, 6, -1, -1},
    // { 4, 3, 11, 9},
    // { 12, 10, -1, -1},
      // {0, 1, 4, 5},
        // { 2, 3, -1, -1},
        // {6, 7, 10, 11},
        // { 8, 9, -1, -1},
    // };
extern const std::vector<int> placecup_theta = {20, 30, 0, 10};
extern const std::vector<int> getcup_theta = {20,-20, 30,  -30}; // [0] for hand 2 4 9 11 [1] for hand 3 5 8 10 

extern const std::vector<vector<int>> cup_pos{
    { 400, 300 }, {1200, 300}, {1200, 300 }, {1085, 445 },
    { 100, 670 }, {400, 956}, {1955, 1005}, { 1655, 1065 },
    { 800, 1100 }, { 1200, 1270 }, { 1655, 1335 }, { 1955, 1395 },
    { 1955, 1605 }, { 1655, 1665 }, { 1200, 1730 }, {800, 1900},
    {1655, 1935 }, { 1955, 1995 }, { 400, 2044 }, { 100, 2330 },
    { 515, 2555 }, { 1085, 2555 }, { 400, 2700 }, { 1200, 2700 }, {150, 60 }
};

extern const std::vector<int> cup_color{ 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1};


