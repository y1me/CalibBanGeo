import serial, logging, collections, time

class Devices:
    def __init__(self, portnum = None, DeviceName = None ):
        self.ser = None
        self.name = DeviceName
        self.portName = portnum
        self.Tbat = None
        self.Vbat = None
        self.TbatRaw = None
        self.VbatRaw = None
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

    def updateBattData(self):
	x = self.ser.write("CF\n")
        time.sleep(0.01)
        y = self.ser.read(8)
        self.TbatRaw = ord(y[3]) + (256 * ord(y[4]) )
        self.VbatRaw = ord(y[5]) + (256 * ord(y[6])) 
        self.Tbat = round( (((float(self.TbatRaw)/1024*4.096)-0.4)/0.0195),1 )
        self.Vbat = round( ((float(self.VbatRaw)/1024*4.096)/0.352),2 )
        
    def updateName(self):
	x = self.ser.write("CA\n")
        time.sleep(0.01)
        y = self.ser.read(7)
	self.name = str(y).strip()
        
    def getName(self):
	return self.name

    def getTempBatt(self):
	return self.Tbat

    def getVoltBatt(self):
	return self.Vbat

    def getTempBattRaw(self):
	return self.TbatRaw

    def getVoltBattRaw(self):
	return self.VbatRaw

    def getPortName(self):
	return self.portName

