# 🩺 CARE COMPANION – A Guardian For Your Health At Home

> 🚀 *An AI + IoT-based Smart Healthcare Assistant for Patients and Elderly Care*  
> 👨‍⚕️ Built with **Raspberry Pi 4**, **Arduino**, and **Python**

---

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Raspberry%20Pi%204-red?logo=raspberrypi&logoColor=white" />
  <img src="https://img.shields.io/badge/Language-Python%203.10-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Framework-Flask-green?logo=flask" />
  <img src="https://img.shields.io/badge/Hardware-Arduino-orange?logo=arduino&logoColor=white" />
  <img src="https://img.shields.io/badge/Status-Prototype%20Completed-success?style=flat-square" />
</p>

---

## 🌟 Overview

**Care Companion** is a **smart home healthcare assistant** designed to assist patients through **health monitoring**, **emergency alerts**, and **AI-driven interaction**.  
Using **Raspberry Pi 4** as the core controller and **Arduino** for sensor integration, it ensures safety, medication reminders, and communication between patients and caregivers.

This project merges **IoT, AI, and embedded systems** to deliver a low-cost yet powerful solution for smart healthcare.

---

## 🎯 Objectives

- 🧠 Implement a **smart healthcare system** with Raspberry Pi 4 and Arduino.  
- ❤️ Continuously monitor **temperature, pulse rate, gas, and flame**.  
- 🚨 Send **real-time emergency alerts** and reminders.  
- 🗣 Integrate **voice command** for hands-free operation.  
- 🤖 Use **AI-based face and QR recognition** for intelligent movement.  
- 💾 Maintain a **dashboard + database** for patient health data.  

---

## ⚙️ Key Features

| Feature | Description |
|----------|-------------|
| 🦾 **Mobility & Detection** | Detects humans and QR codes, moves intelligently with obstacle avoidance |
| 💊 **Medication Reminder System** | Automatic drawer opens + buzzer rings after set interval |
| 🚨 **Emergency Panic Button** | Immediate alarm + caregiver notification |
| 🔥 **Gas & Fire Detection** | Detects hazards in real time |
| 🌡 **Temperature & Pulse Monitoring** | Measures health vitals using DHT11 and Pulse Sensor |
| 🗣 **Voice Command Control** | Recognizes commands like “Come Kiki” or “Go” |
| 📸 **Camera Integration** | Detects people, tracks movement |
| 💻 **Dashboard & Database** | Web-based real-time monitoring system |
| 🔊 **Audio Alerts & LED Indicators** | Visual and sound alerts for emergencies |
| 📱 **Bluetooth Connectivity** | Enables data sync with mobile apps |
| ☁️ **Future Expansion** | Emotion detection & cloud synchronization planned |

---

## 🧩 Hardware Components

| Section | Component | Model | Purpose |
|----------|------------|--------|----------|
| **Processor** | Raspberry Pi 4 | 8GB | Core control & AI logic |
| **Controller** | Arduino UNO | — | Sensor communication |
| **Temperature Sensor** | DHT11 | — | Measures body temperature |
| **Pulse Sensor** | Pulse Sensor Amped | — | Reads heart rate |
| **Gas Sensor** | MQ-2  | —     | Detects harmful gases |
| **Flame Sensor** | IR Flame Module | — | Fire detection |
| **Motors** | TT Gear Motors | — | Rover mobility |
| **Servo Motor** | SG90 | — | Controls medicine drawer |
| **Motor Driver** | L298N | — | Drives motor system |
| **Display** | 16x2 LCD / 3.5" TFT | — | Shows vitals & alerts |
| **Camera** | Raspberry Pi Cam v3 | — | Face & human recognition |
| **Buzzer** | Active Buzzer Module | — | Alerts |
| **Battery** | 18650 Li-ion Pack | — | Power supply |

---

## 🧠 System Architecture
   +--------------------------------------+
   |          CARE COMPANION SYSTEM       |
   +--------------------------------------+
         |       |       |       |
         v       v       v       v
    Sensors   Camera   Voice   Dashboard
         |       |       |       |
         +-------+-------+-------+
                 Raspberry Pi 4
                       |
                  Arduino UNO
                       |
               Biomedical Sensors
                       |
               Web Dashboard + DB


---

## 🧪 Expected Outcomes

✅ Real-time temperature & heart rate monitoring  
✅ Smart reminder and drawer mechanism  
✅ AI-driven detection & mobility  
✅ Alert system for hazards and emergencies  
✅ Centralized dashboard for caregivers  
✅ Prototype ready for real-world application  

---

## 💻 Installation & Usage

```bash
# Clone the repository
git clone https://github.com/Tanjamul-Azad/Silicon-Squad-.git
cd care_companion

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate   # For Linux
venv\Scripts\activate      # For Windows

# Install dependencies
pip install -r requirements.txt

# Run the project
python run_all.py
💡 Ensure Arduino is connected and serial port configured before running.

🧑‍💻 Developed By

👨‍🎓 Team Silicon Squad
Department of Computer Science & Engineering (CSE)
United International University (UIU), Bangladesh

📘 Course: Microprocessors and Microcontrollers Laboratory (CSE 4326)

💻 GitHub: Tanjamul-Azad / Silicon-Squad-


💬 Future Enhancements

😊 Emotion detection (AI model)

☁️ Cloud data storage and analytics

🧭 Advanced mobility with obstacle avoidance

🔔 Smart IoT notification system

🩹 Doctor consultation portal integration

🏁 Conclusion

Care Companion merges AI, IoT, and Embedded Systems to deliver a next-generation healthcare solution.
It ensures constant monitoring, safety, and assistance — bringing smart healthcare to every home.

💚 “Because true care never sleeps.”
