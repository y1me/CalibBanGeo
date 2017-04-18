import serial

class Devices:
    def __init__(self, portnum = None, DeviceName = None ):
        self.ser = None
        self.name = DeviceName

        try:
            self.ser = serial.Serial(
                        port         = portnum,
                        baudrate    = 115200,
                        bytesize    = serial.EIGHTBITS,
                        parity      = serial.PARITY_NONE,
                        stopbits    = serial.STOPBITS_ONE,
                        timeout     = 1, #seconds
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

        
    def updateName(self):
        self.ser.open()
	self.ser.write("CA\n")
	self.name = ser.read(7).strip()
        self.ser.close()
        
    def getName(self):
	return self.name

    def read(self, length, timeout = None):
        if timeout != self.ser.timeout:
            try:
                self.ser.timeout = timeout
            except ValueError as e:
                logging.error("Error setting UART read timeout. Continuing.")
            
        value = self.ser.read(length)
        if len(value) != length:
            raise Exceptions.SnifferTimeout("UART read timeout ("+ str(self.ser.timeout) +" seconds).")
        
        if self.useByteQueue:
            self.byteQueue.extend(stringToList(value))
        return value
            
    def readByte(self, timeout = None):
        readString = ""
        
        readString = self.read(1, timeout)
            
        return readString
        
    def readList(self, size, timeout = None):
        return self.read(size, timeout)
        
    def writeList(self, array, timeout = None):
        nBytes = 0
        if timeout != self.ser.writeTimeout:
            try:
                self.ser.writeTimeout = timeout
            except ValueError as e:
                logging.error("Error setting UART write timeout. Continuing.")
        try:
            nBytes = self.ser.write(array)
        except:
            self.ser.close()
            raise
        
        return nBytes
    

def list_serial_ports():
    # Scan for available ports.
    return list_ports.comports()

# Convert a list of ints (bytes) into an ASCII string
def listToString(list):
    str = ""
    for i in list:
        str+=chr(i)
    return str
    
# Convert an ASCII string into a list of ints (bytes)
def stringToList(str):
    lst = []
    for c in str:
        lst += [ord(c)]
    return lst
