#!/usr/bin/env python 
import rospy 
from serial.tools import list_ports 
from std_msgs.msg import String 
from ast import literal_eval 
import time 
from driver import * 
import serial 
 
baud = 4800 
VID = '1A86' 
PID = '7523' 
device_list = list_ports.comports() 
for device in device_list: 
   if ('{:04X}'.format(device.vid) == VID and '{:04X}'.format(device.pid) == PID): 
      port = device.device 
      break 
port = None 
usb = port 

plants = [] 
path = [] 
real_pos = [0,0] 
point = 0 
done = True 
ser = serial.Serial(port, baud) 

def callback_planner(data): 
   global path, plants 
   data_raw = (data.data).replace("[","").replace("]","").split("/") 
   points = [((data_raw[i][0]).split(", "))[0] for i in 
   range(len(data_raw))] 
   plants = [((data_raw[i][1]).split(", "))[0] for i in 
   range(len(data_raw))] 


def callback(data): 
   global real_pos,done,point,ser 
   data_raw = (data.data).replace("[","").replace("]","").split("/") 
   pos_x = ((data_raw[0]).split(", "))[0] 
   pos_y = ((data_raw[1]).split(", "))[0] 
   real_pos = [float(pos_x), float(pos_y)] 

   if done==True: 
      start = path[point] 
      point += 1 
      goal = path[point] 
      move_to_point(ser, start, goal) 
      done = False 
         
   if euc(real_pos, path[point]) < 0.05: 
      done = True 
   if euc(plants, path[point]) < 0.05: 
      stop(ser) 
      time.sleep(10) 

def moving(): 
#pub = rospy.Publisher('chatter', String, queue_size = 10) 
   rospy.init_node('moving', anonymous = True) 
   rospy.Subscriber("position_from_sensors_chatter", String, callback) 
   rospy.Subscriber("planner" String, callback_planner) 
   rate = rospy.Rate(10) 
   rospy.spin() 
   rate.sleep() 
if __name__ == "__main__": 
   moving() 