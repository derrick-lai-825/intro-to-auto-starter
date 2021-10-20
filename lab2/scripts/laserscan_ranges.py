#!/usr/bin/env python

import rospy
import numpy as np
from std_msgs.msg import String, Float32
from sensor_msgs.msg import LaserScan
from lab2.msg import ScanRange
import time

import json


class LaserScanNode():
    def __init__(self):
        
        # create a publisher handle to publish ScanRange messages to the 
        # laserscan_range topic. Make sure you use self.var_name = xyz so
	    # that you are able to use this handle in your other functions

       	#TODO: CREATE PUBLISHER HANDLER HERE
        self.laserscan_range = rospy.Publisher("/laserscan_range", ScanRange, queue_size=10) #pub = rospy.Publisher('chatter', String, queue_size=10)


        #TODO: CREATE INSTANCE OF ScanRange HERE
        self.scan_range = ScanRange() #Probably won't work
        # subscriber handle for the scan message. This handle 
        # will subscribe to scan and recieve LaserScan messages. Each
        # time this happens the scan_callback function is called

        print(self.scan_range.closest_point)
        rospy.Subscriber('scan', LaserScan, self.scan_callback)

        
        # initialize and register this node with the ROS master node
        rospy.init_node('laserscan_listen', anonymous=False)
        
        # Create an instance of the scan range message to store your closest and farthest
        # points. Remember, these attributes can be accesed with:
        # self.scan_range.closest_point. Also note the attributes are set to default values
        # currently.
        # self.closest_point = 0
        # self.farthest_point = 0

        
    
    # this is the callback for the scan message. 
    # here we will use the scan_data parameter to access the ranges 
    # from the LaserScan message and figure out the closest and farthest point
    def scan_callback(self, scan_data):
        # Write code to loop through the laser scan ranges and find the closest
        # and farthest values. Store those values in the ScanRange instance you created
        # in __init__()
        # TODO: FILTER DATA
        #array = np.array(list(scan_data))
        #print(type(array))
        dataList = scan_data.ranges

        self.scan_range.closest_point = 10000000
        self.scan_range.farthest_point = 0

        minPoint = scan_data.range_min
        maxPoint = scan_data.range_max


        for point in dataList:
            if (point < minPoint) or (point > maxPoint) or (np.isinf(point)) or (np.isnan(point)):
                continue

            if point > self.scan_range.farthest_point:
                self.scan_range.farthest_point = point

            elif point < self.scan_range.closest_point:
                self.scan_range.closest_point = point

            
        #listData = list(scan_data)
        #print(listData)
        # TODO: FIND CLOSEST AND FARTHEST POINTS
        #return self.closest_point, self.farthest_point
        # return scan_data
        
        pass

    # the publish method is  called on an interval in the main
    # loop of this file. This is where we publish our ranges to 
    # the topic. 
    def publish(self):
       # TODO: ADD PUBLISHER CODE HERE
        self.laserscan_range.publish(self.scan_range)
        print(self.scan_range.closest_point, self.scan_range.farthest_point)
        pass
        

if __name__ == '__main__':
    ls = LaserScanNode()

    rate = rospy.Rate(10) # 10hz
    try:
        # Add a while loop which calls the publish() function of the laser scan node
        # on the interval we have defined with rate
        # TODO: CREATE PUBLISHER LOOP HERE
        while not rospy.is_shutdown():
            ls.publish()
            rate.sleep()

        pass
    except rospy.ROSInterruptException:
        pass
