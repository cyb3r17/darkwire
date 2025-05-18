# LoRa Ra-02 to Arduino Uno Connection Table

| LoRa Ra-02 Pin | Arduino Uno Pin | Description |
|----------------|-----------------|-------------|
| VCC            | 3.3V            | Power supply (3.3V only, do not use 5V) |
| GND            | GND             | Ground |
| NSS (CS)       | D10             | SPI Chip Select |
| MOSI           | D11             | SPI MOSI |
| MISO           | D12             | SPI MISO |
| SCK            | D13             | SPI Clock |
| DIO0           | D2              | Interrupt pin |
| DIO1           | D3              | Interrupt pin (optional) |
| RESET          | D9              | Reset pin |

## Important Notes

- The Ra-02 module operates at 3.3V. Make sure to power it from the Arduino's 3.3V pin, not the 5V pin.
- Some pins may be labeled differently on different Ra-02 modules (e.g., NSS may be labeled as CS).
- You may need a 3.3V to 5V level shifter if you want to ensure safe operation, but many users report success with direct connections.
- The DIO1 connection is optional for basic operations but may be required for certain advanced features.

