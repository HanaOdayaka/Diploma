import os 
os.environ["OPENBLAS_CORETYPE"] = "nehalem" 
import numpy as np 
import cv2 
import cv2.aruco as aruco 
import sys, time, math 
 
id_to_find  = 68 
marker_size  = 5 #- [cm] 
 
def isRotationMatrix(R): 
  Rt = np.transpose(R) 
  shouldBeIdentity = np.dot(Rt, R) 
  I = np.identity(3, dtype=R.dtype) 
  n = np.linalg.norm(I - shouldBeIdentity) 
  return n < 1e-6 
  
def rotationMatrixToEulerAngles(R): 
  assert (isRotationMatrix(R)) 

  sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0]) 

  singular = sy < 1e-6 

  if not singular: 
      x = math.atan2(R[2, 1], R[2, 2]) 
      y = math.atan2(-R[2, 0], sy) 
      z = math.atan2(R[1, 0], R[0, 0]) 
  else: 
      x = math.atan2(-R[1, 2], R[1, 1]) 
      y = math.atan2(-R[2, 0], sy) 
      z = 0 

  return np.array([x, y, z]) 
 
calib_path  = "/home/orangepi/car_ws/src/battery_station/scripts/" 
camera_matrix   = np.loadtxt(calib_path+'cameraMatrix_webcam.txt', 
delimiter=',') 
camera_distortion   = np.loadtxt(calib_path+'cameraDistortion_webcam.txt', 
delimiter=',') 
 
R_flip  = np.zeros((3,3), dtype=np.float32) 
R_flip[0,0] = 1.0 
R_flip[1,1] =-1.0 
R_flip[2,2] =-1.0 
 
aruco_dict  = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL) 
parameters  = aruco.DetectorParameters_create() 
 
font = cv2.FONT_HERSHEY_PLAIN 
 
def aruco_main(frame):  
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
  corners, ids, rejected = aruco.detectMarkers(image=gray, 
  dictionary=aruco_dict, parameters=parameters) 
  if ids is not None and ids[0] == id_to_find: 

    ret = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, camera_distortion) 
    rvec, tvec = ret[0][0,0,:], ret[1][0,0,:] 

    aruco.drawDetectedMarkers(frame, corners) 
    aruco.drawAxis(frame, camera_matrix, camera_distortion, rvec, 
    tvec, 10) 

    str_position = "MARKER Position x=%4.0f  y=%4.0f  z=%4.0f"%(tvec[0], tvec[1], tvec[2]) 
    cv2.putText(frame, str_position, (0, 100), font, 1, (0, 255, 0), 2, cv2.LINE_AA) 

    R_ct = np.matrix(cv2.Rodrigues(rvec)[0]) 
    R_tc = R_ct.T 

    roll_marker, pitch_marker, yaw_marker = rotationMatrixToEulerAngles(R_flip*R_tc) 
    str_attitude = "MARKER Attitude r=%4.0f  p=%4.0f  y=%4.0f"%(math.degrees(roll_marker),math.degrees(pitch_marker), 
                              math.degrees(yaw_marker)) 
    cv2.putText(frame, str_attitude, (0, 150), font, 1, (0, 255, 0), 2, cv2.LINE_AA) 
    pos_camera = -R_tc*np.matrix(tvec).T 
    str_position = "CAMERA Position x=%4.0f  y=%4.0f  z=%4.0f"%(pos_camera[0], pos_camera[1], pos_camera[2]) 
    cv2.putText(frame, str_position, (0, 200), font, 1, (0, 255, 0), 2, cv2.LINE_AA) 
      
    roll_camera, pitch_camera, yaw_camera = 
    rotationMatrixToEulerAngles(R_flip*R_tc) 
    str_attitude = "CAMERA Attitude r=%4.0f  p=%4.0f  y=%4.0f"%(math.degrees(roll_camera),math.degrees(pitch_camera), math.degrees(yaw_camera)) 
    cv2.putText(frame, str_attitude, (0, 250), font, 1, (0, 255, 0), 2, cv2.LINE_AA) 
      
    return frame, [tvec, pos_camera, math.degrees(roll_marker),math.degrees(pitch_marker), math.degrees(yaw_marker)] 
    
  return frame, [[0,0,0], [0,0,0], 0, 0, 0] 