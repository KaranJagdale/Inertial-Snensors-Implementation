import rospy
from fb5_torque_ctrl.msg import IMUmsg
from fb5_torque_ctrl.msg import GPSmsg
from fb5_torque_ctrl.msg import PwmInput

def CallbackIMU(msg):
  global accW
  accW = IMUmsg()
  accW.Ax = msg.Ax
  accW.Ay = msg.Ay
  accW.Az = msg.Az
  accW.Gx = msg.Gx
  accW.Gy = msg.Gy
  accW.Gz = msg.Gz

def CallbackGPS(msg):
  global pos
  pos = GPSmsg()
  pos.X = msg.N
  pos.Y = msg.E
  pos.Z = msg.d
  
def heading():
  gobal angle
  
  
  
def drawSquare():
  global pos, accW
  if
  
