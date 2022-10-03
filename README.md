# Binomica labs Opentron protocols

Collection of python protocols for Opentrons API.

For usage I recommend pipenv:

```bash
pip3 install pipenv

#cd to a working directory i.e. cd ~/python/opentrons_scripts
#using pipenv to install a module will create a local environment specific to the directory
pipenv install opentrons

#activate the pipenv shell in the same directory to access the installed module
pipenv shell

#you can check for proper installation of opentrons API or any other pip module within your working directory via:
pip3 show opentrons

```

Current protocols are written for an Opentrons V2 (not OT-2R) using p300_single (not v2 revision).

Most protocols are optimized for saving tips and utilizing off-the-shelf containers and wells when possible. I'd recommend running a protocol calibration and doing a dry run for these scripts. 


