MeshBBS

MeshBBS is a Bulletin Board System (BBS) designed specifically for the Meshtastic network. It allows Meshtastic users to exchange messages, post bulletins, and access community information using a familiar text-based interface while running continuously on low-power hardware.

Features

* Bulletin board system for Meshtastic networks
* Local mail between Meshtastic users
* Persistent SQLite database
* Menu-driven command-line interface optimised for Meshtastic messaging
* User and session management
* Read tracking for messages and bulletins
* Comprehensive logging and configuration
* Designed to run continuously on low-power devices such as the Raspberry Pi Zero

Project Goals

* Provide a reliable community BBS over Meshtastic.
* Store bulletins and mail locally.
* Minimise radio traffic while providing a responsive user experience.
* Operate unattended 24/7 on inexpensive, low-power hardware.
* Maintain a modular, well-tested, and maintainable codebase.

Current Status

Version: 0.2.1

Completed

* Project architecture
* Logging framework
* Configuration management
* Application lifecycle
* SQLite database layer
* Domain models
* Bulletin service
* Menu and command router
* Interactive command-line interface
* User sessions
* Automated unit tests

In Progress

* Raspberry Pi deployment
* Meshtastic interface integration
* End-to-end testing with Heltec hardware
* Automatic service startup and recovery

Development Workflow

Each development sprint follows the same process:

1. Plan
2. Build
3. Test
4. Fix
5. Commit
6. Push

The application is expected to remain in a runnable and testable state after every sprint.

Planned Features

* Personal mail
* Public bulletins
* User statistics
* Local services directory
* Weather information
* Node directory
* File transfer
* System administration tools

Hardware

MeshBBS is designed to run on modest hardware, including:

* Raspberry Pi Zero
* Raspberry Pi Zero 2 W
* Raspberry Pi 3 and newer
* Meshtastic-compatible LoRa devices (tested with the Heltec V3)

License

This project is licensed under the MIT License. See the LICENSE file for details.