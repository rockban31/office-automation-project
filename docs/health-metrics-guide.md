# Client Health Metrics Analysis Guide (STEP 4)

## Overview

STEP 4 of the wireless troubleshooter performs comprehensive analysis of client connection quality by examining multiple wireless performance indicators. This guide explains what each metric means and how to interpret the results.

---

## 📊 Health Metrics Explained

### 1️⃣ **RSSI (Received Signal Strength Indicator)**

**What it measures:** Signal power from Access Point to client device

**Unit:** dBm (decibel-milliwatts) - a logarithmic scale where higher = better

**Thresholds:**
| RSSI Range | Status | Description | Impact |
|------------|--------|-------------|--------|
| > -67 dBm | ✅ Excellent | Strong signal | Optimal performance, maximum speeds |
| -67 to -70 dBm | ✅ Good | Acceptable signal | Normal operation |
| -70 to -80 dBm | ⚠️ Fair | Weak signal | Reduced speeds, possible drops |
| < -80 dBm | 🔴 Poor | Very weak | Frequent disconnects, very slow |

**Real-world analogy:** Like "signal bars" on your phone, but with precise numbers

**Common causes of poor RSSI:**
- Too far from Access Point
- Physical obstructions (walls, metal, concrete)
- Client device has weak antenna
- AP power settings too low

**Recommendations if poor:**
- Move closer to AP
- Check for obstructions
- Add additional APs for better coverage
- Verify AP transmit power settings

---

### 2️⃣ **SNR (Signal-to-Noise Ratio)**

**What it measures:** Quality of signal relative to background RF noise

**Unit:** dB (decibels) - higher = cleaner signal

**Thresholds:**
| SNR Range | Status | Description | Impact |
|-----------|--------|-------------|--------|
| > 25 dB | ✅ Excellent | Very clean signal | Optimal data rates, no errors |
| 20-25 dB | ✅ Good | Clean signal | Good performance |
| 15-20 dB | ⚠️ Fair | Some noise | Performance affected |
| < 15 dB | 🔴 Poor | High noise | Significant interference |

**Real-world analogy:** Like trying to hear someone speak in a noisy room - high SNR = clear conversation

**Common causes of poor SNR:**
- RF interference (microwaves, Bluetooth, other Wi-Fi)
- Channel congestion (too many APs on same channel)
- Non-Wi-Fi interference (baby monitors, wireless cameras)
- Poor quality client adapter

**Recommendations if poor:**
- Change Wi-Fi channel
- Identify and remove interference sources
- Use 5 GHz instead of 2.4 GHz (less crowded)
- Check for neighboring APs on same channel

---

### 3️⃣ **Retry Rates (TX/RX)**

**What it measures:** Percentage of packets that need to be retransmitted

**Components:**
- **TX Retries:** Packets sent from client that needed resending
- **RX Retries:** Packets sent from AP that client had to request again

**Calculation:** `(Retries / Total Packets) × 100`

**Thresholds:**
| Retry Rate | Status | Description | Impact |
|------------|--------|-------------|--------|
| < 5% | ✅ Excellent | Very low errors | Optimal efficiency |
| 5-10% | ✅ Good | Normal errors | Good performance |
| 10-20% | ⚠️ Fair | Elevated errors | Reduced throughput |
| > 20% | 🔴 Poor | High errors | Significant degradation |

**Real-world analogy:** Like having to repeat yourself in a conversation - high retries = lots of repetition needed

**Common causes of high retries:**
- Poor signal quality (low RSSI)
- RF interference (low SNR)
- Channel congestion
- Defective client wireless adapter
- Corrupted packets

**Recommendations if high:**
- Check RSSI and SNR first
- Verify channel utilization
- Test with different device to rule out client issue
- Check for packet corruption

---

### 4️⃣ **Latency** (if available)

**What it measures:** Round-trip time for packets to travel client ↔ AP ↔ destination

**Unit:** milliseconds (ms)

**Thresholds:**
| Latency | Status | Use Case | Impact |
|---------|--------|----------|--------|
| < 20 ms | ✅ Excellent | Gaming, VoIP | Real-time apps work perfectly |
| 20-50 ms | ✅ Good | General use | No noticeable lag |
| 50-100 ms | ⚠️ Fair | Web browsing | Slight delay |
| > 100 ms | 🔴 Poor | Limited use | Noticeable lag |

**Real-world analogy:** The "lag" you feel in video calls or online games

---

## 📈 Additional Metrics Collected

### **Data Rates (Link Speed)**
- **TX Rate:** Maximum speed client → AP (Mbps)
- **RX Rate:** Maximum speed AP → client (Mbps)
- These are **potential** speeds, not actual usage

### **Throughput (Actual Usage)**
- **TX Throughput:** Current data being sent (Kbps/Mbps)
- **RX Throughput:** Current data being received (Kbps/Mbps)
- Shows **real-time** bandwidth usage

### **Connection Details**
- **Band:** 2.4 GHz or 5 GHz
- **Channel:** Specific radio channel
- **Protocol:** 802.11 standard (ac, ax, etc.)
- **SSID:** Network name
- **VLAN:** Network segmentation
- **Security:** Encryption method (WPA2, WPA3)
- **Uptime:** How long connected

---

## 🔄 What Happens After STEP 4?

### **If NO Health Issues Detected:**
✅ Troubleshooter marks client as healthy and proceeds to STEP 5 (All checks passed)

### **If Health Issues ARE Detected:**
The troubleshooter proceeds with deeper analysis:

#### **STEP 4a: Client Connectivity & Reachability Tests**
- Ping tests to client IP
- Packet loss measurement
- Latency measurement
- Disconnection frequency analysis

**What it checks:**
```
• Can we reach the client?
• Is packet loss acceptable (<5%)?
• Is ping latency reasonable (<100ms)?
• Is the client disconnecting frequently?
```

#### **STEP 4b: AP Uptime Analysis**
- Checks how long AP has been running
- Identifies if AP needs reboot

**What it checks:**
```
• Has AP been up > 30 days? (may need scheduled reboot)
• Has AP been up < 1 hour? (recent restart - stability issue?)
```

#### **STEP 4c: AP Hardware Status**
- CPU utilization
- Memory usage
- Temperature monitoring

**What it checks:**
```
• Is AP CPU overloaded (>80%)?
• Is AP memory exhausted (>85%)?
• Is AP overheating (>70°C)?
```

#### **STEP 4d: RF Environment Analysis**
- Channel utilization on 2.4/5 GHz
- Noise floor levels
- Co-channel interference (multiple APs on same channel)

**What it checks:**
```
• Is the channel congested (>70% utilization)?
• Is RF noise high (> -85 dBm)?
• Are too many APs using the same channel?
```

---

## 🎯 Real Example from Your Network

Here's an actual analysis from your network:

```
📍 Client: iPhone
   Site: Phoenix
   MAC: 2a:fa:2e:8c:b8:0f
   IP: 10.21.5.242
   Connected to AP: ac:23:16:0e:5a:74

1️⃣ RSSI: -45 dBm
   Status: ✅ EXCELLENT - Strong signal
   Impact: Optimal performance, no concerns

2️⃣ SNR: 49 dB
   Status: ✅ EXCELLENT - Very clean signal
   Impact: Optimal data rates, minimal errors

3️⃣ Retry Rates:
   TX: 2.87% (1,226 retries / 42,668 packets)
   RX: 0.98% (64 retries / 6,540 packets)
   Status: ✅ EXCELLENT - Very low retry rate

4️⃣ Data Rates:
   TX: 516.1 Mbps (Client → AP)
   RX: 24.0 Mbps (AP → Client)

5️⃣ Connection Details:
   Band: 5 GHz
   Channel: 52
   Protocol: AX (Wi-Fi 6)
   SSID: COLLEAGUE
   Security: WPA2-EAP-FT/CCMP
   Uptime: 0.6 hours

Result: ✅ All health metrics within normal ranges!
```

---

## 🔍 How to Test

Run the demonstration script:

```bash
python examples/health_metrics_demo.py
```

Or run full troubleshooting:

```bash
python office_automation_cli.py wireless troubleshoot --client-mac <MAC> --client-ip <IP>
```

---

## 📚 Industry Standards

The thresholds used in this analysis are based on:
- **Cisco Wireless LAN Controller Standards**
- **IEEE 802.11 Specifications**
- **Industry Best Practices** (CWNA, CWAP certifications)
- **Real-world deployment experience**

### Key Thresholds Summary:
- **RSSI:** < -70 dBm triggers warning
- **SNR:** < 15 dB triggers warning  
- **Retry Rate:** > 10% triggers warning
- **Latency:** > 100 ms triggers warning

---

## 💡 Pro Tips

1. **RSSI + SNR Together:** Both must be good. Good RSSI with poor SNR = interference problem

2. **5 GHz vs 2.4 GHz:** 5 GHz has shorter range but less interference

3. **Retry Rates:** Often the first indicator of RF problems

4. **Monitor Trends:** Single snapshot is useful, but trending over time is better

5. **Compare Multiple Clients:** If all clients have issues, it's the AP. If one client has issues, it's the client device

---

**Last Updated:** 2025-10-20  
**Version:** 1.0
