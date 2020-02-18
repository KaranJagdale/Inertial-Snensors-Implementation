import rospy
import serial
import io
ser=serial.Serial('/dev/ttyACM0',19200)
from fb5_torque_ctrl.msg import GPSmsg
#define message in cmakelist

def bintodec(k,l):
	decimal = 0
	binary = []
	for i in range(4):
		nzeros = 10 - len((k[l-i]))
		print(nzeros)
		for j in range(nzeros):
			binary.append(0)
		for j in range(len(k[l-i])-2):
				binary.append(int((k[l-i][j+2])))      #Not appending initial 0b
	print(binary)
	if(binary[0]==1):
		for i in range(len(binary)):
			if(binary[i] == 1):
				binary[i] = 0
			else:
				binary[i] = 1
			decimal = decimal + int(binary[i])*pow(2,(len(binary)-(i+1)))
		return -(decimal+1)
	
	else:
		for i in range(len(binary)):
			decimal = decimal + int(binary[i])*pow(2,(len(binary)-(i+1)))
		
		return decimal
		

 
def pub():
  rospy.init_node('pubGPS',anonymous = True)
  pub = rospy.Publisher('GPSmessage',GPSmsg,queue_size = 10)
  msg = GPSmsg()
  while not rospy.is_shutdown():
	  s = ser.read(26)
	#for  i in s:
	  s1 = map(bin,bytearray(s))
	  msg.N = bintodec(s1,17)
	  msg.E = bintodec(s1,21)
	  msg.D = bintodec(s1,25)
	  #print(s1)
	  print(msg)


if __name__ == '__main__':
    try:
        pub()
    except rospy.ROSInterruptException:
        pass





#print(' '.join(format(ord(x), 'b') for x in s))
#ser = io.BytesIO(b"some initial binary data: \x00\x01")
#print(ser[0])
#print(ord(s))
#print(toBinary(s))	#print((s1))
	#print(type(s1[0]))
	#print((s1[0][1]),int((s1[0][2])),(s1[0][3]))
ser.close()
