import serial, logging, collections, time

class Devices:
    def __init__(self, portnum = None, DeviceName = None ):
        self.ser = None
        self.__name = DeviceName
        self.__portName = portnum
        self.__battStat = [0,0.0,0,0.0]
        try:
            self.ser = serial.Serial(
                        port         = portnum,
                        baudrate    = 115200,
                        bytesize    = serial.EIGHTBITS,
                        parity      = serial.PARITY_NONE,
                        stopbits    = serial.STOPBITS_ONE,
                        timeout     = 3, #seconds
                        writeTimeout= 1, #seconds
                        rtscts         = False 
                        ) 
            
        except Exception as e:
            if self.ser:
                self.ser.close()
            raise
        

        # if self.ser.name != None:
            # print "UART %s on port %s" % ("open" if self.ser else "closed", self.ser.name)

    def __del__(self):
        if self.ser:
            logging.info("closing UART")
            self.ser.close()

    def __updateBattData(self):
	x = self.ser.write("CF\n")
        time.sleep(0.01)
        y = self.ser.read(8)
        self.__battStat[0] = ord(y[3]) + (256 * ord(y[4]) )
        self.__battStat[2] = ord(y[5]) + (256 * ord(y[6])) 
        self.__battStat[1] = round( (((float(self.__battStat[0])/1024*4.096)-0.4)/0.0195),1 )
        self.__battStat[3] = round( ((float(self.__battStat[2])/1024*4.096)/0.352),2 )
        
    def __updateName(self):
	self.ser.write("CA\n")
        time.sleep(0.01)
        y = self.ser.read(7)
	self.__name = str(y).strip()
        
    def getName(self):
        self.__updateName()
	return self.__name

    def getBattStat(self):
        self.__updateBattData()
	return self.__battStat

    def getPortName(self):
	return self.__portName

