# Welcome to [RSX's](rsx-utoronto.com) repository for the 2015-2016 URC
The goal is to create a nicely organized repository so we don't have to rewrite the whole codebase every year. 
To help us do this, we need you to keep the repo clean and well organized, by reading this (hopefully short) readme. 

## Basic code organization
The code is divided into three folders, meant to run on three different computers. Please put code where it belongs. 

- The **ground** folder contains files meant to run on the ground station computer. The main script is main.py, which will call other files as necessary. 
- The **obc** folder contains the files meant to run on the onboard computer, i.e. the Raspberry Pi, the master computer on the rover. There will be one script, main.py, running on this computer.
- The **controller** folder contains the files meant to run on the microcontroller, i.e. the Arduino, that interfaces directly with the sensors. There will be one script, controller.ino, running on this computer. 

- The **ground_comm** folders in ground/ and obc/ handle socket communications between the ground station and the onboard computer. 
- The **control_comm** folders in obc/ and controller/ handle serial communications on the rover between the onboard computer and the microcontroller.
- Each folder should have a test folder for scripts that test the code. 


## Code guidelines
1. Comment your code, and use commit messages. I don't think this needs explanation. 
2. Test your code before committing, and put the scripts for testing in the test folder for the system you're testing. The script should include what it's testing. 
3. If you make large-scale changes to the organization, please consult at least one of the designers: Michael, Jay or Christopher before doing so, so we can explain why we did it the way we did

## Using git from command line
On Windows: [Download the git shell] (https://desktop.github.com)

On Linux: It should be included by default

Navigate to where the repo is stored (e.g. cd C:/Users/user/Documents/galaxy2)

To set up the repository on your computer: 
```
$ git clone https://github.com/rsx-utoronto/galaxy2.git
```

To commit changes (after testing!):
```
$ git add *
$ git commit -m "Look, I can commit my code!"
$ git push
```

To pull changes (update the version on your computer to the latest):
```
$ git pull
```