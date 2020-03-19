# Red Pants or Die Trying

## the next iteration in the Red Pants saga

----------------

### What is Red Pants?

The first game I ever created was my senior project in high school, it was titled:
"Guy in red pants and a blue shirt in the MS Paint Jungle."
Well Red Pants man has long escaped the MS Paint Jungle, thankfully, and I have been using the character to make platformers on and off for a few years.

His pants are red, his shirt is blue, and he's here to jump all over the place.

### How do I play this game?

Red Pants games are all built in Python using Pygame. For now, you will need to install Python and Pygame to run the script.

If the project gets far enough, I'll make an executable using pyinstaller or something for an itch.io release.

### Can I give you a job?

Yes! I'm pretty good with python. Please email me at wootenwesley@gmail.com

## Installation
- `pip install -r requirements.txt`
- Get pylint for your desired IDE/text editor
	- https://github.com/SublimeLinter/SublimeLinter-pylint
	- https://code.visualstudio.com/docs/python/linting
	- https://atom.io/packages/linter-pylint
- `cp .pylintrc.example .pylintrc`
	- fill in required values
- `cp .env.sample .env`
	- alter values if desired

## Boot up
`python boot {options}`

### Options
`-d`: Enable debug mode. This allows frame-by-frame debug pausing.
`-f`: Start game in fame-by-frame freeze frame state. Must also have `-d`