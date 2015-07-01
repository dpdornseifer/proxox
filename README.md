PROXOX
=======================

A small tool to make it easy to manage proxy settings and inject it into open terminal sessions as well as making changes directly in configuration files
if the application does not support proxy configuration via command line.

The tool is capable of 
* Using the systemtools 
* Injecting proxy changes into open terminal sessions if there is no process running by sourcing a config file / deleting the environment variable
* Configuring a variable in a application config file via 'sed'
