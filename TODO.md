# Rocket To-Do List

* Add `Rocket --makefile [LANGUAGE]` flag to just generate and configure a makefile for the language, in an already existing project
* Need separate `makefile.json` config file for the makefile portion?
* Add more configuration options to `config.json`:
    * `"git": true/false`
    * `"github": username`
    * `"travis-ci": username`
* Add ability to init `git` local repo and push to remote GitHub repo
* Add ability to use non-GitHub repo with `"git-remote": "url"`
* Have separate `git.json` config file?
* Add `blinky` examples in C and C++ for AVR microcontrollers
* Add `arduino` as 'language', with makefile, gitignore, and example (blinky from Arduino IDE)
* For AVR microcontroller and Arduino makefiles, print message to screen after configuration to run `export PORT=...` and `export PROGRAMMER=...` for `avrdude` 
