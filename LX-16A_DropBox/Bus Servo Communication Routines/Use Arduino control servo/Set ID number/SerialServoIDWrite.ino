

#define GET_LOW_BYTE(A) (uint8_t)((A))
//Macro function  get lower 8 bits of A
#define GET_HIGH_BYTE(A) (uint8_t)((A) >> 8)
//Macro function  get higher 8 bits of A
#define BYTE_TO_HW(A, B) ((((uint16_t)(A)) << 8) | (uint8_t)(B))
//Macro Function  put A as higher 8 bits   B as lower 8 bits   which amalgamated into 16 bits integer

#define LOBOT_SERVO_FRAME_HEADER         0x55
#define LOBOT_SERVO_ID_WRITE             13

byte LobotCheckSum(byte buf[])
{
  byte i;
  uint16_t temp = 0;
  for (i = 2; i < buf[3] + 2; i++) {
    temp += buf[i];
  }
  temp = ~temp;
  i = (byte)temp;
  return i;
}

void LobotSerialServoSetID(HardwareSerial &SerialX, uint8_t oldID, uint8_t newID)
{
  byte buf[7];
  buf[0] = buf[1] = LOBOT_SERVO_FRAME_HEADER;
  buf[2] = oldID;
  buf[3] = 4;
  buf[4] = LOBOT_SERVO_ID_WRITE;
  buf[5] = newID;
  buf[6] = LobotCheckSum(buf);
  SerialX.write(buf, 7);
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200); //Baud rate is 115200
  pinMode(13, OUTPUT);
  delay(1000);
}


void loop() {
  // put your main code here, to run repeatedly:
  delay(500);
  digitalWrite(13,HIGH);  //Indicator  run indication
  LobotSerialServoSetID(Serial, 254, 1); // The first parameter is the serial port which is used for communication. The second parameter is old ID ( the number of old ID is 254 , which is valid for all online servo when you send commands to them) 
                                           //The third parameter is new ID
  delay(500);
  digitalWrite(13,LOW);
}
