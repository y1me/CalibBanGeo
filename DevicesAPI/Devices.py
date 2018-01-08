import serial, logging, collections, time

STARTADDEEPROM = '0'
MAGICCALIBANGLE = 21.641

class Devices:
    def __init__(self, portnum = None, DeviceName = None ):
        self.ser = None
        self.__name = DeviceName
        self.__portName = portnum
        self.__battStat = [0,0.0,0,0.0]
        self.__anlgInput = [0,0,0,0,0.0,0.0,0.0,0.0]
        self.__calibValue = []
        self.__Zero = []
        self.__Sensi = []
        self.__DeltaS = []
        self.__Angle = []
        try:
            self.ser = serial.Serial(
                        port         = portnum,
                        baudrate    = 115200,
                        bytesize    = serial.EIGHTBITS,
                        parity      = serial.PARITY_NONE,
                        stopbits    = serial.STOPBITS_ONE,
                        timeout     = 5, #seconds
                        writeTimeout= 5, #seconds
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
        return self.__name[3:]

    def getBattStat(self):
        self.__updateBattData()
	return self.__battStat

    def getPortName(self):
	return self.__portName

    def __updateInputData(self):
	x = self.ser.write("CG\n")
        time.sleep(0.015)
        y = self.ser.read(12)
        i = 0
        while(i < 4):
            self.__anlgInput[i] = ord(y[2*i+3]) + (256 * ord(y[2*i+4]) )
            if self.__anlgInput[i] > 32768:
                 self.__anlgInput[i] -= 65536
            i += 1
        i = 0
        while(i < 4):
            self.__anlgInput[i+4] = round(( float(self.__anlgInput[i])/32767*4.096 ),5)
            i += 1

    def getAnalogIN(self):
        self.__updateInputData()
	return self.__anlgInput

    def WriteCalib(self,Address):
        x = self.ser.write("CH"+Address+"\n")
        time.sleep(0.015)

    def ReadCalib(self,Address):
        x = self.ser.write("CK"+Address+"\n")
        time.sleep(0.015)
        y = self.ser.read(6)
        value = ord(y[4]) + (256 * ord(y[3]))
        if value > 32768:
            value -= 65536
        return value

    def __updateCalib(self):
        self.__calibValue = []
        self.__Zero = []
        self.__Sensi = []
        for k in range(12):
            self.__calibValue.append( self.ReadCalib(chr(ord(STARTADDEEPROM)+k)) )
        for k in range(4):
            self.__Zero.append( self.__calibValue[k] )
            self.__Sensi.append( (self.__calibValue[k + 8] -  self.__calibValue[k + 4]) / MAGICCALIBANGLE )   
    
    def getCalibValue(self):
        self.__updateCalib()
        return self.__calibValue
    
    def getZeroValue(self):
        self.__updateCalib()
        return self.__Zero
    
    def getSensiValue(self):
        self.__updateCalib()
        return self.__Sensi

    def updateDeltaS(self,DeltaValue):
        self.__DeltaS = DeltaValue

    def getDeltaS(self):
        return self.__DeltaS


