#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
import rospy 
from serial.tools import list_ports 
import main as m 
from std_msgs.msg import String 
import filterpy.kalman 
import filterpy.common 
import numpy as np 
import numpy.random 
 
baud = 4800 
VID = '0483' 
PID = '5740' 
device_list = list_ports.comports() 
for device in device_list: 
  if ('{:04X}'.format(device.vid) == VID and '{:04X}'.format(device.pid) == PID): 
    port = device.device 
    break 
port = None 
usb = port 

def updateSensor(data, position_x,position_y, dt): 

  if data[2]==0.0 and data[3]==0.0: 
    data[0]=0.0 
    data[1]=0.0 

    position_x = position_x + data[2] * dt + (data[0] * dt ** 2) / 2.0 
    position_y = position_y + data[3] * dt + (data[1] * dt ** 2) / 2.0 
    trajectory_x = np.zeros((3, 1)) 
    trajectory_y = np.zeros((3, 1)) 
    trajectory_x[0][0] = position_x 
    trajectory_x[1][0] = data[2] 
    trajectory_x[2][0] = data[0] 
        
    trajectory_y[0][0] = position_y 
    trajectory_y[1][0] = data[3] 
    trajectory_y[2][0] = data[1] 

    return trajectory_x, trajectory_y 


  dt=0.01                      # Шаг времени 
  measurementSigma = 0.5          # Среднеквадратичное отклонение датчика 
  processNoise = 1e-4             # Погрешность модели 

  # Моделирование данных датчиков 
  filter = filterpy.kalman.KalmanFilter(dim_x=3, dim_z=1)  
  filter.F = np.array([[1,   dt,  (dt**2)/2], 
                      [0,   1.0,     dt   ], 
                      [0,    0,      1.0  ]]) 

  filter.H = np.array([[1.0, 0.0, 0.0]]) 
  filter.Q = filterpy.common.Q_discrete_white_noise(dim=3, dt=dt, 
  var=processNoise) 
  filter.R = np.array([[measurementSigma*measurementSigma]]) 
  filter.x = np.array([0.0, 0.0, 0.0]) 
  filter.P = np.array([[10.0, 0.0,  0.0], 
                      [0.0,  10.0, 0.0], 
                      [0.0,  0.0, 10.0]]) 

  filteredState = [] 
  stateCovarianceHistory = [] 


  dt_y = 0.01                       # Шаг времени 
  measurementSigma_y = 0.5          # Среднеквадратичное отклонение датчика 
  processNoise_y = 1e-4             # Погрешность модели 

  # Моделирование данных датчиков 
  filter_y = filterpy.kalman.KalmanFilter(dim_x=3, dim_z=1)  
  filter_y.F = np.array([[1,   dt_y,  (dt_y**2)/2], 
                      [0,   1.0,     dt_y   ], 
                      [0,    0,      1.0  ]]) 

  filter_y.H = np.array([[1.0, 0.0, 0.0]]) 
  filter_y.Q = filterpy.common.Q_discrete_white_noise(dim=3, dt=dt_y, 
  var=processNoise_y) 
  filter_y.R = np.array([[measurementSigma_y*measurementSigma_y]]) 
  filter_y.x = np.array([0.0, 0.0, 0.0]) 
  filter_y.P = np.array([[10.0, 0.0,  0.0], 
                      [0.0,  10.0, 0.0], 
                      [0.0,  0.0, 10.0]]) 

  filteredState_y = [] 
  stateCovarianceHistory_y = [] 



def position_from_sensors(): 
  pos_x=0 
  pos_y = 0 
  pub = rospy.Publisher('position_from_sensors_chatter', String, 
  queue_size = 10) 
  rospy.init_node('position_from_sensors', anonymous = True) 
  rate = rospy.Rate(5) 
  #time.sleep(3) 

  while not rospy.is_shutdown(): 
    package = m.listener(usb, baud) 
      
    info = package.split(",") 
    coords = [float(info[0]),float(info[1]),float(info[2]),float(info[3]),float(info[4]), float(info[5])] 
    rpm_1=coords[1] 
    rpm_2=coords[3] 
    rpm_3=coords[0] 
    rpm_4=coords[2] 
    v_x = 1*(rpm_1 + rpm_2 + rpm_3 + rpm_4) 
    v_y = 1*(-rpm_1 + rpm_2 + rpm_3 - rpm_4) 
    #print(coords) 
    #print(v_x, v_y) 
    Ax = coords[4] 
    Ay = coords[5] 
    battery = info[6]  
      
    tr_x, tr_y = updateSensor([Ax, Ay, v_y, v_x], pos_x, pos_y, dt) 
    pos_x = tr_x[0][0] 

    pos_y = tr_y[0][0] 
    z = [ tr_x[0][0] ]                      
    filter.predict()                            
    filter.update(z) 
      
    z = [ tr_y[0][0] ]                      
    filter_y.predict()                            
    filter_y.update(z)  
    
  #filteredState.append(filter.x) 
  #stateCovarianceHistory.append(filter.P)                            

  #filteredState_y.append(filter_y.x) 
  #stateCovarianceHistory_y.append(filter_y.P) 
    
  #rospy.loginfo(np.array(filteredState)[:,0]) 
  pub.publish(str((filter.x).tolist())+"/"+ 
  str((filter_y.x).tolist())) 
  print(filter.x[0], filter_y.x[0]) 
  rate.sleep() 
    
if __name__ == "__main__": 
  try: 
    position_from_sensors() 
  except rospy.ROSInterruptException: 
    pass