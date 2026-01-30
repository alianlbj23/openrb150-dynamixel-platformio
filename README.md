# OpenRB-150 Dynamixel PlatformIO Project

This is a sample project for developing on the [Robotis OpenRB-150](https://en.robotis.com/shop_en/item.php?it_id=902-0183-000) using [PlatformIO](https://platformio.org/), integrated with the [Dynamixel2Arduino](https://github.com/ROBOTIS-GIT/Dynamixel2Arduino) library.

## Related Resources

### PlatformIO Setup Reference
Configuration reference for using OpenRB-150 with PlatformIO.  
🔗 [Forum Discussion](https://forum.robotis.com/t/using-rb-150-with-platformio/6571/2)

### Dynamixel2Arduino Library
Official Dynamixel2Arduino library reference and documentation.  
📖 [Library Reference](https://www.arduinolibraries.info/libraries/dynamixel2-arduino)

### OpenRB-150 Board Driver
Official GitHub repository for OpenRB-150 board support.  
🔗 [GitHub Repository](https://github.com/ROBOTIS-GIT/OpenRB-150)

### OpenRB-150 Dynamixel ROS Controller
ROS controller package that uses rosbridge to connect and control Dynamixel motors on OpenRB-150 MCU flashed with micro-ROS firmware.  
🔗 [GitHub Repository](https://github.com/alianlbj23/openrb150-dynamixel-ros-controller)

### OpenRB-150 Arduino Development Board
Arduino-compatible controller with 4 dedicated DYNAMIXEL ports, supporting X/MX/AX/P series motors.  
📖 [OpenRB-150 Documentation](https://emanual.robotis.com/docs/en/parts/controller/openrb-150/)

### DYNAMIXEL Wizard 2.0
Official GUI tool for configuring DYNAMIXEL motors - supports firmware updates, motor testing, real-time data plotting, and control table management.  
📖 [DYNAMIXEL Wizard 2.0 Documentation](https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_wizard2/)  
💾 Download: [Windows](http://www.robotis.com/service/download.php?no=1670) | [Linux](http://www.robotis.com/service/download.php?no=1671) | [macOS](http://www.robotis.com/service/download.php?no=1760)

## Project Structure

```
.
├── boards/
│   └── OpenRB-150.json  # Custom board definition
├── lib/                 # Project libraries
├── platformio.ini       # PlatformIO project configuration file
├── src/
│   └── main.cpp         # Main application code
└── variants/
    └── OpenRB-150/      # Variant configuration for OpenRB-150
```

## Custom Board

This project uses `OpenRB-150.json` located in the `boards/` directory as a custom board definition. This allows you to define specific hardware parameters for the OpenRB-150.

Key settings within `OpenRB-150.json`:
- **`"variant": "OpenRB-150"`**: Specifies the name of the variant folder.
- **`"variants_dir": "variants"`**: Tells PlatformIO to look for the variant folder inside the `variants` directory at the project root.

The `platformio.ini` file uses this definition with `board = OpenRB-150`. PlatformIO automatically finds `OpenRB-150.json` in the `boards` folder and then locates the correct variant files using the paths defined within the JSON file.

## `platformio.ini` Configuration

The project's `platformio.ini` contains the following important settings:

- **`platform = atmelsam`**: Specifies the Atmel SAM hardware platform.
- **`board = OpenRB-150`**: Specifies the custom board defined in the `boards/` directory.
- **`framework = arduino`**: Uses the Arduino framework.
- **`lib_deps`**: Declares project library dependencies, in this case, `Dynamixel2Arduino`.
- **`build_flags`**:
  - `-Ivariants/OpenRB-150`: Adds the `variants/OpenRB-150` directory to the header search path, allowing the compiler to find files like `pins_arduino.h`.
- **`board_build.ldscript`**:
  - `variants/OpenRB-150/linker_scripts/gcc/flash_with_bootloader.ld`: Explicitly specifies the path to the linker script. This ensures the correct memory layout is used during linking, which is especially important when working with a custom bootloader.

## How to Use

1.  Install [Visual Studio Code](https://code.visualstudio.com/) and the [PlatformIO IDE extension](https://platformio.org/install/ide?install=vscode).
2.  Clone this repository.
3.  Open the project folder in VS Code.
4.  PlatformIO will automatically install the required toolchains and libraries.
5.  Use the "Build" and "Upload" buttons in the PlatformIO toolbar to compile and upload your code.

## Running micro-ROS Agent

To connect your OpenRB-150 to ROS2 using micro-ROS, you need to run a micro-ROS agent on your host machine. Use the following Docker command:

```bash
docker run -it --rm --net=host --privileged \
  -v /dev:/dev \
  microros/micro-ros-agent:jazzy \
  serial --dev /dev/ttyACM0 -b 115200 -v6
```

**Note**: The micro-ROS agent version (`jazzy` in this example) should match the ROS2 distribution specified in `platformio.ini`. To change the ROS2 version, modify the `board_microros_distro` parameter in the `platformio.ini` file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
