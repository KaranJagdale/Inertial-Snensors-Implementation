import serial
import io
ser=serial.Serial('/dev/ttyACM0',19200)


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
		

 
def main():
	s = ser.read(26)
	#for  i in s:
	s1 = map(bin,bytearray(s))
	N = bintodec(s1,17)
	E = bintodec(s1,21)
	D = bintodec(s1,25)
	print(s1)
	print(N,E,D)
main()







#print(' '.join(format(ord(x), 'b') for x in s))
#ser = io.BytesIO(b"some initial binary data: \x00\x01")
#print(ser[0])
#print(ord(s))
#print(toBinary(s))	#print((s1))
	#print(type(s1[0]))
	#print((s1[0][1]),int((s1[0][2])),(s1[0][3]))
ser.close()
