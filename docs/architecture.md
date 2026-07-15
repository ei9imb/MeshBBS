# MeshBBS Architecture
Version: 0.1
Status: Draft
Author: Domhnall Mac Aodha & ChatGPT

---

# 1. Vision

MeshBBS is an open-source community information server for Meshtastic networks.

Rather than attempting to replace Meshtastic's messaging system, MeshBBS extends it by providing persistent information, structured services and local community resources while respecting the severe bandwidth limitations of LoRa.

The primary design goal is to maximise usefulness while minimising airtime.

---

# 2. Design Philosophy

Every design decision should follow these principles.

## 2.1 Airtime is precious

Every transmission should justify the airtime it consumes.

If a packet does not provide value, it should not be transmitted.

---

## 2.2 Keep messages small

Menus should fit inside a single Meshtastic packet whenever possible.

Long responses should be paginated rather than transmitted in full.

---

## 2.3 MeshBBS complements Meshtastic

Meshtastic already provides excellent messaging.

MeshBBS provides:

- Persistent information
- Structured information
- Community resources
- Mail storage
- Bulletin boards

It is **not** intended to become a replacement chat platform.

---

## 2.4 Simplicity first

A feature should only be added when it solves a real problem.

The first release should remain intentionally small.

---

## 2.5 Modular architecture

Each component should have a single responsibility.

Future features should be added without rewriting existing code.

---

## 2.6 Configuration over code

Node names, welcome messages, weather sources and other settings should never be hard-coded.

---

## 2.7 The operating system is disposable

The Raspberry Pi operating system should always be recoverable.

GitHub contains the source.

Configuration files are backed up separately.

The SQLite database is backed up independently.

---

# 3. Project Goals

Version 0.1 will provide:

- Bulletins
- Mail
- Maps
- Weather
- User statistics
- Read tracking

Nothing more.

Features such as channels, local services, events and file transfer are intentionally deferred.

---

# 4. System Architecture

```
           Meshtastic Network
                    │
             Heltec V3 Radio
                    │
              USB Serial Link
                    │
          Raspberry Pi Zero
                    │
             MeshBBS Application
                    │
               SQLite Database
```

---

# 5. Menu Structure

```
MeshBBS

1 Bulletins
2 Mail
3 Maps
4 Weather
5 Stats
6 Help

0 Exit
```

Submenus will be defined separately.

---

# 6. Session Management

Every node interacting with MeshBBS has its own session.

The BBS remembers:

- Current menu
- Current page
- Current bulletin
- Current mail item
- Session timeout

Navigation principles:

```
0 = Back

9 = Home

? = Help
```

Session state expires automatically after inactivity.

---

# 7. Read Tracking

MeshBBS tracks what every user has already viewed.

Initially:

- Bulletins

Future versions may extend this to:

- Mail
- Weather alerts
- Announcements

Read tracking should minimise unnecessary retransmissions.

---

# 8. Core Components

The application will eventually consist of modules similar to:

```
main.py

meshtastic_client.py

database.py

session.py

bulletins.py

mail.py

maps.py

weather.py

stats.py

commands.py

logging.py

config.py
```

Each module should have a single responsibility.

---

# 9. Logging

Everything important should be logged.

Examples:

- Startup
- Shutdown
- Incoming packets
- Outgoing packets
- Errors
- User activity
- Administrative actions

Logs should make unattended troubleshooting possible.

---

# 10. Database

SQLite will be used.

Likely entities include:

- Users
- Sessions
- Bulletins
- Mail
- Statistics
- Configuration

The database schema will be documented separately.

---

# 11. Statistics

MeshBBS should collect anonymous operational statistics.

Examples:

- Total users
- Active users today
- Sessions started
- Bulletins read
- Mail sent
- Most frequently used features
- Uptime

Administrative statistics may include additional information.

---

# 12. Development Strategy

Software development is performed before hardware integration.

Current development environment:

- Raspberry Pi Zero
- USB Ethernet Gadget
- SSH
- VS Code Remote SSH
- Git
- GitHub

Hardware integration with the Heltec will occur only after the software is mature.

---

# 13. Roadmap

Phase 1
Architecture

Phase 2
Database

Phase 3
Session Engine

Phase 4
Meshtastic Interface

Phase 5
Bulletins

Phase 6
Mail

Phase 7
Maps

Phase 8
Weather

Phase 9
Statistics

Phase 10
Administration

Phase 11
Hardware Integration

Phase 12
Public Release

---

# 14. Future Features

Potential future additions include:

- Channels directory
- Local services directory
- Community groups
- Events
- Emergency information
- Buy & Sell
- Polls
- Weather stations
- File transfer
- Plugin architecture

These are intentionally excluded from Version 0.1.

---

# 15. Project Statement

MeshBBS is not simply a bulletin board.

It is intended to become a community information server for Meshtastic networks while respecting the unique limitations of LoRa communication.

Every design decision should prioritise:

1. Reliability
2. Simplicity
3. Efficient airtime usage
4. Extensibility
5. Community usefulness