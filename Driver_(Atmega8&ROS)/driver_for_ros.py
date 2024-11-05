#Driver for ROS to communicate with Atmega8 driver 
import serial 
import math  
 
def stop(ser): 
    com = 'a:'  
    send_com(ser, com) 
 
def forward(ser, a, b):  
    com = 'b' + str(a) + str(b) + ':'  
    send_com(ser, com)   
     
def backward(ser, a, b): 
    com = 'c' + str(a) + str(b) + ':' 
    send_com(ser, com) 
     
def right(ser, a, b): 
    com = 'd' + str(a) + str(b) + ':' 
    send_com(ser, com) 
     
def left(ser, a, b): 
    com = 'e' + str(a) + str(b) + ':' 
    send_com(ser, com) 
 
def right_up_diagonally(ser, a): 
    com = 'f' + str(a) + ':' 
    send_com(ser, com) 
     
def left_up_diagonally(ser, a): 
    com = 'g' + str(a) +':' 
    send_com(ser, com) 
     
def right_down_diagonally(ser, a): 
    com = 'h' + str(a) + ':' 
    send_com(ser, com) 
     
def left_down_diagonally(ser, a): 
    com = 'i' + str(a) + ':' 
    send_com(ser, com) 
     
 
def euc(point_1, point_2): 
    return ((point_1[0] - point_2[0])**2 + ((point_1[1] - 
point_2[1])**2))**0.5 
 
    
def send_com(ser, com): 
    for i in range(len(com)): 
        ser.write(com[i].encode()) 
         
         
def get_angle(start, goal): 
    x, y = start[0], start[1] 
    x_g, y_g = goal[0], goal[1] 
    radi = math.atan2(y_g - y, x_g - x) 
    degr = radi*180/math.pi 
     
    if x_g < x and y_g < y: 
        degr = 180 - abs(degr)  
         
    elif x_g > x and y_g < y: 
 
        degr = abs(degr) 
         
    elif x_g < x and y_g > y: 
        degr = 180 - degr 
         
    return degr*math.pi/180 
     
     
def speed_manager(v, R_w, start, goal): 
    beta = get_angle(start, goal) 
    v_x = v * math.sin(beta) 
    v_y = v * math.cos(beta) 
    print((v_x + v_y)/R_w) 
    rpm_1 = abs((v_x - v_y)/R_w) 
    rpm_2 = (v_x + v_y)/R_w 
    return rpm_1, rpm_2 
 
 
def move_to_point(ser, start, goal): 
    v = 200 
    R_w = 4 
     
     
    x_start, y_start = start[0], start[1] 
    x_goal, y_goal = goal[0], goal[1] 
     
    rpm_1, rpm_2 = speed_manager(v, R_w, start, goal) 
    print(rpm_2) 
    if x_goal > x_start and y_goal > y_start: 
        if y_goal - y_start == x_goal - x_start: 
            right_up_diagonally(ser, v/R_w) 
        elif y_goal - y_start > x_goal - x_start: 
            forward(ser, rpm_2, rpm_1) 
        elif y_goal - y_start < x_goal - x_start: 
            right(ser, rpm_2, rpm_1) 
         
    elif x_goal < x_start and y_goal > y_start: 
        if y_goal - y_start == x_start - x_goal: 
            left_up_diagonally(ser, v/R_w) 
        elif y_goal - y_start > x_start - x_goal: 
            forward(ser, rpm_1, rpm_2) 
        elif y_goal - y_start < x_start - x_goal: 
            left(ser, rpm_1, rpm_2) 
         
    elif x_goal < x_start and y_goal < y_start: 
        if y_start - y_goal == x_start - x_goal: 
            left_down_diagonally(ser, v/R_w ) 
        elif y_start - y_goal > x_start - x_goal: 
            backward(ser, rpm_2, rpm_1) 
        elif y_start - y_goal < x_start - x_goal: 
            left(ser, rpm_2, rpm_1) 
         
    elif x_goal > x_start and y_goal < y_start: 
        if y_start - y_goal == x_goal - x_start: 
            right_down_diagonally(ser, v/R_w) 
        elif y_start - y_goal > x_goal - x_start: 
            backward(ser, rpm_1, rpm_2) 
        elif y_start - y_goal < x_goal - x_start: 
            right(ser, rpm_1, rpm_2) 
             
    elif x_goal > x_start and y_goal == y_start: 
        right(ser, v/R_w, v/R_w) 
         
    elif x_goal < x_start and y_goal == y_start: 
        left(ser, v/R_w, v/R_w) 
         
    elif x_goal == x_start and y_goal > y_start: 
        forward(ser, v/R_w, v/R_w) 
         
    elif x_goal == x_start and y_goal < y_start: 
        backward(ser, v/R_w , v/R_w) 
         
    ser.close()