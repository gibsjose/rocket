# Rocket
Configurable C, C++, and Python skeleton projects with configurable makefiles and git repository initialization.

## Description
`Rocket` generates a new project folder with skeleton code (`.c` or `.cpp` and `.h` for C and C++ projects, and `.py` for Python) with auto-generated header comment blocks, and a simple `main`.

`Rocket` also generates and configures a generic makefile for C and C++ projects.

Finally, `Rocket` can be configured to start a new `git` repository in the project directory, generate a `README.md`, use a language-specific `.gitignore`, and even create and push to a new GitHub remote repository.

You can also specify your license type for open source projects, such as MIT, GNU GPL, Apache, etc.

## Installation
Clone with:
```bash
git clone https://github.com/gibsjose/Rocket.git
```

Then install:
```bash
cd Rocket
sudo ./install
```

## Usage
First, create a new project directory and name it something clever, like `Project`:

```bash
cd ~
mkdir "Project"
```

Then hop into the newly created directory and run Rocket:
```bash
cd Project
Rocket -l C++
```

This will create a new C++ project in the `Project` directory, including a `config.json` configuration file. Edit `config.json` with your project's name, your name and email, and any other details, then run:

```bash
Rocket -c
```

And you're done!

To remove project files, run:
```bash
Rocket -r
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

    "git": true,
    "github create": false,
    "github remote": "git@github.com:user/Rocket.git",
    "github user": "user",

    "language": "Python",

    "license": "MIT",

    "project": "Rocket",

    "websites": [
        "https://www.example.com",
        "https://github.com/user/example"
    ]
}
```

The order of attributes does not matter, but `Rocket` will throw strange errors if you mess up the JSON syntax! `Rocket` will automatically order the attributes alphabetically when it generates a configuration file, but you are free to re-order it afterwards and it won't be touched unless you re-generate.

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

For Python, `Rocket` will default to naming the main script, for example, `Rocket.py`, instead of just `Rocket`. If you would like to remove the `.py` extension, add the following attribute to the python `language.json`:
```json
    "extension": false
```

## Git
`Rocket` can create a local (or remote, see below) `git` repository, complete with a language-specific `.gitignore` and a project-specific `README.md`

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
