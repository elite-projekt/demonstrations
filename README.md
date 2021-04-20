# Demonstrations

Documentation can be found in the group [wiki](https://code.fbi.h-da.de/groups/esc-mpse20/-/wikis/home)

# Organization

This repository holds all source and configuration files for the Demonstrations.
Folders:
- `Demo Navigation` contains the demo navigation (currently only for the Phishing Demo, but can be extended for future demos)
- `Phishing Demo` contains the flask server including the files for the phishing websites and prototypes for the native access script including mails. (The actual native access + emails is located in the platform repository)
- `ci` contains utility script run by the gitlab CI
- `native` contains a flask app which runs native on every workstation, it also contains code that is required by the demonstrations.

