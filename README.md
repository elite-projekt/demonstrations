# Demonstrations
[![Latest Release](https://code.fbi.h-da.de/esc-mpse20/demonstrations/-/badges/release.svg)](https://code.fbi.h-da.de/esc-mpse20/demonstrations/-/releases)

Documentation can be found in the Wiki.

## Organization

This repository holds all source and configuration files for the Demonstrations.
Folders:

- `ci` contains utility script run by the gitlab CI
- `native` contains a flask app which runs native on every workstation, it also contains code that is required by the demonstrations.
- `password Demo` contains the flask server including the files for the password demo sites and a docker compose file for the development.
- `phishing_demo` contains the flask server including the files for the phishing websites and prototypes for the native access script including mails. (The actual native access + emails is located in the platform repository)
