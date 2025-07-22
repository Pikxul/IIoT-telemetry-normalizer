# IIoT Telemetry Normalizer

This project was developed as part of the **Deloitte Australia Job Simulation** on [Forage](https://www.theforage.com/), simulating a real-world industrial client scenario for **Daikibo Industrials**, a global manufacturer of heavy machinery.

## 🛠️ Objective

To normalize telemetry data from industrial IoT devices streaming in two distinct formats into a **unified schema**, making it suitable for real-time monitoring in a manufacturing dashboard.

## 📦 Features

- Converts two disparate data formats into a unified structure
- Handles timestamp normalization (ISO → Unix milliseconds)
- Converts flat string locations into structured objects
- Implements clean error handling and logging
- Includes unit tests for both data types
- Optimized for performance and readability

## 🧪 Tech Stack

- **Language:** Python 3  
- **Libraries:** `json`, `datetime`, `unittest`, `logging`  
- **Platform:** [Replit](https://replit.com/)

## ✅ How It Works

- `convert_from_format_1`: Parses devices with string-based location and Unix timestamps
- `convert_from_format_2`: Handles structured location fields and ISO timestamps
- `normalize_payload`: Detects and routes input data to the correct handler
- `TestPayloadNormalization`: Unit tests ensure conversions are valid against expected results

## 📂 File Structure
├── data-1.json # Format 1 sample input
├── data-2.json # Format 2 sample input
├── data-result.json # Target unified format
├── main.py # Core logic + tests
