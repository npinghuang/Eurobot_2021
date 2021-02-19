#!/usr/bin/env python
#coding=utf-8

import sys
import rospy
from goap_2021.srv import*

def goap_client():
    rospy.wait_for_service('goap')
    try:
        goap = rospy.ServiceProxy('goap', goap_)
