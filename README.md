# Darkwire

**The internet is optional. Freedom isn't.**

Darkwire is an open-source project that enables off-grid communication and Bitcoin transactions using LoRa (Long Range Radio) technology. Born out of necessity and inspired by real-life stories of individuals bypassing centralized control and surveillance, Darkwire aims to provide a resilient and censorship-resistant communication layer independent of traditional internet infrastructure and satellites.

This project was submitted for the **Bitcoin 2025 Official Hackathon**.

## Why Darkwire?

In an increasingly centralized world where freedom of speech is throttled and financial transactions are constantly monitored, reliance on fragile infrastructure like the internet and power grids can be a point of vulnerability.

Darkwire is a response to this, inspired by stories like:
*   **Evan, a priest from Zimbabwe:** Used Bitcoin to survive hyperinflation and provide essentials to his community when the traditional financial system failed. Bitcoin became a necessity, bypassing banks and middlemen.
*   **Lezhi, a Chinese Programmer:** Used Ethereum to embed messages about corporate mind control operations on the blockchain, a way to smuggle truth in code when other avenues were blocked.

These vital actions hinged on the internet and electricity. Darkwire seeks to provide a layer of communication resilience even when these fail, ensuring that freedom of communication and transaction remains possible.

## How it Works

Darkwire uses LoRa radio modules to transmit encrypted packets of data. It functions as a mesh network, where each node can have a range of several kilometers (5-10 km in rural/plain environments, 3-5 km in urban environments). Just a few strategically placed nodes can cover a significant area.

Your message or transaction is:
1.  Signed (for authenticity).
2.  Fragmented (if necessary, for transmission).
3.  Encrypted (for privacy).
4.  Sent via LoRa, hopping from node to node until it reaches its destination.

There are no ISPs, no carriers, no satellites, and no central off-switch that can easily disable the network.

Darkwire currently supports two modes of operation:
*   Sending Bitcoin transactions.
*   Sending simple text messages/Tweets.

*Note: The initial Bitcoin functionality requires manual UTXO management. LoRa-based UTXO retrieval for complete internet freedom is a planned feature.*

## Project Structure

The repository is organized as follows:

*   `src/`: Contains all source code and project assets.
    *   `src/hardware/`: Contains Arduino sketches (`.ino` files) for the Darkwire nodes. These are designed to be uploaded to a microcontroller connected to a LoRa transceiver.
        *   `receiver.ino`: Sketch for a node configured primarily as a receiver.
        *   `transceiver.ino`: Sketch for a node configured as both a transmitter and receiver (for mesh networking).
        *   `transmitter.ino`: Sketch for a node configured primarily as a transmitter.
    *   `src/website/`: Contains the source code for the project's informational website (placeholder).
    *   `src/darkwire.png`: The project logo/image.
    *   `src/gui_sender.py`: A Python script providing a graphical user interface to interact with a connected Darkwire node (specifically designed for sending).

## Hardware Requirements

To build a Darkwire node, you will typically need:

*   An Arduino UNO (or compatible microcontroller like an ESP32, Teensy, etc.)
*   A LoRa transceiver module (e.g., based on the SX1276, SX1278, SX1272 chipsets).
*   A suitable antenna for your LoRa module's frequency band (ensure you comply with local radio regulations!).
*   Jumper wires to connect the microcontroller and LoRa module.
*   A USB A to B cable (for Arduino UNO) to connect the node to your computer.

Consult the specific `.ino` files in `src/hardware/` for pinout details and connections suitable for Arduino UNO + common LoRa modules.

## Software Setup

### For the Arduino Hardware Nodes (`.ino` files)

1.  **Install Arduino IDE:** Download and install the Arduino IDE from [arduino.cc](https://www.arduino.cc/en/software).
2.  **Install Libraries:** The Arduino sketches require the `SPI` and `LoRa` libraries.
    *   `SPI` is usually included by default in the Arduino IDE.
    *   The `LoRa` library can be installed via the Arduino IDE's Library Manager (`Sketch` > `Include Library` > `Manage Libraries...`). Search for "LoRa" and install the library by Sandeep Mistry.
3.  **Upload Sketch:** Open the desired `.ino` file (`receiver.ino`, `transceiver.ino`, or `transmitter.ino`) in the Arduino IDE. Select your board and port, and upload the sketch to your microcontroller.
4.  **Monitor Output:** Use the Arduino IDE's Serial Monitor (`Tools` > `Serial Monitor`) or a custom serial reading script/program to view incoming packets or debug output.

### For the Python GUI Sender (`gui_sender.py`)

1.  **Install Python:** Ensure you have Python 3 installed on your computer.
2.  **Install Dependencies:** The `gui_sender.py` script requires several Python libraries. Some are built-in, but others need to be installed using pip.

    The required libraries are:
    *   `tkinter` (built-in GUI library)
    *   `threading` (built-in for handling concurrent tasks)
    *   `time` (built-in for time-related functions)
    *   `serial` / `serial.tools.list_ports` (for serial communication with the Arduino)
    *   `bitcoinlib` (for handling Bitcoin wallets and transactions)
    *   `re` (built-in for regular expressions)

    You can install the external dependencies using pip:

    ```bash
    pip install pyserial bitcoinlib
    ```
    *(Note: The Python module is named `serial`, but the package name for pip is `pyserial`)*

3.  **Connect Hardware:** Connect your Darkwire node (running a transceiver or receiver sketch) to your computer via the USB cable.
4.  **Run the GUI:** Navigate to the project's `src/` directory in your terminal and run the script:

    ```bash
    python gui_sender.py
    ```

    The GUI application should open, allowing you to interface with the connected Darkwire node for sending transactions and messages.

## Deployment Scenarios

Darkwire is designed for environments where traditional communications might be restricted or unavailable. Potential scenarios include:

*   Cross-border communication in censored regions (e.g., Rafah Crossing, English Channel, Indo-Tibetan Border, 38th Parallel Korean Border - *as shown in the video*).
*   Disaster areas where infrastructure is down.
*   Remote locations without internet access.
*   Privacy-sensitive communication to bypass surveillance.

With a range of 5-10 km per node in ideal conditions, a network of just ~10 Darkwire nodes can theoretically provide coverage spanning 100+ kilometers! Nodes can be deployed in various ways (balloons, buoys, rooftops, handheld devices).

## Planned Features

*   **LoRa-based UTXO Retrieval:** Implement functionality to retrieve Unspent Transaction Outputs (UTXOs) over the LoRa network itself, eliminating the need for manual updates or temporary internet access for spending Bitcoin.
*   **More Cryptocurrency Support:** Extend support to other cryptocurrencies like Ethereum (ETH) and Monero (XMR) where off-grid transaction or message embedding is valuable.
*   **Improved Hardware Documentation:** Provide detailed PCB schematics and potentially custom PCB designs for more robust and reliable hardware compared to basic breadboard/jumper wire setups.
*   **Advanced Mesh Networking:** Enhance routing protocols for more efficient and reliable data transmission across a larger network of nodes.

## Contributing

Darkwire is Free and Open Source Software (FOSS!). Contributions are highly welcome. Whether you're a developer, hardware enthusiast, designer, or documentation writer, your skills can help.

1.  Fork the repository.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

Please ensure your code adheres to the project's style guidelines and includes appropriate tests.

## License

This project is licensed under the [MIT License](LICENSE).

## Links

*   **Project Website:** `darkwire.cyb3r17.space` (no longer available)
*   **GitHub Repository:** `github.com/cyb3r17/darkwire` (You are here!)
*   **Follow Updates (X/Twitter):** `x.com/cyb3r_17`


## Videos:

transmitter node with dakrwire gui
<video src="https://github.com/user-attachments/assets/da19390c-9608-41bd-924a-bcd7f17aab93" controls width="100%"></video>

receiver node with arduino IDE listening to LoRa inputs and printing them to the serial monitor
<video src="https://github.com/user-attachments/assets/525d0014-25df-46ff-83b7-58066d4e5735" controls width="100%"></video>

## Acknowledgements

*   Big thanks to the Bitcoin 2025 Official Hackathon for the opportunity to build and share Darkwire.

---
