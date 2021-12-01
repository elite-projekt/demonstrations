# Demonstrations

Documentation can be found in the Wiki.

## Organization

This repository holds all source and configuration files for the Demonstrations.
Folders:

- `ci` contains utility script run by the gitlab CI
- `demo_navigation` contains the demo navigation (currently only for the Phishing Demo, but can be extended for future demos)
- `native` contains a flask app which runs native on every workstation, it also contains code that is required by the demonstrations.
- `password Demo` contains the flask server including the files for the password demo sites and a docker compose file for the development.
- `phishing_demo` contains the flask server including the files for the phishing websites and prototypes for the native access script including mails. (The actual native access + emails is located in the platform repository)
