# A3CSuperMario_Windows
## result

![alt text](https://raw.githubusercontent.com/xushsh163/A3CSuperMario_Windows/master/result.gif)

3 threads

after 4000 episodes, about 30% chance of Clearance

after 8000 episodes, about 70% chance of Clearance

## Enviroment

Install NES emulator [FCEUX](http://www.fceux.com/web/home.html)

lua scripts and nes files in 'SuperMarioBros' Folder are modified from [gym-super-mario](https://github.com/ppaquette/gym-super-mario)

Install pywin32

using win32 named pipe to comunicate with FCEUX, so support winodws only

## Config

> config.py
```
FCEUX_PATH = 'D:\\fceux-2.2.3-win32\\fceux.exe'
```
change to your install path

> A3CTrainer.py
```
load_model = False
```
change to True if you need to continue training

## Run

Train

```
python A3CTrainer.py
```

Test

```
python A3CTester.py
```


## A3C model

[introduction article to this impelement](https://zhuanlan.zhihu.com/p/53907806)

A3C model implements is from this article 《[simple-reinforcement-learning-with-tensorflow-part-8-asynchronous-actor-critic-agents-a3c](https://medium.com/emergent-future/simple-reinforcement-learning-with-tensorflow-part-8-asynchronous-actor-critic-agents-a3c-c88f72a5e9f2)》.

I have tried a lot of A3C implements and this one is most efficient.

