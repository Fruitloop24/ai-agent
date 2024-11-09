import psutil
import platform
import os
import speedtest
import subprocess
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to gather system stats
def get_system_snapshot():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    snapshot = {
        "system": {
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine()
        },
        "cpu": {
            "usage_percent": cpu_percent,
            "cores": psutil.cpu_count(logical=False),
            "threads": psutil.cpu_count(logical=True)
        },
        "memory": {
            "total": memory.total,
            "available": memory.available,
            "used_percent": memory.percent
        },
        "disk": {
            "total": disk.total,
            "free": disk.free,
            "used_percent": disk.percent
        },
        "network": {
            "interfaces": len(psutil.net_if_addrs())
        }
    }
    
    return snapshot

# Function to check patch status
def check_patch_status():
    try:
        result = subprocess.run(['apt', 'list', '--upgradable'], capture_output=True, text=True)
        if "upgradable" in result.stdout:
            num_patches = result.stdout.count("\n")  # Count how many patches are available
            return f"Patches available: {num_patches} patches pending."
        return "System is fully patched."
    except Exception as e:
        return f"Error checking patch status: {e}"

# Function to check ARP table for DNS spoofing indicators
def check_arp_table():
    try:
        result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
        num_entries = result.stdout.count("\n")
        # Add logic to detect spoofing (in a real scenario, we would compare MAC/IP pairs)
        if "inconsistent" in result.stdout:  # Placeholder for real logic
            return f"Potential DNS spoofing detected across {num_entries} ARP entries."
        return f"No DNS spoofing detected across {num_entries} ARP entries."
    except Exception as e:
        return f"Error checking ARP table: {e}"

# Function to check for suspicious files
def check_malware_indicators():
    try:
        suspicious_files = []
        directories_to_check = ['/tmp', '/var/tmp']
        for directory in directories_to_check:
            result = subprocess.run(['ls', directory], capture_output=True, text=True)
            # Example check for 'suspicious_file' or any anomalies
            if "suspicious_file" in result.stdout:
                suspicious_files.append(f"Suspicious file found in {directory}")
        return " | ".join(suspicious_files) if suspicious_files else f"No suspicious files found across {len(directories_to_check)} directories."
    except Exception as e:
        return f"Error scanning for malware: {e}"

# Function to run the speed test
def run_speedtest():
    st = speedtest.Speedtest()
    download_speed = st.download() / 1e6  # Convert from bits to Mbps
    upload_speed = st.upload() / 1e6  # Convert from bits to Mbps
    return {"download": download_speed, "upload": upload_speed}

# Function to run traceroute
def run_traceroute():
    try:
        result = subprocess.run(['traceroute', 'google.com'], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error running traceroute: {e}"

# Function to run ping test
def run_ping():
    try:
        result = subprocess.run(['ping', '-c', '4', 'google.com'], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error running ping: {e}"

# Function to check firewall status
def check_firewall_status():
    try:
        result = subprocess.run(['sudo', 'ufw', 'status'], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error retrieving firewall status: {e}"

# Parallel execution for tests
def run_tests_in_parallel():
    with ThreadPoolExecutor() as executor:
        future_speedtest = executor.submit(run_speedtest)
        future_traceroute = executor.submit(run_traceroute)
        future_ping = executor.submit(run_ping)
        future_patch_status = executor.submit(check_patch_status)
        future_arp_check = executor.submit(check_arp_table)
        future_malware_check = executor.submit(check_malware_indicators)
        future_firewall = executor.submit(check_firewall_status)
        
        return {
            "speedtest": future_speedtest.result(),
            "traceroute": future_traceroute.result(),
            "ping": future_ping.result(),
            "patch_status": future_patch_status.result(),
            "arp_check": future_arp_check.result(),
            "malware_check": future_malware_check.result(),
            "firewall": future_firewall.result()
        }

# Formatting snapshot and test results for AI prompt
def format_for_prompt(snapshot, tests):
    return f"""
    System Snapshot:
    OS: {snapshot['system']['os']} {snapshot['system']['os_version']} ({snapshot['system']['architecture']})
    CPU: {snapshot['cpu']['usage_percent']}% usage, {snapshot['cpu']['cores']} cores, {snapshot['cpu']['threads']} threads
    Memory: {snapshot['memory']['used_percent']}% used ({snapshot['memory']['available']/1e9:.2f}GB available out of {snapshot['memory']['total']/1e9:.2f}GB)
    Disk: {snapshot['disk']['used_percent']}% used ({snapshot['disk']['free']/1e9:.2f}GB free out of {snapshot['disk']['total']/1e9:.2f}GB)
    Network Interfaces: {snapshot['network']['interfaces']}
    
    Test Results:
    - Patch Status: {tests['patch_status']}
    - ARP Table: {tests['arp_check']}
    - Malware Indicators: {tests['malware_check']}
    - Speed Test: Download {tests['speedtest']['download']} Mbps, Upload {tests['speedtest']['upload']} Mbps
    - Traceroute: {tests['traceroute']}
    - Ping: {tests['ping']}
    - Firewall: {tests['firewall']}
    """

# Analyzing system health using AI
def analyze_system_health(snapshot_string):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a sarcastic network and system security expert. Analyze the following system snapshot for potential security issues."},
                {"role": "user", "content": snapshot_string}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error analyzing system health: {e}"

# Main function to run all tests and print results
def main():
    snapshot = get_system_snapshot()
    test_results = run_tests_in_parallel()
    snapshot_string = format_for_prompt(snapshot, test_results)
    health_analysis = analyze_system_health(snapshot_string)
    
    # Printing all results
    print("\nSYSTEM SNAPSHOT\n" + "="*50)
    print(snapshot_string)
    print("\nAI Health Analysis\n" + "-"*50)
    print(health_analysis)

if __name__ == "__main__":
    main()

