#include <ros/ros.h>
#include <std_msgs/String.h>
#include "main2021/Data.h"
#include "main2021/dataToAgent.h"
#include "main2021/cup_camera.h"
#include "main2021/gui_state.h"

#include "../include/main2021/data_state_small.h"

#include <iostream>
#include <stdlib.h>
#include <vector>

#define INIbig_POSX 600. //mm
#define INIbig_POSY 2805. //mm
#define INIsmall_POSX 980. //mm
#define INIsmall_POSY 2805. //mm
#define INI_CUP 16777215 //24 cups are here

using namespace std;

int main(int argc, char** argv){
    ros::init(argc, argv, "data_node");
    ros::NodeHandle nh;

	//give data to chicken
	ros::Publisher pub_dataBig = nh.advertise<main2021::dataToAgent>("DataToBig", 1000);
	ros::Publisher pub_dataSmall = nh.advertise<main2021::dataToAgent>("DataToSmall", 1000);
	
	main2021::dataToAgent big;
	main2021::dataToAgent small;

	//time
	ros::Time begin_time;
	ros::Time now_time;

	//data
	GUI gui;
	data_state state(INIbig_POSX, INIbig_POSY, INIsmall_POSX, INIsmall_POSY, INI_CUP);
	ros::Subscriber sub_data = nh.subscribe<main2021::Data>("giveToData", 1000, &data_state::datacallback, &state);

	int start = 0;
	int now_status = 0;
	int cupCall = 0;
	int nsCall = 0;
	bool firstrun = false;
	bool cameraCall = false;
	float doing_time = 0;

	ros::Rate rate(200);
	if(ros::ok() == false)
		ROS_INFO("Data FALSE");
	while(ros::ok()){
		//To Do******
		if(now_status < 4)
			now_status = gui.changState();
		switch(state.now_status()){
			case 0://戰術選擇 --> team, enemy
				//from launch file
				
				ROS_INFO("STATE 0");
				cameraCall = false;
				gui.set_strategy();
				state.set_ini(gui);
				// now_status = gui.changState();
				break;
			case 1://機構,底盤reset
				
				ROS_INFO("STATE 1");
				cameraCall = false;
				// now_status = 2;
				break;
			case 2://更新Data, reset
				
				ROS_INFO("STATE 2");
				cupCall = 1;
				nsCall = 1;
				// state.callNS(1);
				// state.callCup(1);				
				cameraCall = true;
				// now_status = 3;
				break;
			case 3://拿另一機的資料
				ROS_INFO("STATE 3");
				cameraCall = false;
				// now_status = 4;
				break;
			case 4://等拔插銷 from ST1
				//To Do******
				//wait for ST1
				nh.getParam("/start", start);
				ROS_INFO("STATE 4");
				cameraCall = false;
				if(start >= 1)
					now_status = 5;
				break;
			case 5://run
				if(firstrun == false){
					begin_time = ros::Time::now();
					firstrun = true;
				}
				now_time = ros::Time::now();
				doing_time = (now_time - begin_time).toSec();
				cameraCall = true;
				// ROS_INFO("TIME:%f", doing_time);
				break;      
		}
		gui.pubToGUI(now_status);
		gui.countScore(state.get_bscore(), state.get_sscore());

		//ROS_INFO("NOWSTATUS:%d", now_status);
		state.unityAction();
		// if(doing_time % 2. == 0)
		state.callCamera(cameraCall);
		// state.callNS(cupCall);
		// state.callNS(nsCall);
		//give big chicken
		big.x = state.get_bx();
		big.y = state.get_by();
		big.fx = state.get_sx();
		big.fy = state.get_sy();
		big.degree = state.get_sdegree();
		big.action.assign(state.get_saction().begin(), state.get_saction().end());
		big.action_list.assign(state.get_list().begin(), state.get_list().end());
		big.cup_color.assign(state.get_color().begin(), state.get_color().end());
		big.cup = state.get_cup();
		big.script = state.get_script();
		big.ns = state.get_ns();
		big.team = state.get_team();
		big.time = doing_time;
		big.status = now_status;

		pub_dataBig.publish(big);
		//ROS_INFO("BIG");
		//give small chicken
		small.x = state.get_sx();
		small.y = state.get_sy();
		small.fx = state.get_bx();
		small.fy = state.get_by();
		small.degree = state.get_bdegree();
		small.action.assign(state.get_baction().begin(), state.get_baction().end());
		small.action_list.assign(state.get_list().begin(), state.get_list().end());
		small.cup_color.assign(state.get_color().begin(), state.get_color().end());
		small.cup = state.get_cup();
		small.script = state.get_script();
		small.ns = state.get_ns();
		small.team = state.get_team();
		small.time = doing_time;
		small.status = now_status;

		pub_dataSmall.publish(small);

		ros::spinOnce();
		rate.sleep();
	}

	return 0;
}
