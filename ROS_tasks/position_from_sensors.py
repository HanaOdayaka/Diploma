num = "move_x" 
 
def distance_x(x, camera_x): 
  global num 


  if x > 0: 
    return "right" 
  if x < 0: 
    return "left" 
  else: 
    num = "move_y" 
  return "stop" 
   
def distance_y(y, camera_y): 
  global num 
  if abs(y)>5: 
    return "forward" 
  else: 
    return "stop"  

def rotate(angle_x, angle_y): 
  if angle_y < 0: 
    return "rotate_right" 
  if angle_y > 0: 
    return "rotate_left" 
  if abs(angle_y) == 0: 
    num = "move" 
  return "stop" 
  
def moving(coords): 
  global num 
  x = int(coords[0][0]) 
  y = int(coords[0][1]) 
  camera_x = int(coords[1][0]) 
  camera_y = int(coords[1][1]) 
  angle_x = int(coords[2]) 
  angle_y = int(coords[3]) 

  print (x) 
  num1 = "stop" 
  if num == "move_x": 
    #num1 = rotate(angle_x, angle_y) 
    
    return distance_x(x, camera_x) 

  if num == "move_y": 
    return distance_y(y, camera_y) 
    
  if num == "rotate": 
    return rotate(angle_x, angle_y) 
    
  return num1 