# CoreApiDocumentation Parser for Bulk Insertion

Python Parser for Bulk Insertion into Database various endpoints, Apis and Properties.  

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

### The Steps to install and set Python Environment in your system to make the following files working fine. ####
1. Install Python for windows by navigating to this link on browser:
    a) https://www.python.org/ftp/python/2.7.14/python-2.7.14.msi  ### Installing Python27 Version under C:\ Directory
2. Changing Environment Variables in your system.
    a) Navigate Control Panel\System and Security\System\Advanced system settings\Environment_variables
    b) Click on New button and set following changes:
        # Variable name: PYTHONPATH
        # Varibale value: C:\Python27;C:\Python27\DLLs;C:\Python27\Lib\lib-tk;C:\Python27\Scripts
    c) Setting EXE PATH to work Python for Terminal(Command Prompt) by using these commands:
        # Just Append this line for Path variable under System variables section  ;C:\Python27;C:\Python27\Scripts;   
        # Note: From the above line we also set our pip execution environment as well.So, just type pip command wherever any folder you are!.   
3. Change your Folder Path with this Path.
    a) C:\< Your folder where project files are situated >\CoreApiDocumentation_Bulk_Insert
    b) Type this command:
        # python get-pip.py in your terminal to install pip 
    c) Now type this command:
        # pip install -r requirements.txt
    d) Now we are fit for to execute our script file by just typing: The Rest it perform by itself.
        # python CoreApi_BulkInsert.py.   


## Built With

* Python
* Lxml
* minidom
* Pydoc (Library for connection to MS sql server)


## Versioning

1.0

## Authors

* **Faisal Shafi** - (https://faisalshafi.github.io)


## License

This project is open source and free to use.

## Acknowledgments

* Django Community

