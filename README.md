# Automated IoT-Based Attendance Tracking

An IoT-based attendance management system proposed to automate attendance recording using **RFID identification**, **ESP32-CAM**, and a **Python Flask web application**. The system is designed to reduce the time and errors associated with manual attendance registers while providing timely, period-wise attendance records for educational institutions.

> **Project status:** This repository is associated with a **minor project proposal (December 2024)** from Tribhuvan University, Institute of Engineering, Purwanchal Campus. The report documents the proposed architecture, workflow, and *expected* outcomes; it does not provide verified deployment results or performance measurements.

## Overview

The proposed system identifies a student through an RFID tag, checks whether the scanned UID is registered, and uses an ESP32-CAM camera for an additional identity-verification step. Once the checks pass, attendance is recorded and made available to authorized teachers or administrators through a web dashboard.

## Planned Features

- **Contactless RFID scanning** using an MFRC522 reader and compatible 13.56 MHz RFID tags.
- **UID-based identification** to associate scanned tags with registered users.
- **Camera-assisted verification** through an ESP32-CAM to help discourage proxy attendance.
- **Period-wise attendance logging**, including student identity, subject, date, time, and class period.
- **Wi-Fi data transfer** between the microcontroller and the backend server.
- **Web dashboard** for viewing and managing attendance records.
- **User authentication** to limit dashboard access to authorized teachers and administrators.
- **Local feedback** through proposed display and buzzer components.

*These are design goals from the project proposal, not claims of completed or validated functionality.*

## Proposed Technology Stack

| Layer | Technologies / Components | Role |
| --- | --- | --- |
| Identification | MFRC522 RFID reader, RFID cards/tags | Read a unique tag identifier (UID) |
| Edge controller | ESP32 / ESP32-CAM | Process device inputs, provide Wi-Fi connectivity, support camera capture |
| Camera | ESP32-CAM (OV2640 sensor) | Additional user-verification input |
| Firmware development | Arduino IDE | Program the ESP32-based hardware |
| Backend | Python, Flask | Receive device data, apply attendance logic, and serve the web application |
| Database | MySQL or SQLite (proposal references both) | Store user mappings and attendance records |
| Frontend | HTML, CSS, JavaScript | Teacher/admin dashboard |
| Authentication | Flask-Login (proposed) | Manage authenticated web sessions |
| Feedback | Display and buzzer (proposed) | Indicate status or unsuccessful verification |

**Database note:** The proposal describes **MySQL** in the software-design section but **SQLite** in the expected-results section. The implemented database, if any, should be confirmed from the code before publishing setup instructions.

## Proposed System Architecture

```text
       Student RFID Card / Tag
                 |
                 v
        MFRC522 RFID Reader
                 |
                 v
          ESP32 / ESP32-CAM
          |       |       |
          |       |       +--> Display / Buzzer
          |       |
          |       +----------> Camera-based verification
          |
          +---- Wi-Fi / HTTP ----> Python Flask Server
                                      |
                                      v
                              Attendance Database
                                      |
                                      v
                             Authenticated Web UI
                              (Teacher / Admin)
```

The architecture diagram is a conceptual summary of the proposal, not a verified wiring or deployment diagram.

## Proposed Attendance Workflow

1. A student presents an RFID card to the MFRC522 reader.
2. The device reads the card's UID and checks whether it is registered.
3. If the UID is invalid, the system displays an error and returns to scanning.
4. If the UID is valid, the camera captures data for an additional identity check.
5. If verification fails, attendance is not recorded and the user receives an invalid/failed-verification message.
6. If verification succeeds, the backend updates the attendance record for the relevant date, time, subject, and period.
7. An authenticated teacher or administrator views the updated record in the dashboard.

> The report proposes camera-based verification but does **not** specify or validate a particular face-recognition algorithm or accuracy level.

## Project Objectives

- Replace repetitive manual attendance entry with RFID-based identification.
- Support timely, period-wise attendance updates.
- Improve ease of access to attendance records for authorized staff.
- Explore additional camera verification to reduce attendance fraud.
- Create a modular foundation for later analytics, notifications, and scaling.

## Expected Outcomes

The proposal anticipates faster attendance recording, real-time updates, authenticated record access, and integration across hardware and web software. **No measured speed, recognition accuracy, fraud-prevention effectiveness, or successful field-deployment statistics are reported in the supplied proposal.**

## Getting Started

The supplied report is a **design proposal**, not a complete installation manual. After the project source code and firmware are added to this repository, this section can be updated with verified instructions for:

1. Wiring the MFRC522 reader and optional feedback components to the selected ESP32 board.
2. Flashing the correct firmware using the Arduino IDE.
3. Configuring Wi-Fi and backend connectivity without committing credentials.
4. Creating the supported database schema and configuring the Flask application.
5. Installing Python dependencies and launching the web dashboard.
6. Registering users and testing the attendance workflow.

**Security:** Store database passwords, Wi-Fi credentials, session secrets, and other sensitive values in configuration files excluded from Git, or in environment variables. Do not commit real student identifiers, face images, or attendance records.

## Limitations and Future Work

- The proposal does not establish the final hardware wiring, database choice, or tested implementation status.
- Camera verification details, privacy controls, and evaluation metrics require further design and validation.
- Future enhancements could include reporting/analytics, notifications, stronger security controls, and broader institutional deployment.

## Project Team

**Tribhuvan University**  
Institute of Engineering, Purwanchal Campus  
Department of Electronics and Computer Engineering  
Dharan, Nepal

- **Mausam Lamichhane** — PUR078BEI019
- **Hitesh Labh** — PUR078BEI013
- **Prayag Kharel** — PUR078BEI025
- **Sugam Subedi** — PUR078BEI042

**Academic project:** Minor Project Proposal, December 2024.

## Documentation

For detailed motivations, proposed components, the system block diagram, the proposed verification flowchart, and expected results, consult the original minor project proposal supplied with the project.

## License

No software license is specified in the report. Check with the project contributors before adding a license or reusing project code beyond its authorized terms.
