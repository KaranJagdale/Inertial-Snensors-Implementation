import rospy
from fb5_torque_ctrl.msg import IMU
from fb5_torque_ctrl.msg import GPS
from fb5_torque_ctrl.msg import PwmInput
import math
count =0
currhead = 0
t1 = rospy.get_time() 
xt = [0, 0, 10, 10]
yt = [0, 10, 10, 0]
i = 0 
publish = False 

        
def CallbackGPS(msg):
  global pos
  pos = GPS()
  pos.N = msg.N
  pos.E = msg.E
  #pos.Z = msg.d
   
def headCorrection(currhead,reqhead):
    pub_PWM=rospy.Publisher('pwmCmd_square',PwmInput,queue_size=10)
    pwmInput = PwmInput()
    while(((currhead-reqhead) > (5*3.14/180)) or ((currhead-reqhead) < (-5*3.14/180))):
        if(currhead>reqhead):
            pwmInput.rightInput = -120
            pwmInput.leftInput = 120
        if(currhead<reqhead):
            pwmInput.rightInput = 120
            pwmInput.leftInput = -120
        pub_PWM.publish(pwmInput)
		      
  
def drawSquare():
    while not rospy.is_shutdown():
        global pos, accW,i,publish
        if (publish == False):
            initial_pos = [pos.N, pos.E]
        pwmInput = PwmInput()
        
        if ((pos.N-initial_pos[0])*(pos.N-initial_pos[0]) + (pos.E-initial_pos[1])*(pos.E-initial_pos[1]) < 10):
            pwmInput.rightInput = 150
            pwmInput.leftInput = 150
            pub_PWM.publish(pwmInput)
            publish = True
        else:
            pwmInput.rightInput = 0
            pwmInput.leftInput = 0
            pub_PWM.publish(pwmInput)
	
     
if __name__ == '__main__':
    rospy.init_node('draw_square',anonymous=True)
    pub_PWM=rospy.Publisher('pwmCmd0',PwmInput,queue_size=10)
    rospy.Subscriber("GPSmessage", GPS, CallbackGPS,0)
    #rospy.Subscriber("IMU message", IMU, CallbackGPS,0)
    try:
        drawSquare()
    except rospy.ROSInterruptException:
        pass
