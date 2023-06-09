import numpy as np
import gymnasium as gym
from gymnasium import spaces
from client import Client
import time

class DogEnv(gym.Env):

    def __init__(self, dog_ip: str, action_time=0.01, move_speed=8):
        self.action_time = action_time # Time to continue every action for (in s)
        self.dog_ip = dog_ip # (local) IP address of dog
        self.move_speed = move_speed # How fast the dog walks

        self.observation_space = spaces.Dict(
            {
                "distance": spaces.Box(0, 1000, shape=(1,), dtype=int), # Not really accurate up to 10 meters probably
                "image": spaces.Box(0, 255, shape=(300, 400, 3), dtype=np.uint8),
            }
        )

        self.client = Client(ip=dog_ip, move_speed=self.move_speed)
        self.client.turn_on_client()

        self.action_map = [
            self.client.forward,
            #self.client.backward,
            #self.client.turn_left,
            #self.client.turn_right,
            #self.client.step_left,
            #self.client.step_right,
        ]

        self.action_space = spaces.Discrete(len(self.action_map))


    # Dog begins in relax mode
    def reset(self):
        self.client.relax()
        image = self.client.get_image()
        distance = self.client.get_distance()

        return {
            "image": image,
            "distance": distance
        }

    def step(self, action):
        # Map int to action function
        action_command = self.action_map[action]
        
        # Execute action
        action_command()

        # The previous action will be executed for this amount of time
        # plus the time it takes to get the image and distance
        time.sleep(self.action_time)

        # Observe next state
        observation = {
            "image": self.client.get_image(),
            "distance": self.client.get_distance()
        }
        
        # Compute reward based on state
        reward = 0 # TODO 

        return observation, reward, False, False, {}

# Basic usage
# WARNING! Be very careful when executing arbitrary commands on a real robot
if __name__ == '__main__':
    env = DogEnv(dog_ip="192.168.86.68")
    obs = env.reset()
    print(obs["distance"])
    
    import matplotlib.pyplot as plt
    #plt.imshow(obs["image"])
    #plt.show()
    
    # WARNING! Be very careful when executing arbitrary commands on a real robot
    for i in range(10):
        action = 0 # Forward
        obs, reward, terminated, truncated, info = env.step(action)
        print(obs["distance"])

    print(obs["distance"])
    #plt.imshow(obs["image"])
    #plt.show()

    env.client.turn_off_client()