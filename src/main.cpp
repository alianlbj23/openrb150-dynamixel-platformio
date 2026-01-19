#include <Arduino.h>
#include <Dynamixel2Arduino.h>

// OpenRB-150 預設 DXL TTL 腳位
#define DXL_SERIAL   Serial1
#define DXL_DIR_PIN  2   // OpenRB-150 預設方向控制腳

Dynamixel2Arduino dxl(DXL_SERIAL, DXL_DIR_PIN);

void setup()
{
  Serial.begin(57600);
  while (!Serial) {
    ; // 等待 USB Serial
  }

  Serial.println("=== DYNAMIXEL ID Scan Start ===");

  // 初始化 DXL
  dxl.begin(57600);             // 常見 baudrate
  dxl.setPortProtocolVersion(2.0);  // 大多新款是 Protocol 2.0

  bool found_any = false;

  // 掃描 ID 1~252
  for (uint8_t id = 1; id <= 252; id++) {
    if (dxl.ping(id)) {
      Serial.print("Found DYNAMIXEL ID: ");
      Serial.println(id);
      found_any = true;
    }
  }

  if (!found_any) {
    Serial.println("No DYNAMIXEL found.");
  }

  Serial.println("=== Scan Done ===");
}

void loop()
{
  // 不用重複掃描
}
