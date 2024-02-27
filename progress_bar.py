""" progress bar"""

import time
import sys

def print_progress_bar(duration, msg='', bar_length=50):
    """
    Prints a progress bar with a message to the terminal.

    :param duration: The number of seconds the progress bar will run.
    :param msg: The message to display before the progress bar.
    :param bar_length: The character length of the bar (default is 50).
    """
    for i in range(duration):
        # Calculate the percentage completion.
        percent = (i + 1) / duration
        filled_length = int(bar_length * percent)

        # Create the bar string.
        progress = '█' * filled_length + '-' * (bar_length - filled_length)

        # Print the progress bar with the message.
        sys.stdout.write(f'\r{msg} |{progress}| {percent*100:.2f}% Complete')
        sys.stdout.flush()

        # Sleep for one second.
        time.sleep(1)

    # Print a newline at the end to ensure the next terminal output is on a new line.
    print()

# You can add some testing code here to see how it works when you run this module directly.
if __name__ == '__main__':
    # Test the progress bar function.
    print_progress_bar(60, msg='Loading')
    