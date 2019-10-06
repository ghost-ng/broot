# How to contribute
The primary way to contribute is to create additional plugins for the broot framework.  The beauty in broot is that you can create your own plugin using the specified template and the framework will seemlessly accept it as a "plug-n-play" style plugin.  In order for this to work, you do need to have specific sections in your plugin, to be discussed in the next sections.

## Plugin Template
You must complete a minimum of 6 sections to effectively work with the broot framework.

**Main parts:**
import broot framework requirements
import plugin requirements
plugin commands
plugin variables
main *run* function

### Section 0 - Default Imports *DO NOT CHANGE*
For normal usage, this section should not change.  It consists of default imports that all plugins need available.  

### Section 1 - Imports
Use this section if you need 3rd party python modules that are not included inthe main python installation.  It is prefered to use as many default modules, however we know that this is sometime unrealisticl; therefore this section allow you to import these pre-requisites as well as auto install any new ones.

To make it a little easier, the lines commented with "#HERE" need to be modified.

**Example:**
*<new_module_here>* --> *requests*

Don't be afraid, this sections requires user input to accept the installation and simply invokes pip to install modules.

### Section 2 - About
This section is completely non-essential, however is needed if you want to create a robust and helpful guide to help users understand when to use your plugin, introduce some version control, and outline contributing authors.

Additionally, the *banner* variable is displayed upon a successful import of all prerequisites which is helpful to give the broot user feedback.

### Section 3 - Plugin Commands
This section contains any additional commands you need to get your plugin to work.  Normally, this section is not needed.  Your commands will become available in the *show commands* output.  The *parse_plugin_cmds* then handles the logic that will parse your new commands.

Critical Elements:
**plugin_cmds**
These commands will automatically be available when you *load* a plugin.  The actions these commands spawn is controlled by the *parse_plugin_cmds* function (below).

This variable MUST retain the dictionary structure in the tempalte example.

**parse_plugin_cmds**
The role of this function is to parse the input commands and dictate subsequent actions.  The framework will default to this function if it see a command found in the *plugin_cmds* dictionary variable.

### Section 4 - Plugin Variables
Use this section to define plugin-specific variables that will help execute or fine-tune your new plugin.  A user can "set" these variables in the main broot framework, but your "run" method will reference these variables to help with your authentication function. The **plugin-vars** variable MUST retain the dictionary structure in the tempalte example. 

## Section 5 - Validate
This section accomplished all your validation steps prior to running the plugin.  You can opt to not fill this section out, but that is highly discouraged.  If a validate options fails here, you should set validated = False.  Also your last statement will be a return statement of 'return validated.'  

If you find yourself needing other functions in the "var" library, you can change the import function to 'import var' but then you'd need to ensure to update your 'global_vars' references to 'var.global_vars.'


### Section 5 - Main
This section MUST be present or the broot framework with throw an error.  The main engine will call the *run* function to execute the plugin.  The broot framework will iterate over the list of usernames, targets, and password and pass each combination to the *run* method.  This method will then run through the authenticaiton logic for your plugin and should return 'True' for a successful authentication attempt and 'False' for a failure.

## Dynamic Refresh
To help with troubleshooting and overall ease of use, as you modify your plugin or add new plugins to the framework, you can execute a "reload plugins" commands to refresh the plugins list.  

## Directory Structure
I recommend you create your plugin seperately, verify it works, then include it into the framework.  This can be achieved with the python if/main commands:
*if __name__ == "__main__":*

Here you can preset all your variables to test that the authentication method works before testing framework integration.
