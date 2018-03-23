Extract frames from video in Python
======================================================

Given a directory of mp4 files, extract the frames


Input dir:
```
avi ----> 1 ---> clip.mp4
     |
      --> 2 ---> clip.mp4
     |
     ...
     |
     ---> n ---> clip.mp4
```

Output dir:
```
avi ----> 1 ---> clip.mp4
     |       |
     |       --> frames ---> 01.png ... 0N.png
     |
      --> 2 ---> clip.mp4
     |       |
     |       --> frames ---> 01.png ... 0N.png
     |
     ...
     |
     ---> n ---> clip.mp4
             |
             --> frames ---> 01.png ... 0N.png
```
             
## Example
```python
python main.py --dir <path-to-you-dir> --height 320 --width 240 --fps 30 --extension mp4
```

## Requirements
- [x] python 3.5
- [x] ffmpeg
           
## TODO
* Multiprocessing