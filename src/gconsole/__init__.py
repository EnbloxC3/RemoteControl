"""Import gconsole

---

### Good Console
`gconsole`

This library provides pre-defined customizations that can be used to enhance terminal or console applications. It is a simple and easy-to-use library designed for creating a custom console with minimal effort. With `gconsole`, you can add style, color, and custom messaging to your command-line applications. The library offers the following features:

- **Color and Style Support:** Choose from a wide range of colors and styles for text. Create messages or alerts in different colors, and define specific coloring schemes for various events.
- **Custom Formatting:** Make text formatting more readable and meaningful. This is especially helpful when dealing with lengthy and complex console outputs, making the data easier to parse and understand.
- **Logging and Error Handling:** Provides an alternative to standard logging modules, allowing for more detailed or simplified logs for specific events. Errors can be conveyed to the user with custom formats and messages.
- **Easy Integration:** `gconsole` can be seamlessly integrated into Python projects and requires minimal setup. It enhances existing console applications without requiring complex configuration.

### Installation and Usage

To install the `gconsole` library, use the following command:

```
pip install gconsole
```

Here is a simple example:

```python
# Import GConsole
import gconsole as gcs

# Print a message in green and bold
gcs.Console.style_print("Hello, World!", color="green")
```

In the above example, the `Hello, World!` message is printed in green and bold text on the terminal. The `gconsole` library provides a variety of customization options to make your terminal applications more readable and user-friendly.

For more information and detailed usage examples, please refer to the documentation.
"""

import os as _OS

class Console:
  """
  This class is used to create a custom console.
  """
  def clear():
    """
    Clears the console.
    """
    if _OS.name == 'nt':  
      _OS.system('cls')
    else:
      _OS.system('clear')
  def style_print(text, color, sep: str | None = " ", end: str | None = '\n'):
    """
    Prints the given text with the specified color and style.
    """
    print(Style.style(text, color), sep=sep, end=end)
  def clear_lines(count=1):
    """
    Clears the current line.
    """
    for _ in range(count):
      print('\r' + ' ' * 100 + '\x1b[2K', end='\r')

  def clear_linechars(count=1):
    """
    Clears the specified number of characters in the current line.
    """
    print('\b' * count + ' ' * count + '\b' * count, end='', flush=True)
  
  def get_line():
    """
    Gets the current line content.
    """
    return input()
  def get_input(prompt):
    """
    Gets the user input.
    """
    return input(prompt)
  def get_input_with_default(prompt, default):
    """
    Gets the user input with a default value.
    """
    return input(prompt + ' [' + default + ']: ')
  
class Style:
  """
  This class is used to create custom styles for the console.
  """
  def style(text: str, color: str | None = "breset"):
    """
    Returns the text with the specified color.

    Colors:
    - "black": "\\033[30m",
    - "white": "\\033[37m",
    - "red": "\\033[31m",
    - "green": "\\033[32m",
    - "yellow": "\\033[33m",
    - "blue": "\\033[34m",
    - "magenta": "\\033[35m",
    - "cyan": "\\033[36m",
    - "reset": "\\033[0m",
    - "bold": "\\033[1m",
    - "underline": "\\033[4m",
    - "italic": "\\033[3m", 
    - "strikethrough": "\\033[9m",
    - "blink": "\\033[5m",
    - "reverse": "\\033[7m",
    - "hidden": "\\033[8m",
    - "double_underline": "\\033[21m",
    - "double_blink": "\\033[25m",
    - "bblack": "\\033[40m",
    - "bwhite": "\\033[47m",
    - "bred": "\\033[41m",
    - "bgreen": "\\033[42m",
    - "byellow": "\\033[43m",
    - "bblue": "\\033[44m",
    - "bmagenta": "\\033[45m",
    - "bcyan": "\\033[46m",
    - "breset": "\\033[49m",
    """
    color_codes = {
        "black": "\033[30m",
        "white": "\033[37m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "reset": "\033[0m",
        "bold": "\033[1m",
        "underline": "\033[4m",
        "italic": "\033[3m", 
        "strikethrough": "\033[9m",
        "blink": "\033[5m",
        "reverse": "\033[7m",
        "hidden": "\033[8m",
        "double_underline": "\033[21m",
        "double_blink": "\033[25m",
        "bblack": "\033[40m",
        "bwhite": "\033[47m",
        "bred": "\033[41m",
        "bgreen": "\033[42m",
        "byellow": "\033[43m",
        "bblue": "\033[44m",
        "bmagenta": "\033[45m",
        "bcyan": "\033[46m",
        "breset": "\033[49m",
      
    }
    color_code = color_codes.get(color.lower())
    if not color_code:
      raise ValueError("Invalid color!")
    return f"{color_code}{text}{color_codes['reset']}"

  

