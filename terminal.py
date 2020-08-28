# terminal.py
# CLI utilities for IO
# Copyright © Nathan Sales 2020

normal = "\033[0m"


class color:
    red = "\033[91m"
    yellow = "\033[93m"
    green = "\033[92m"
    blue = "\033[94m"
    purple = "\033[95m"


class style:
    italic = "\033[3m"
    underline = "\033[4m"
    bold = "\033[1m"


class status:
    # Success, something worked.
    success = ("[" + color.green + '✓' + normal + "] SUCCESS:")

    # Informational. Not necessarily something positive or negative. Just a heads up.
    info = ("[" + color.blue + 'i' + normal + "] INFO:")

    # Small problems that won't effect the programs execution. Best practices, old versions, things to speed up performance, etc.
    low = ("[" + color.yellow + '!' + normal + "] (low) ERROR:")

    # Medium priority, things that will crash the program. Dependency problems and invalid arguments would fall into this category.
    medium = ("[" + color.yellow + '✖' + normal + "] (medium) ERROR:")

    # Things that effect more than just the current program. Such as the database server is down or system load is too high.
    high = ("[" + color.red + '⚠' + normal + "] (high) ERROR:")

    # The whole machine is about to go down if it hasn't already.
    critical = ("[" + color.red + '☠' + normal + "] (critical) ERROR:")
