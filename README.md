# darkwire

[![darkwire](https://img.shields.io/static/v1?label=&message=darkwire&style=for-the-badge&logo=bitcoin&logoSize=auto&labelColor=0A0A0A&color=00FF41)](https://github.com/cyb3r17/darkwire)
[![License: MIT](https://img.shields.io/static/v1?label=License&message=MIT&style=for-the-badge&logo=opensourceinitiative&logoSize=auto&labelColor=0A0A0A&color=FF003C)](https://github.com/cyb3r17/darkwire/blob/main/LICENSE)
[![Documentation](https://img.shields.io/static/v1?label=Docs&message=Download&style=for-the-badge&logo=gitbook&logoSize=auto&labelColor=0A0A0A&color=00B4D8)](https://github.com/cyb3r17/darkwire)
[![YouTube Demo](https://img.shields.io/static/v1?label=Demo&message=YouTube&style=for-the-badge&logo=youtube&logoSize=auto&labelColor=0A0A0A&color=FF0000)](https://www.youtube.com/watch?v=vEsVZjViFdM)
[![GitHub Issues](https://img.shields.io/github/issues/cyb3r17/darkwire?style=for-the-badge&logo=github&logoSize=auto&labelColor=0A0A0A&color=11A836)](https://github.com/cyb3r17/darkwire/issues)
[![GitHub Stars](https://img.shields.io/github/stars/cyb3r17/darkwire?style=for-the-badge&logo=github&logoSize=auto&labelColor=0A0A0A&color=FF003C)](https://github.com/cyb3r17/darkwire/stargazers)
![Profile Views](https://komarev.com/ghpvc/?username=cyb3r17&style=for-the-badge&logo=github&logoSize=auto&labelColor=0A0A0A&color=00FF41)
[![Website](https://img.shields.io/static/v1?label=Website&message=darkwire&style=for-the-badge&logo=firefox&logoSize=auto&labelColor=0A0A0A&color=00B4D8)](https://darkwire.cyb3r17.space)
[![Reddit Discussion](https://img.shields.io/static/v1?label=Reddit&message=r/Bitcoin&style=for-the-badge&logo=reddit&logoSize=auto&labelColor=0A0A0A&color=FF4500)](https://www.reddit.com/r/Bitcoin/comments/1kq84a1/send_bitcoin_without_the_internet/)
[![X Thread](https://img.shields.io/static/v1?label=X&message=Thread&style=for-the-badge&logo=x&logoSize=auto&labelColor=0A0A0A&color=FFFFFF)](https://x.com/cyb3r_17/status/1924057524107718861)
[![Hackathon](https://img.shields.io/static/v1?label=Hackathon&message=Bitcoin%202025&style=for-the-badge&logo=bitcoin&logoSize=auto&labelColor=0A0A0A&color=F7931A)](https://bitcoin2025.com)

![darkwire Banner](static/imgs/darkwire88x31.png)

**The internet is optional. Freedom isn't.**

darkwire is an open-source project that enables **off-grid Bitcoin transactions and messaging** using **LoRa-based mesh networks**. Built for censored regions, darkwire empowers activists, humanitarians, and freedom fighters to maintain financial and communicative sovereignty during internet blackouts or surveillance. Submitted for the **Bitcoin 2025 Official Hackathon**, darkwire is inspired by real-life stories of individuals bypassing centralized control to achieve freedom.

🌐 **Join the resistance:** [github.com/cyb3r17/darkwire](https://github.com/cyb3r17/darkwire)

## Why darkwire?

In a world where **80% of people live under authoritarian or partly free regimes**, reliance on fragile internet and power infrastructure is a vulnerability. darkwire provides a resilient, censorship-resistant communication layer using LoRa technology, independent of ISPs, carriers, or satellites.

**Inspiration**:
- **Evan, a priest from Zimbabwe**: Used Bitcoin to survive hyperinflation, bypassing banks to provide essentials for his community.
- **Lezhi, a Chinese programmer**: Embedded messages about corporate control on the Ethereum blockchain, smuggling truth when other channels were blocked.

darkwire ensures these actions remain possible even when internet and electricity fail.

## How It Works

darkwire uses LoRa radio modules to transmit encrypted data packets over a mesh network, with each node covering **5-10km in rural areas** or **1-3km in urban environments**. A few strategically placed nodes can span vast areas.

**Process**:
1. **Sign**: Authenticate your message or Bitcoin transaction.
2. **Fragment**: Break data into packets if needed.
3. **Encrypt**: Secure data for privacy.
4. **Transmit**: Send via LoRa, hopping across nodes until reaching the destination or an internet-connected exit node.

**Modes**:
- Bitcoin transactions (manual UTXO management; LoRa-based UTXO retrieval planned).
- Simple text messages/Tweets.

📺 **See it in action**:
- [Transmitter Node with GUI](https://github.com/user-attachments/assets/da19390c-9608-41bd-924a-bcd7f17aab93)
- [Receiver Node with Arduino IDE](https://github.com/user-attachments/assets/525d0014-25df-46ff-83b7-58066d4e5735)

📹 **Full Demo**: [How darkwire Works](https://www.youtube.com/watch?v=vEsVZjViFdM)

![darkwire Node](static/imgs/darkwire_node.png)

## Project Structure

- **src/**: Source code and assets.
  - **src/hardware/**: Arduino sketches for nodes.
    - `receiver.ino`: Configures a node as a receiver.
    - `transceiver.ino`: Configures a node for both transmitting and receiving (mesh).
    - `transmitter.ino`: Configures a node as a transmitter.
  - **src/website/**: Source code for the informational website.
  - **src/darkwire.png**: Project logo.
  - **src/gui_sender.py**: Python script for a GUI to interact with nodes (sending focus).

## Hardware Requirements

- **Microcontroller**: Arduino UNO or compatible (e.g., ESP32, Teensy).
- **Transceiver**: LoRa module (SX1276, SX1278, SX1272).
- **Antenna**: Suitable for your LoRa module’s frequency band (check local regulations).
- **Power**: Solar panels, batteries, or direct power.
- **Enclosure**: Weatherproof for outdoor use.
- **Connectivity**: Only one node needs internet to relay to the Bitcoin network.
- **Range**: 5-10km (rural), 1-3km (urban) per hop.

![Hardware Setup](static/imgs/lorabox.png)

## Software Setup

### Arduino Nodes
1. **Install Arduino IDE**: Download from [arduino.cc](https://www.arduino.cc/en/software).
2. **Install Libraries**:
   - `SPI` (included in Arduino IDE).
   - `LoRa` by Sandeep Mistry (via Library Manager: `Sketch > Include Library > Manage Libraries`).
3. **Upload Sketch**: Open `receiver.ino`, `transceiver.ino`, or `transmitter.ino`, select your board/port, and upload.
4. **Monitor**: Use Arduino IDE’s Serial Monitor (`Tools > Serial Monitor`) to view packets or debug.

### Python GUI (`gui_sender.py`)
1. **Install Python**: Ensure Python 3 is installed.
2. **Install Dependencies**:
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

*   **Project Website:** `darkwire.cyb3r17.space` (will be online temporarily)
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


📺 **See it in action**:
- [Transmitter Node with GUI](https://github.com/user-attachments/assets/da19390c-9608-41bd-924a-bcd7f17aab93)
- [Receiver Node with Arduino IDE](https://github.com/user-attachments/assets/525d0014-25df-46ff-83b7-58066d4e5735)

📹 **Full Demo**: [How darkwire Works](https://www.youtube.com/watch?v=vEsVZjViFdM)

![darkwire Node](static/imgs/darkwire_node.png)

## Deployment Methods

darkwire nodes are versatile and can be deployed in various environments:

- **High-Altitude Balloon Node**: Wide-area coverage using weather balloons for cross-border communication.
- **Maritime Buoy Node**: Solar-powered buoys connect regions across water bodies.
- **Portable Transceiver Node**: Compact, weatherproof nodes for urban or rural deployment.

### Deployment Scenarios

| Scenario | Description |
|----------|-------------|
| **English Channel** | Maritime buoys create a censorship-resistant corridor across waters. |
| **Indo-Tibetan Border** | Relay nodes enable transactions in mountainous, restricted areas. |
| **38th Parallel** | High-altitude balloons bridge the Korean border for financial freedom. |
| **Rafah Crossing** | Portable nodes support communication during humanitarian crises. |

![Deployment Example](static/imgs/38thpll.png)

## Technical Specifications

### Hardware Requirements
- **Microcontroller**: Arduino UNO or compatible
- **Transceiver**: LoRa Module (RA-02 or similar)
- **Power**: Solar panels, batteries, or direct power
- **Enclosure**: Weatherproof for outdoor use
- **Connectivity**: Only one node needs internet to relay to Bitcoin network
- **Range**: 10km (rural), 1-2km (urban) per hop

![Hardware Setup](static/imgs/lorabox.png)

## Community Feedback

> "80% of the world's population lives in either authoritarian or 'partly free' countries. The use case is obvious, and the idea is great. Make Bitcoin more unstoppable."  
> — *axnoro, Bitcoin Discord*

> "Fantastic project! This is what the community wants and needs!"  
> — *C10H24NO3PS, r/Bitcoin*

> "That's huge bro! I'm imagining the possibilities of radio transactions... it's like finding the holy grail in true freedom economies :D"  
> — *𝕏𝙿𝙴𝚁𝙸𝙼𝙴𝙽𝚃𝙸𝙽𝙶, X*

> "You did some great work. This has the potential to be one of the greatest developments of our time."  
> — *Popenga3000, r/Bitcoin*

Explore more in the [Community Feedback section](https://darkwire.cyb3r17.space/#testimonials).

## Join the Resistance

darkwire is open-source and built for those fighting for freedom. Download the documentation and start building your node today!

📜 **Get Started**: [Download Documentation](https://github.com/cyb3r17/darkwire)

### Support Us

Help spread the word by adding our button to your site:  
<a href="https://darkwire.cyb3r17.space"><img src="static/imgs/darkwire88x31.png" alt="darkwire Button"></a>

## License

This project is licensed under the [MIT License](https://github.com/cyb3r17/darkwire/blob/main/LICENSE).

---

**darkwire** - The internet is optional. Freedom isn't.
