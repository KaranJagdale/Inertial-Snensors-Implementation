import rospy
from fb5_torque_ctrl.msg import IMUmsg
from fb5_torque_ctrl.msg import GPSmsg
from fb5_torque_ctrl.msg import PwmInput
import math
count =0
currhead = 0
t1 = rospy.get_time() 
xt = [0, 0, 10, 10]
yt = [0, 10, 10, 0]
i = 0  
def CallbackIMU(msg):
  global accW,t1,count,currhead
  accW = IMUmsg()
  #accW.Ax = msg.Ax
  #accW.Ay = msg.Ay
  #accW.Az = msg.Az
  #accW.Gx = msg.Gx
  #accW.Gy = msg.Gy
  if(count !=0):
      currhead = (currhead + (t1-rospy.get_time())*accW.Gz)*0.98
  count = count+1
  accW.Gz = msg.Gz
  t1 = rospy.get_time()    
        
def CallbackGPS(msg):
  global pos
  pos = GPSmsg()
  pos.X = msg.N
  pos.Y = msg.E
  pos.Z = msg.d
   
def headCorrection(currhead,reqhead):
    pub_PWM=rospy.Publisher('pwmCmd_square',PwmInput,queue_size=10)
    pwmInput = PwmInput()
    while(((currhead-reqhead) > (5*3.14/180)) or ((currhead-reqhead) < (-5*3.14/180))):
        if(currhead>reqhead):
            pwmInput.rightInput = -150
            pwmInput.leftInput = 150
        if(currhead<reqhead):
            pwmInput.rightInput = 150
            pwmInput.leftInput = -150
        pub_PWM.publish(pwmInput)
        
  
def drawSquare():
    rospy.init_node('draw_square',anonymous=True)
    pub_PWM=rospy.Publisher('pwmCmd_square',PwmInput,queue_size=10)
    rospy.Subscriber("GPSmessage", GPSmsg, CallbackGPS,0)
    rospy.Subscriber("IMU message", IMUmsg, CallbackGPS,0)
    pwmInput = PwmInput()
    global pos, accW,i
    if ((xt[i]-pos.X)*(xt[i]-pos.X) + (yt[i]-pos.Y)*(yt[i]-pos.Y) < 1):
      i = i+1
      break
    
    if(i == 1):
      reqhead = math.atan((yt[i]-pos.Y)/(xt[i]-pos.X))
      
    else:
      reqhead = math.atan2((yt[i]-pos.Y)/(xt[i]-pos.X))
      
    
    headCorrection(currhead, reqhead)
      
    pwmInput.rightInput = 150
    pwmInput.leftInput = 150
    pub_PWM.publish(pwmInput)
     
if __name__ == '__main__':
    try:
        drawSquare()
    except rospy.ROSInterruptException:
        pass

    
