# Find-Replace
A terminal based utility for find and replace in multiple files

## Installation
- Requires python3
- Install python packages in requirements.txt

## How to use
- All regular expression must be python `re` compatible
- `python main.py`
- On first screen enter 
    1. folder to search (`.` and `..` is also valid)
    2. filename pattern to search (e.g. `py$` for python files)
    3. text search pattern (e.g. `var(\d+)` to find all var1, var2...)
    4. replacement pattern (e.g. `variable_\1`)
    5. press `tab` or `down arrow` to move down, `up arrow` to move up, `enter` to go to next screen, `esc` to exit

- Main screen
    - keys: `up/down arrow` for movement, `space` to select/deselect entry/file, `enter` to confirm and apply changes, `backspace` go to previous screen and edit patterns, `esc` go to previous screen and start new search
