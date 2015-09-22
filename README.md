# drac
A python implementation of the *incredibly* popular Fury of Dracula game.


## FAQ

##### How do I launch the game?
You can launch it from the `drac.py` file, from console or otherwise. I'm working out a better way.

##### How can I make this work how I want it to?
See the `drac_config.py` file? That's drac's config. Use it wisely.

##### How do I play this glorious thing?
Use the config to change drac's mode:
* **Plays**, **Turns**: The program's first argument is the past plays string.
* **Interactive**: Just run `drac.py`, it will greet you with the interactive menu.
* **Networked**: WIP. Client-server system according to `drac_config.py`, allowing network play.
* **Pygame**: WIP. Graphical representation of the game using the pygame module.
* **AI Mode**: WIP. Allows AI modules to be used to battle it out.

##### Why did you decide this was a good idea?
COMP1927's second assessment is/was doing this in C, and I decided to do it in Python too, as a side project.

## Contributors
* Nick Robson: Programming

## Licensing
drac is licensed under the GNU AFFERO GENERAL PUBLIC LICENSE v3.

This means:

| **Required** | **Permitted** | **Forbidden** |
| --- | --- | --- |
| Disclose Source              | Commercial Use | Hold Liable  |
| License and copyright notice | Distribution   | Sublicensing |
| Network Use is Distribution  | Modification   | |
| State Changes                | Patent Grant   | |
|                              | Private Use    | |

This means modifications:
* must be open source (Source Code is publically available)
* must include the same LICENSE (use AGPL v3)
* must provide full software access (including Source Code) to anyone using the software via network
* must explicitly state changes between the modification and the original software

Please see the provided LICENSE file for more information.
