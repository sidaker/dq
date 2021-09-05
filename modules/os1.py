import os
from pathlib import Path

curr_path = os.path.dirname(os.path.dirname(__file__))
print(curr_path)

path = Path(curr_path)
print(path.parent.absolute())
