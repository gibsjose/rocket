# Rocket
Configurable C, C++, and Python skeleton projects with configurable makefiles and git repository initialization.

## Description
`Rocket` generates a new project folder with skeleton code (`.c` or `.cpp` and `.h` for C and C++ projects, and `.py` for Python) with auto-generated header comment blocks, and a simple `main`.

`Rocket` also generates and configures a generic makefile for C and C++ projects.

Finally, `Rocket` can be configured to start a new `git` repository in the project directory, use a generic `.gitignore`, and even create and push to a new GitHub remote repository.

You can also specify your license type for open source projects, such as MIT, GNU GPL, Apache, etc.

## Configuration
Configuration is done through a simple `config.json` file using JSON syntax to define parameters such as the project name, author names and emails, project websites, license type, etc.

## GitHub
`Rocket` uses `hub create` to create the new GitHub repository. It then runs `git push --set-upstream origin master` to make the first push to the master branch of the remote repository.

## Credits
* Generic C and C++ Makefile: [@mbcrawfo](https://github.com/mbcrawfo/GenericMakefile)
* Generic AVR Makefile
* Generic Arduino Makefile: [@sudar](https://github.com/sudar/Arduino-Makefile)
* Generic Python skeleton code
* Generic `.gitignore` files: [@github](https://github.com/github/gitignore)
* MIT License template: [@remy](https://github.com/remy/mit-license)

## License
MIT License: [http://gibsjose.mit-license.org/](http://gibsjose.mit-license.org/)
