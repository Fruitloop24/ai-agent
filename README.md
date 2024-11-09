---

# 🛡️ **AI-Powered System Hardening Agent** 🛡️

### 🚀 **Project Overview**
Welcome to the AI-Powered System Hardening Agent, a powerful tool designed for Linux systems that combines system diagnostics, network monitoring, and AI-driven analysis. This agent runs a suite of checks to provide a detailed snapshot of system health and security. **Note**: Due to its powerful capabilities and requirements for `sudo`, we recommend running this tool only on **virtual machines** until further security improvements are made.

### ⚠️ **Important Notice**
This tool is still under development, with additional features like SSH capabilities, baseline comparisons, and enhanced network monitoring on the way. For now, it is designed solely for **Linux systems**, and running it on other operating systems may result in unexpected behavior. Proceed with caution and follow all setup guidelines to ensure a safe and secure experience.

### 🎯 **Key Features**
- **Comprehensive System Snapshots**: Gathers OS details, CPU usage, memory, disk stats, and network interface information.
- **Patch Status Checks**: Identifies pending updates and patch availability.
- **ARP Table Inspection**: Checks for DNS spoofing indicators.
- **Malware Indicators**: Scans specific directories for suspicious files.
- **Network Performance**: Runs speed tests, traceroute, and ping diagnostics.
- **Firewall Status**: Reports the current state of the system firewall.
- **AI-Driven Analysis**: Uses OpenAI to provide insights and recommendations based on system snapshots.
- **Concurrent Execution**: Uses multithreading for efficient test execution.

### 🛠️ **Setup & Installation**
#### **Pre-requisites**:
- Linux operating system (tested on Ubuntu, Debian, etc.)
- Python 3.x installed
- OpenAI API key for AI analysis

#### **Installation Steps**:
1. **Clone the Repository**:
   ```bash
   git clone git@github.com:Fruitloop24/ai-agent.git
   ```
2. **Set Up a Virtual Environment**:
   - Navigate to the project directory:
     ```bash
     cd ai-agent
     ```
   - Create a virtual environment to avoid global package installation:
     ```bash
     python3 -m venv venv
     ```
   - Activate the virtual environment:
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```
     - On Windows (if applicable for future versions):
       ```bash
       venv\Scripts\activate
       ```
3. **Install Dependencies**:
   - With the virtual environment activated, install the required packages:
     ```bash
     pip install -r requirements.txt
     ```

4. **Configure Environment Variables**:
   - Create a `.env` file and add:
     ```bash
     OPENAI_API_KEY=<your_openai_api_key>
     ```

### 📝 **How to Run**
**Caution**: This tool requires `sudo` permissions for certain checks. Run on a **VM** or test environment until the final security enhancements are complete.

1. Ensure your virtual environment is activated.
2. Run the tool with:
   ```bash
   python sudo.py
   ```

### 🖥️ **Future Enhancements**
- **SSH Capabilities**: Enabling remote diagnostics over SSH to extend the agent's reach.
- **Baseline Comparisons**: A feature for comparing current system states with known good baselines.
- **Network Monitoring**: Enhanced network analysis tools for real-time monitoring.
- **Agent/Manager System**: 
   - **Vision**: A lightweight setup where this tool can be deployed on multiple Linux endpoints. Each agent runs autonomously, gathering data and performing checks, while a central manager interface collects and displays results.
   - **Interface**: A simple web-based user interface accessible via a network port, allowing users to monitor all agents in one place. This approach emphasizes a small footprint and efficient deployment.
   - **Value**: This system would be perfect for organizations looking for an easy-to-deploy, scalable security and monitoring solution.

### 🔐 **Security Considerations**
- This tool is powerful and requires `sudo` for some functions, which can be a potential security risk. Ensure you're running it in a secure, controlled environment, such as a **virtual machine**.
- The `OPENAI_API_KEY` and any other credentials should be stored securely in the `.env` file, which should be excluded from version control.
- The tool collects sensitive system data for analysis, so use responsibly and ensure compliance with your organization's security policies.

### 🛡️ **Why Use This Tool?**
This agent is designed to be small yet powerful, offering a quick, detailed snapshot of your system's health and potential vulnerabilities. Whether you're looking for a standalone tool for system hardening or envisioning an agent/manager framework for network-wide deployment, this project provides immense value with minimal setup.

### 🛠️ **Technical Overview**
**Key Libraries Used**:
- `psutil`: For system resource and hardware stats.
- `platform`: For OS and architecture details.
- `subprocess`: For running system commands (e.g., `arp`, `traceroute`, `ufw`).
- `speedtest`: For network speed tests.
- `dotenv`: For securely loading environment variables.
- `openai`: For integrating AI-driven analysis.

**Current Limitations**:
- **Linux-only**: The tool is not compatible with Windows or macOS.
- **Sudo Required**: Some commands need `sudo` permissions, which will be addressed for better security practices in future updates.

### 🌐 **Project Repository & Demo**
View the project on GitHub: [AI-Agent Repository](https://github.com/Fruitloop24/ai-agent)

**Note**: Direct downloads are not recommended due to the tool’s power and current development stage. Check out the repository and follow the setup instructions to explore the capabilities safely.

### 🖥️ **Explore More**:
For live demonstrations and more details on my projects, visit **[my e-portfolio](https://eportkc.com)**.

---
