# OpenRB-150 Dynamixel PlatformIO Project

This is a sample project for developing on the [Robotis OpenRB-150](https://en.robotis.com/shop_en/item.php?it_id=902-0183-000) using [PlatformIO](https://platformio.org/), integrated with the [Dynamixel2Arduino](https://github.com/ROBOTIS-GIT/Dynamixel2Arduino) library.

## Related Resources

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
