#include <ros/ros.h>
#include <std_msgs/String.h>
#include "main2021/Data.h"
#include "main2021/cup_camera.h"
#include "main2021/ns.h"
#include "main2021/cup.h"
#include "main2021/gui_state.h"

#include "../include/main2021/data_state_small.h"


#include <iostream>
#include <stdlib.h>
#include <vector>
#include <math.h>

using namespace std;

data_state::data_state(float x1,float y1, float x2,float y2, int c){
	//ns--> 0:n 1:s
	client_ns = h.serviceClient<main2021::ns>("ns_service");
	//array--> 1:red 0:green
	client_cup = h.serviceClient<main2021::cup>("cup_service");
	client_camera = h.serviceClient<main2021::cup_camera>("cup_camera");

	ns_srv.request.ask_ns = 0;
	cup_srv.request.ask_cup = 0;
	c_srv.request.req = false;

	sx = x2;
	sy = y2;
	sdegree = M_PI;
	saction = {0};
	saction_list = {0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0};
	scup = c;
	sscore = 0;

	bx = x1;
	by = y1;
	bdegree = M_PI;
	baction = {0};
	baction_list = {0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0};
	bcup = c;
	bscore = 0;

	action_list = {0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0};
	cup_color = {0, 1, 0, 1, 0, 1, 0, 1, 0, 1};
	// another_cup_color = {};
	camera_cup_color = {0};
	camera_cup_pos = {0};
	cup = c;
	script = 0;
	ns = 0;
	team = 1;
	// score = 0;

	//spinonce();
	initial_cup_pos();
}
void data_state::initial_cup_pos(){
	//blue
	// if(team == 0){
		//( num, (x, y), 1 for cup still there 0 for cup gone, 2 for green 3 for red)
		bc[0] = {.num = 1,.pos = pair<float, float>(400., 300.), .color = 3, .state = true}; bc[1] = {.num = 2, .pos = pair<float, float>(1200., 300.), .color = 2, .state = true};
		bc[2] = {.num = 3, .pos = pair<float, float>(515., 445.), .color = 2, .state = true}; bc[3] = {.num = 4, .pos = pair<float, float>(1085., 445.), .color = 3, .state = true};
		bc[4] = {.num = 5, .pos = pair<float, float>(100., 670.), .color = 2, .state = true}; bc[5] = {.num = 6, .pos = pair<float, float>(400., 956.), .color = 3, .state = true}; 
		bc[6] = {.num = 7, .pos = pair<float, float>(1955., 1005.), .color = 3, .state = true}; bc[7] = {.num = 8, .pos = pair<float, float>(1655., 1065.), .color = 2, .state = true};
		bc[8] = {.num = 9, .pos = pair<float, float>(800., 1100.), .color = 2, .state = true}; bc[9] = {.num = 10, .pos = pair<float, float>(1200., 1270.), .color = 3, .state = true};
		bc[10] = {.num = 11, .pos = pair<float, float>(1655., 1335.), .color = 3, .state = true}; bc[11] = {.num = 12, .pos = pair<float, float>(1955., 1395.), .color = 2, .state = true};
		bc[12] = {.num = 13, .pos = pair<float, float>(1955., 1605.), .color = 3, .state = true}; bc[13] = {.num = 14, .pos = pair<float, float>(1655., 1665.), .color = 2, .state = true};
		bc[14] = {.num = 15, .pos = pair<float, float>(1200., 1730.), .color = 2, .state = true}; bc[15] = {.num = 16, .pos = pair<float, float>(800., 1900.), .color = 3, .state = true};
		bc[16] = {.num = 17, .pos = pair<float, float>(1655., 1935.), .color = 3, .state = true}; bc[17] = {.num = 18, .pos = pair<float, float>(1955., 1995.), .color = 2, .state = true};
		bc[18] = {.num = 19, .pos = pair<float, float>(400., 2044.), .color = 2, .state = true}; bc[19] = {.num = 20, .pos = pair<float, float>(100., 2330.), .color = 3, .state = true};
		bc[20] = {.num = 21, .pos = pair<float, float>(515., 2555.), .color = 2, .state = true}; bc[21] = {.num = 22, .pos = pair<float, float>(1085., 2555.), .color = 3, .state = true};
		bc[22] = {.num = 23, .pos = pair<float, float>(400., 2700.), .color = 3, .state = true}; bc[23] = {.num = 24, .pos = pair<float, float>(1200., 2700.), .color = 2, .state = true};
}

//NS service, 0:n 1:s
void data_state::callNS(int req){
	ns_srv.request.ask_ns = req;
	int i = 0;
	while (i == 0)
	{
		if(client_ns.call(ns_srv)){
			ROS_INFO("GET NS");
			ns = ns_srv.response.ns_result;
			ROS_INFO("NS:%d", ns);
			i = 1;
		}
		else
			ROS_INFO("ns fail call");
	}
	
}

//cup color service, 1:red 0:green
void data_state::callCup(int req){
	cup_srv.request.ask_cup = req;
	int i = 0;
	while (i == 0)
	{
		if(client_cup.call(cup_srv)){
			// ROS_INFO("GET NS");
			cup_color.clear();
			//reef five cups left
			for(int j = 0 ; j < 5 ; j++){
				cup_color.push_back(cup_srv.response.cup_result[j]);
			}
			//reef five cups right
			for(int j = 4 ; j >= 0 ; j--){
				if(cup_srv.response.cup_result[j] == 1)
					cup_color.push_back(0);
				else if (cup_srv.response.cup_result[j] == 0)
					cup_color.push_back(1);
			}

			// cup_color.assign(cup_srv.response.cup_result.begin(), cup_srv.response.cup_result.end());

			// for(int j = 0 ; j < 5 ; j++){
			// 	if(cup_color[j] == 1)
			// 		another_cup_color[j] = 0;
			// 	else if (cup_color[j] == 0)
			// 		another_cup_color[j] = 1;
				
			// 	// cup_color[j] = cup_srv.response.CupResult[j];
			// 	// ROS_INFO("CUP%d:%d", j, cup_color[j]);
			// }	
			i = 1;			
		}
		else
			ROS_INFO("color fail call");
	}
}

//cup camera service, mm
void data_state::callCamera(bool req){
	 c_srv.request.req = req;

	int i = 0;
	while(i == 0){
		// ROS_INFO("call");
		if(client_camera.call(c_srv)){
			// ROS_INFO("CUP");
			camera_cup_color.assign(c_srv.response.color.begin(), c_srv.response.color.end());
			camera_cup_pos.assign(c_srv.response.cup_pos.begin(), c_srv.response.cup_pos.end());
			i = 1;
			// ROS_INFO("camera color size: %ld", camera_cup_color.size());
			// for(int j = 0 ; j < camera_cup_color.size() ; j++)
			// 	ROS_INFO("color: %ld", camera_cup_color[j]);
			// ROS_INFO("camera call pos size: %ld", camera_cup_pos.size());
			// for(int j = 0 ; j < camera_cup_pos.size() ; j++)
			// 	ROS_INFO("pos: %lf", camera_cup_pos[j]);	
		}
		else
			ROS_INFO("cup fail call");
	}
	
	unityCup();
}

void data_state::set_ini(GUI g){
	bx = g.get_bigX();
	by = g.get_bigY();
	sx = g.get_smallX();
	sy = g.get_smallY();
	team = g.get_team();
	script = g.get_script();
}
void data_state::set_score(){
	
}

float data_state::get_sx(){ return sx;}
float data_state::get_sy(){ return sy;}
float data_state::get_sdegree(){ return sdegree;}
vector<int>& data_state::get_saction(){ return saction;}
int data_state::get_sscore(){ return sscore;}

float data_state::get_bx(){ return bx;}
float data_state::get_by(){ return by;}
float data_state::get_bdegree(){ return bdegree;}
vector<int>& data_state::get_baction(){ return baction;}
int data_state::get_bscore(){ return bscore;}

vector<int>& data_state::get_list(){ return action_list;}
vector<int>& data_state::get_color(){ return cup_color;}
// vector<int>& data_state::get_another_color(){ return another_cup_color;}
int data_state::get_cup(){ return cup;}
int data_state::get_script(){ return script;}
bool data_state::get_ns(){ return ns;}
int data_state::get_team(){ return team;}
// int data_state::get_team(){ return score;}
int data_state::now_status(){ return status;}

void data_state::unityAction(){
	//ROS_INFO("SIZE %d", (int)action_list.size());
	for(int i = 0 ; i <= action_list.size() ; i++){
		if(saction_list[i] == 1 || baction_list[i] == 1)
			action_list[i] = 1;
		else{
			if(saction_list[i] == 2 || baction_list[i] == 2)
				action_list[i] = 2;
			else{
				if(saction_list[i] == 3 || baction_list[i] == 3)
					action_list[i] = 3;					
			}
		} 
	}
}

void data_state::tf_cup(){
	int radiu = 0;
	cup = 16777215;
	// ROS_INFO("TF");
	for(int i = 0 ; i < 24 ; i++){
		for(int j = 0 ; j < camera_cup_pos.size() ; j += 3){
			// ROS_INFO("TF_C");
			radiu = (camera_cup_pos[j] - bc[i].pos.first)*(camera_cup_pos[j] - bc[i].pos.first) + (camera_cup_pos[j+1] - bc[i].pos.second)*(camera_cup_pos[j+1] - bc[i].pos.second);
			if(radiu > 20*20){
				bc[i].state = false;
				// break;
			}
			else{
			 	if(bc[i].color != camera_cup_color[j/3]){
					bc[i].state = false;
					break;
				}	
				else{
					bc[i].state = true;
					break;
				}
			}		
		}
		if(bc[i].state == false){
			// ROS_INFO("TF_F");
			cup = cup ^ (1 << i);
		}

	}
}

void data_state::unityCup(){
	//cup = 65535;
	// ROS_INFO("UNITY");
	tf_cup();
	cup = cup & (scup & bcup);
	
}

void data_state::datacallback(const main2021::Data::ConstPtr& msg){

	//small chicken
	sx = msg->small_chicken_pos[0];//0;
	sy = msg->small_chicken_pos[1];//0;
	sdegree = msg->small_chicken_pos[2];//0;
	saction.assign(msg->small_action.begin(), msg->small_action.end());
	saction_list.assign(msg->small_action_list.begin(), msg->small_action_list.end());
	scup = msg->small_cup;//16777215;
	sscore = msg->small_score;
	//big chicken
	bx = msg->big_chicken_pos[0];
	by = msg->big_chicken_pos[1];
	bdegree = msg->big_chicken_pos[2];
	baction.assign(msg->big_action.begin(), msg->big_action.end());
	baction_list.assign(msg->big_action_list.begin(), msg->big_action_list.end());
	bcup = 16777215;//msg->big_cup;
	bscore = msg->big_score;

	team = msg->team;
	status = msg->status;
	//ROS_INFO("DATA");
}
