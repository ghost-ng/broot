# BROOT

This is a bruteforcing framework that takes advantage of the "plug-n-play" approach offered by python.  Modular behavior allows this framework to remain static while scaling available plugins or "plugins."

Time to "be root," **broot**

## What is this?

broot is a bruteforce framework.  The structure and wrappers provided here dictate the logic that wraps arounds authentication methods.  That is to say, byom, bring your own plugin.  If you code, simply create a method to authenticate to a service, give it some specific methods, and hit run...broot will do the rest.

## Getting Started

This code is written exclusively for python3 with no plans to port it to python2 or a different language.  

### Prerequisites

The main "broot" framework aims to utilize packages included in the python installation.  The one exception to this is 'Prettytables.'  You have two choices to install that pre-requisite:

#1:
```
pip prettytables
```
#2:
Let the script install dependencies for you.  View the "requires.py" file to understand how this work; essentially it invokes 'pip' for you.  I anticipate 3rd party plugins or plugins having python packages not installed with the default installation of python.  Because of this, I've built a plugin to pre-install these dependencies.  As with all software, use this AT YOUR OWN RISK.  DO NOT GIVE BLIND TRUST TO 3RD PARTY MODULES.  

### The Command Line Interface (CLI)

My intent in writing this framework was to make it user friendly and familiar.  Naturally this pushed me to gravitate to the very familiar metasploit CLI framework.  Inspired by its usability, i have provided a few commands that will let you explore the tool.

To honor RTFM, the variables and commands have their own help entries and their own command tree structure.

```
help
help [variable]
show commands
set
unset
show options
run
```

Many of the commands are accompanied with an alias or two, best way to see this all is to run the ```show commands```

## Built With

* [VSCODE](https://code.visualstudio.com/) - The solarized dark theme is my jam!

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Contributors

* **midnightseer** - *Author*


## License

See the [LICENSE.md](LICENSE.md) file for details


