#ifndef DATA_STATE_H_
#define DATA_STATE_H_

#include <ros/ros.h>
#include <std_msgs/String.h>
#include "main2021/Data.h"
#include "main2021/cup_camera.h"
#include "main2021/ns.h"
#include "main2021/cup.h"
#include "main2021/gui_state.h"

#include "../include/main2021/data_state.h"

#include <iostream>
#include <stdlib.h>
#include <vector>

using namespace std;

typedef struct cup_p
{
	int num;
	pair<float, float> pos;
	int color;
	bool state;
}CUP;

class data_state{
public:
	data_state(float ,float, float ,float, int);
	void initial_cup_pos();
	void callNS(int);
	void callCup(int);
	void callCamera(bool);

	void set_ini(GUI);
	void set_score();

	float get_sx();
	float get_sy();
	float get_sdegree();
	vector<int>& get_saction();
	int get_sscore();

	float get_bx();
	float get_by();
	float get_bdegree();
	vector<int>& get_baction();
	int get_bscore();

	vector<int>& get_list();
	vector<int>& get_color();
	// vector<int>& get_another_color();
	int get_cup();
	int get_script();
	bool get_ns();
	int get_team();
	int get_score();
	int now_status();

	void unityAction();

	void tf_cup();

	void unityCup();

	void datacallback(const main2021::Data::ConstPtr&);

private:
	ros::NodeHandle h;

	ros::ServiceClient client_ns;
	main2021::ns ns_srv;
	ros::ServiceClient client_cup;
	main2021::cup cup_srv;
	ros::ServiceClient client_camera;
	main2021::cup_camera c_srv;

	float sx;
	float sy;
	float sdegree;
	vector<int> saction;
	vector<int> saction_list;
	int scup;
	int sscore;
	
	float bx;
	float by;
	float bdegree;
	vector<int> baction;
	vector<int> baction_list;
	int bcup;
	int bscore;
	
	vector<int> action_list;
	vector<int> cup_color; //reef five cups
	// vector<int> another_cup_color; //reef five cups left
	vector<int> camera_cup_color; //normal cups' color
	vector<float> camera_cup_pos; //normal cups' pos
	int cup;
	int script;
	int ns;
	bool team;
	int status;
	// int score;
	CUP bc[24];
};

#endif
