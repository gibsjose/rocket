# Rocket
Configurable C, C++, and Python base project generator

## Description
`rocket` generates a new project folder with skeleton code, auto-generated header comment blocks, and a simple `main`.

Creating and running a fully functional C++ project is as simple as:
```bash
rocket create "Awesome New Project" C++
cd "Awesome New Project/"
rocket config
make
./AwesomeNewProject
```

Hate the skeleton code included? No problem – just modify the templates or drop your own files into the global `Rocket/languages/...` directory!

Hate other template/style choices? Again, just edit the language config files ('language.js') or roll your own!

## Features
* Generates directory structure and skeleton code
* Generates robust makefiles for C and C++ projects
* Automatically fills comment headers with project, author, date, etc.
* Automatically names files based on language standards (CamelCase, underscore_names, dash-names, etc.)
* Automatically configures a `makefile` for C and C++ projects
* Can `init` a new `git` repository and create `README.md` and language-specific `.gitignore` files
* Can automatically `add`, `commit`, and `push` to the remote repository
* Project settings configurable with local `config.json` file
* Global language settings configurable with global `language.json` files
* All code file templates are fully configurable

### Future Features
* Support for AVR microcontroller projects in C and C++
* Support for Arduino projects in C and C++ (with templates like Blinky, USART, etc.)
* Support for both Python 3 and Python 2 (currently supports only Python 3)
* Option to only generate makefile for an existing project (non-configurable)
* Support for Travis-CI
* License templates
* ~~Can create a GitHub repo and automatically push to it (requires [`hub`](https://github.com/github/hub) installed and configured)~~ (Investigating the necessity of this feature...)

## Installation
Clone with:
```bash
git clone https://github.com/gibsjose/rocket.git
```

Then just move the `rocket` folder to your desired location (`~/bin/` or `/usr/local/bin/`, perhaps?) and add the `rocket/bin` directory to your `PATH`.

## Usage
The most basic usage is as follows:
```bash
rocket create 'Clever Name' Python
cd 'Clever Name'
# Edit the generated 'config.json' file
rocket config
```

> NOTE: Unless you are currently inside an **empty** directory called 'Clever Name', in the above example, `rocket` will create a new directory to house your project.

To remove project files, run:
```bash
rocket clean
```

## Project Configuration
Configuration is done through a simple `config.json` file using JSON syntax to define parameters such as the project name, author names and emails, project websites, license type, etc.

The following simple `config.json` file shows all **required** options:
```json
{
    "project": "Rocket",

    "language": "Python",

    "authors": [
        {"name": "John Engineer", "email": "john@engineer.com"}
    ]
}
```

The following file shows all **possible** options:
```json
{
    "authors": [
        {"name": "John Engineer", "email": "john@engineer.com"},
        {"name": "Joe Scientist", "email": "joe@scientist.com"}
    ],
    "description": "Some sweet new project!",
    "git": true,
    "git-push": false,
    "git-remote": "git@github.com:user/repo.git",
    "language": "Python",
    "license": "MIT",
    "license-url": "https://user.mit-license.org",
    "project": "Rocket",
    "websites": [
        "https://www.example.com",
        "https://github.com/user/example"
    ]
}
```

The order of attributes does not matter, but `rocket` will throw strange errors if you mess up the JSON syntax! `rocket` will automatically order the attributes alphabetically when it generates a configuration file, but you are free to re-order it afterwards and it won't be touched unless you re-generate.

## Global Language Configuration
Languages can be configured both by editing the skeleton templates in `skeleton/*` and by editing each language's `language.json` file.

### Skeleton Code
When modifying the skeleton code for a language, keep in mind that you **must** use the exact same comment **tags**. For example, you can modify the way the comment blocks appear, where they are placed, and even remove tags you do not want, but for the tags you would like to keep, you must keep their names the same.

For example, changing the `{TITLE}` tag to `{PROJECT}` will result in the text `{PROJECT}` in your comment blocks. It will not be replaced with the project name, because the tag name was modified.

### Language Configuration File: `language.json`
Each language contains a configuration file named `language.json` which contains information about the language's desired file naming conventions, source file suffixes, and other information.

A complete `language.json` file for C might look like this:
```json
{
    "language": "c",
    "naming": "dashes",
    "sources": [
        ".c"
        ".h"
    ]
}
```

The options for `naming` are as follows:
* `dashes`: Will convert `Rocket Project` to `rocket-project`
* `underscores`: Will convert `Rocket Project` to `rocket_project`
* `camel-case`: Will convert `Rocket Project` to `RocketProject`

**No** attributes in the `language.json` file are required, and indeed the existence of the file itself is optional.

If a naming convention cannot be found in the language configuration, the following defaults will be used:
* C: `dashes`
* C++: `camel-case`
* Python: `underscores`

For Python, `rocket` will default to naming the main script, for example, `Rocket.py`, instead of just `rocket`. If you would like to remove the `.py` extension, add the following attribute to the python `language.json`:
```json
    "extension": false
```

## Git
`rocket` can create a local (or remote, see below) `git` repository, complete with a language-specific `.gitignore` and a project-specific `README.md`.

If you supply a `git-remote` in `config.json`, it will also set up that remote to push to, assuming it is a valid remote.

Finally, if you supply a valid `git-remote` and set `git-push` to `true`, `rocket` will automatically add, commit, and push your initial commit with the base project files.

## Credits
* Generic C and C++ Makefile: [@mbcrawfo](https://github.com/mbcrawfo/GenericMakefile)
* Generic Arduino Makefile: [@sudar](https://github.com/sudar/Arduino-Makefile)
* Generic `.gitignore` files: [@github](https://github.com/github/gitignore)
* MIT License template: [@remy](https://github.com/remy/mit-license)

## License
MIT License: [http://gibsjose.mit-license.org/](http://gibsjose.mit-license.org/)
