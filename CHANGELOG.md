# Changelog

All notable changes to this project will be documented in this file.

## 0.3.0 - Un-Released

-   

## 0.2.0 - 03/23/2020

-   Add `CHANGELOG.md`
-   Added base `PyLint` support
-   Added `requirements.txt` for easier dependency management
-   Updated `README.md` with installation and boot instructions
-   Added support for environment variable configuration via `.env` file
-   Added the following dependencies
    -   `python-dotenv==0.12.0`
-   Added the following dev dependencies
    -   `pylint==2.4.4`

-   [[RPA-1]](https://github.com/doctorMcbob/RedPantsOrDieTrying/issues/3) Structural Refactor
    -   Separated game world and game player into their own objects
    -   Separated sprites out into their own directory
    -   Added dynamic sprite sheet loading
    -   Added support for dynamic level loading and default level selection

-   [[RPA-2]](https://github.com/doctorMcbob/RedPantsOrDieTrying/issues/10) Add GamePlayer kick flip mechanic
    -   Added `Kickflip` player states and sprites
    -   Tweaked platformer constants.
        -   Raised gravity
	-   Strengthened jumps
	-   Increased speed
	-   Increased dive velocity

-   [[RPA-3]](https://github.com/doctorMcbob/RedPantsOrDieTrying/issues/4) Decouple game object state from game state
    -   Switch game objects to classes
    -   Add the follolwing classes
        -   GameObject
        -   GameWorld
        -   GameWorldEntity
        -   GamePlayer
    -   Decouple game state, GamePlayer state, and GameWorld state

-   [[RPA-4]](https://github.com/doctorMcbob/RedPantsOrDieTrying/issues/5) Game objects should manage own sprites
    -   Per the relocation of player state to the Player class; sprites are now managed by their own game objects.


-   RPA-6 Walljump mechanic
    -   Walljump functionality
        - walljump startup frames : 3
        - walljump horizontal strength : 14
    -   Animations
    -   Hit detection redux
        - separated state logic to player object out of game world entity

## 0.1.0 - 03/18/2020

-   Released base MVP functionality
-   Added the following game levels
    -   `developer_playground`
-   Added the following sprites
    -   `player_one`
