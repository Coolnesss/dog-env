# Gym environment for Freenove Robot Dog Kit

Work in progress!

This package allows running of reinforcement learning algorithms on the real robot dog, over wifi. RL code will run on your PC, while the commands and sensor data will be sent and recieved over WIFI.

### Setup

1. Build the dog according to the tutorial by Freenove found [here](https://github.com/Freenove/Freenove_Robot_Dog_Kit_for_Raspberry_Pi/blob/master/Tutorial.pdf)
2. Run the server on the Raspberry Pi according to the same tutorial 
3. Calibrate the dog using the calibration paper that came with the dog and the GUI client supplied by Freenove. This allows the motion primitives to be used.
4. Specify a reward function
5. Use an RL library / own code with the gym environment to learn a policy