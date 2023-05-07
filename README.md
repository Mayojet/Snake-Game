# Introduction
This new variant of the traditional SNAKE GAME aims to take the classic to the next level by incorporating two advanced features (random portals and obstacles). With the refine UI design, this game should bring back the good old days memory back to the player. At the same time, this game also has a built-in bot that automatically plays the game which gives more possibilities to the original game.

For more details, view the full project proposal [here](https://docs.google.com/document/d/1zNwCtxuIW_G-cObu6rI39XY_0by7GYty6APoNpppgfg/edit?usp=sharing).

# Technical Architecture
![abc](https://user-images.githubusercontent.com/74951277/236370639-95f0d77e-fb17-45c7-885c-0e7d6a8b3706.jpg)


# Installation
## Clone Repo
To clone this repo, simply run the following:

```
git clone https://github.com/CS222-UIUC/course-project-purdue-hotties.git
```
## Package Management

To install required packages, run the following:

```
pip install -r requirements.txt
```

# Game Instructions
To launch the game faster, run the following **ONCE**

```
chmod +x ./main.py
```
Then, to launch the game, run with following:

```
./main.py
```

Otherwise, depending on the python version, run the  following:  

```
python3 ./main.py #Python3 uses python3, Python2 uses python
```

# Testing Instructions
## Run unit tests
```
python3 -m pytest -v
```
## Check coverage
```
python3 -m pytest --cov=.
```

# Developers
- **Alex Guo**: Worked on basic snake game and welcome/end screens.  
- **Yujie Miao**: Worked on basic snake game and timer feature. 
- **David Li**: Worked on basic snake game, testing, portal feature, and bot benchmarking. 
- **Wilson Sun**: Worked on basic snake game, testing, obstacle feature, and automation bot.  


# Source Credit
1. https://github.com/codebasics/python_projects/tree/main/1_snake_game
2. https://github.com/clear-code-projects/Snake
3. https://freepngimg.com/artistic/portal
