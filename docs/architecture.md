# MeshBBS Architecture

## Overview

MeshBBS is a lightweight Bulletin Board System designed to operate over the Meshtastic network.

The application is intended to run continuously on low-power hardware such as a Raspberry Pi Zero while remaining easy to develop and test on a desktop computer.

Development follows an incremental sprint workflow. The application must remain runnable after every sprint.

---

# High-Level Architecture

```
MeshBBS
│
├── Config
├── Logger
└── Components
    ├── Database
    ├── Meshtastic (planned)
    ├── Bulletin Service (planned)
    ├── Mail Service (planned)
    ├── Weather Service (planned)
    └── Statistics Service (planned)
```

Only components participate in the application lifecycle.

Services such as configuration and logging are always available and are not lifecycle-managed.

---

# Project Structure

```
bbs/
    application.py
    component.py
    config.py
    constants.py
    database.py
    logger.py
    main.py
    models.py
    repositories/
        users.py

config/
data/
docs/
logs/
scripts/
tests/
```

---

# Components

A component is responsible for a subsystem that requires startup and shutdown.

Every component implements:

- start()
- stop()

Current components:

- Database

---

# Models

Models represent domain objects.

Models contain data only.

Current models:

- User

Models do not contain SQL.

---

# Repositories

Repositories are responsible for database access.

Each repository owns one area of the schema.

Current repositories:

- UserRepository

Future repositories:

- BulletinRepository
- MailRepository
- SettingsRepository

Repositories do not know about the application.

Repositories only depend on a database connection.

---

# Database

SQLite is the current storage engine.

The Database component is responsible for:

- Opening the database
- Initialising the schema
- Managing schema versions
- Providing repository instances

Business logic must never execute SQL directly.

---

# Logging

All production logging should use the MeshBBS logger.

The use of print() is permitted only for temporary debugging.

---

# Testing

Every new subsystem should have automated tests.

Tests should never use the production database.

A dedicated test database should be used.

---

# Development Workflow

Every sprint follows the same process:

1. Plan
2. Build
3. Compile
4. Run
5. Test
6. Commit
7. Push

The application should remain runnable after every sprint.

---

# Current Status

Completed

- Project framework
- Configuration
- Logging
- Database component
- User model
- User repository

In Progress

- Repository integration

Next

- Bulletin repository
- Mail repository
- Meshtastic interface