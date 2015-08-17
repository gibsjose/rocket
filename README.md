# Rocket
Configurable C, C++, and Python skeleton projects with configurable makefiles and git repository initialization.

## Description
`Rocket` generates a new project folder with skeleton code (`.c` or `.cpp` and `.h` for C and C++ projects, and `.py` for Python) with auto-generated header comment blocks, and a simple `main`.

`Rocket` also generates and configures a generic makefile for C and C++ projects.

Finally, `Rocket` can be configured to start a new `git` repository in the project directory, use a generic `.gitignore`, and even create and push to a new GitHub remote repository.

## Configuration
Configuration is done through a simple `config.json` file using JSON syntax to define parameters such as the project name, author names and emails, project websites, etc.

## Credits
* Generic C and C++ Makefile
* Generic AVR Makefile
* Generic Python skeleton code
