# 2B0T48
Hi! This is my attempt at a 2048 AI, able to learn from user input and play based on what aspects of the game it finds most important.

It uses my own interpretation and implementation of Ovolve's heuristic functions as well as hidden bias functions to analyze and give a 2048 board value. It uses this value to figure out what move is best given what heuristics it finds most important. While this AI doesn't perform quite as well as others with the same task, my goal was originally to create an AI that could play 2048 with meaningful objectives. Based off of that objective, I feel like I've accomplished my task (albeit inefficiently). Eventually I plan to upgrade and recreate this bot again!

## Installation and Deployment
Install the source files and extract contents to a folder.

**Make sure Python>=3.7 is installed and PIP3 is updated**
To install required python libraries:
```
python3 -m pip install -r requirements.txt
```
*requirements.txt* is found within the source files.

Run *main.py* to start the program. You can either input values for the heuristics via the sliders or use the learning function by pressing **Let 2B0T48 Learn**. If you have a 2048 game open in the background, the program will run and learn what weights are important based on your playing. To stop the program from learning, simply open or alt-tab to a different window and the program will come back to the home window. 

To have the program play the game 2048, press **Start 2B0T48!** and make sure a 2048 game is up in the background. The bot will continue to play 2048 until it loses or you exit the 2048 game window. 

## Acknowledgments

Ovolve's 2048-AI : https://github.com/ovolve/2048-AI/

2048 Site : https://play2048.co/
