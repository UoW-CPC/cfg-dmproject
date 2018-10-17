# dmproject

This project is a test application that mimic as the Digital Marketplace component of CFG. The application demonstrates the integration of CFGUM using Python based Django framework. 

Please use the following steps in order to setup and configure this project on your local machines:

1. Download the project,
2. Create a virtual enviornment, using the following command, inside the project directory,

    	virtualenv <vir_env_name>   # Let's say dmprojectenv
3. From the project directory, activate the virtual enviornment using the following command,

		source dmprojectenv/bin/activate
4. Run the following command to install project dependencies. The [requirements.txt](requirements.txt) file contains list of dependencies,

		pip3 install -r requirement.txt 
5. deactivate the virtual enviornment using the following command,

		deactivate
6. Provide values of different settings in the provided [dmconfig.json](dmconfig.json) file,

7. Apache settings:
    * Install mod_auth_openidc and mod_wsgi modules.
    * Configure Apache virtual host using the provided [vhost_conf](vhost_conf) file.
    * restart apache after making the above changes.