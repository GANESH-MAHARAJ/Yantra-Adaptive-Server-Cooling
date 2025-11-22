# Adaptive Server Cooling using Agentic AI

A next-generation AI-driven thermal management system designed to optimize power consumption and cooling efficiency in server rooms and data centers. This project combines IoT sensing, agentic AI decision-making, predictive thermal control, and microcontroller-based actuation to deliver smart, zone-based cooling automation.

---

## 🚀 Overview

Traditional data center cooling relies on fixed-speed fans or rigid cooling configurations that waste energy and fail to adapt to dynamic heat loads. This system introduces **adaptive, AI-powered cooling** capable of:

- Adjusting cooling intensity in real time  
- Reducing energy consumption  
- Preventing local overheating  
- Improving server reliability  
- Scaling across multiple cooling zones  

According to the patent disclosure (IDF-B) :contentReference[oaicite:1]{index=1}, existing methods lack zone-based control, historical analysis, and real-time AI decision-making. This system fills those gaps.

---

## 🎯 Key Features

### **🔹 1. Real-Time Sensor Monitoring**
- Temperature & humidity sensors (DHT11/DHT22)
- Multi-zone sensing across “data cubes”
- Continuous data streaming to MongoDB for real-time + historical analysis

### **🔹 2. Agentic AI Decision Engine (LangFlow)**
- AI processes sensor data to determine optimal fan speeds and humidity control  
- Predictive cooling using historical trends  
- Energy-aware decision policies  
- Fully modular—switch between online/offline LLMs without circuit changes  

### **🔹 3. Zone-Based Cooling Control**
- Each zone receives independent cooling instructions  
- Prevents overcooling/undercooling in different server racks  
- Example control signal:  
  `1 100` → *Zone 1 → Fan 100%*

### **🔹 4. Microcontroller-Based Actuation**
- Arduino Nano handles fan & humidity actuator control  
- L298N motor driver adjusts cooling fans dynamically  
- Low-latency serial communication between AI → Arduino  

### **🔹 5. Energy Efficiency**
- Reduces unnecessary power draw by adjusting cooling only where needed  
- Supports sustainability goals through smarter thermal management  

---

## 🧠 System Architecture

### **📡 1. Sensor Layer**
- DHT11/DHT22 sensors  
- Infrared sensors for airflow/overheat detection  

### **🗄 2. Data Layer**
- MongoDB database stores real-time & historical data  
- Enables pattern learning and predictive cooling  

### **🤖 3. AI Processing Layer**
- LangFlow-based agentic AI  
- Predictive temperature modelling  
- Multi-zone decision logic  
- Real-time optimization loop  

### **⚙️ 4. Actuation Layer**
- Arduino Nano  
- L298N motor driver  
- DC Cooling Fans  
- AC–DC Hi-Link power module  

### **📊 5. Dashboard**
- Admin interface for viewing:
  - Sensor values  
  - Cooling actions  
  - Temperature trends  
  - Real-time zone performance  

---

## 🔌 Circuit Diagram

The circuit (shown in the patent disclosure, Page 3–4) :contentReference[oaicite:2]{index=2} includes:

- Arduino Nano as central controller  
- DHT sensors for thermal-humidity sensing  
- L298N motor driver for DC fan control  
- IR sensors for airflow detection  
- AC–DC converter for power regulation  


---

## 🧪 Experimental Validation

Early prototype tests (IDF-B Section 8) :contentReference[oaicite:3]{index=3} show:

- System correctly adjusts fan speeds based on varying sensor values  
- AI agent responds instantly to thermal fluctuation inputs  
- Validates feasibility of predictive thermal regulation  
- Next phase focuses on energy savings & full-scale deployment  

---

## 🔬 Novelty & Innovation

This invention introduces:  
- **AI-Based Predictive Cooling**  
- **Multi-Zone Dynamic Thermal Management**  
- **Hardware–Software Agentic Integration**  
- **Modular Cooling Architecture**  
- **Real-Time Microcontroller Actuation from AI Decisions**  

These innovations make the system patentable and practically deployable in server rooms and industrial environments.

---

## ⚙️ Tech Stack

### **Hardware**
- Arduino Nano  
- DHT11/DHT22 sensors  
- IR sensors  
- L298N Motor Driver  
- DC Cooling Fans  

### **Software & AI**
- Python  
- LangFlow AI agent  
- MongoDB  
- Serial communication  
- Predictive logic models  

---

## 📦 Installation & Setup

### **1️⃣ Clone the repository**

git clone https://github.com/GANESH-MAHARAJ/Yantra-Adaptive-Server-Cooling
cd Yantra-Adaptive-Server-Cooling

### **2️⃣ Install backend dependencies**

pip install -r requirements.txt

### **3️⃣ Start the AI Agent (LangFlow / LangChain backend)**
python ai_agent_server.py

### 4️⃣ Start the Python–Arduino bridge
python serial_controller.py

### 5️⃣ Power on the Arduino circuit
Connect sensors + driver + fans
Ensure correct COM port configuration


🧑‍💻 Author

Ganesh Maharaj Kamatham

B.Tech CSE (Data Science), VIT Vellore

Email: ganeshmaharaj.kamatham@email.com

📜 License

This project is part of a filed invention and is not licensed for commercial use without permission.





