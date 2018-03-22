# README

Given a directory of mp4 files, extract the frames

Input:
avi ----> 1 ---> clip.mp4
     |
      --> 2 ---> clip.mp4
     |
     ...
     |
     ---> n ---> clip.mp4

Output:
avi ----> 1 ---> clip.mp4
     |       |
     |       -> frames -> 01.png ... 0N.png
     |
      --> 2 ---> clip.mp4
     |       |
     |       -> frames -> 01.png ... 0N.png
     |
     ...
     |
     ---> n ---> clip.mp4
             |
             -> frames -> 01.png ... 0N.png
             
## Call example
```
python main.py --dir <path-to-you-dir> --height 320 --width 240 --fps 30 --extension mp4
```

## Requirements
python 3.5
ffmpeg
           
## TODO
* Multiprocessing