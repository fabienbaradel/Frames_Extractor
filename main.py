import argparse
import os
import subprocess
import time
import sys
import ipdb
import re


def main(args):
    # Parameters from the args
    dir, h, w, fps, extension, do_extract_frames = args.dir, args.height, args.width, args.fps, args.extension, args.extract_frames

    # Get the video filenames
    list_video_fn = get_all_videos(dir, extension)

    print("{} videos to uncompressed in total".format(len(list_video_fn)))

    # Loop over the video and extract
    op_time = AverageMeter()
    start = time.time()
    list_error_fn = []
    for i, video_fn in enumerate(list_video_fn):
        try:
            # Rescale
            video_fn_rescaled = rescale_video(video_fn, w, h, fps)

            if do_extract_frames:
                # Extract
                extract_frames(video_fn_rescaled, w, h, fps)

            # Log
            duration = time.time() - start
            op_time.update(duration, 1)
            print("{}/{} : {time.val:.3f} ({time.avg:.3f}) sec/video".format(i + 1, len(list_video_fn), time=op_time))
            sys.stdout.flush()
            start = time.time()
        except:
            print("Impossible to extract frames for {}".format(video_fn))
            list_error_fn.append(video_fn)

    print("\nDone")
    print("\nImpossible to extract frames for {} videos: \n {}".format(len(list_error_fn), list_error_fn))


class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def get_duration(file):
    """Get the duration of a video using ffprobe. -> https://stackoverflow.com/questions/31024968/using-ffmpeg-to-obtain-video-durations-in-python"""
    cmd = 'ffprobe -i {} -show_entries format=duration -v quiet -of csv="p=0"'.format(file)
    output = subprocess.check_output(
        cmd,
        shell=True,  # Let this run in the shell
        stderr=subprocess.STDOUT
    )
    # return round(float(output))  # ugly, but rounds your seconds up or down
    return float(output)


def rescale_video(video_fn, w, h, fps):
    """ Rescale a video according to its new width, height an fps """

    # Output video_name
    video_dir, video_name = '/'.join(video_fn.split('/')[:-1]), video_fn.split('/')[-1]
    video_name_rescaled = video_name.split('.')[0] + '_{}x{}_{}.mp4'.format(w, h, fps)
    video_fn_rescaled = os.path.join(video_dir, video_name_rescaled)

    # Run a subprocess using ffmepg
    subprocess.call('ffmpeg -i {video_input} -vf scale={w}:{h} -r {fps} -y {video_output} -loglevel panic'.format(
        video_input=video_fn,
        h=h,
        w=w,
        fps=fps,
        video_output=video_fn_rescaled
    ), shell=True)

    # Get the duration of the new video (in sec)
    duration_sec = get_duration(video_fn_rescaled)
    duration_frames = int(duration_sec * fps)

    # Update the name of the file
    video_name_rescaled_dur = video_name_rescaled.split('.')[0] + '_{}.mp4'.format(duration_frames)
    video_fn_rescaled_dur = os.path.join(video_dir, video_name_rescaled_dur)
    os.rename(video_fn_rescaled, video_fn_rescaled_dur)

    return video_fn_rescaled


def extract_frames(video_fn, w, h, fps):
    # Create the dir for the frames
    dir = '/'.join(video_fn.split('/')[:-1])
    dir_frames = os.path.join(dir, 'frames_{}x{}_{}'.format(w, h, fps))

    if not os.path.isdir(dir_frames):
        os.makedirs(dir_frames)

    # Extract frames
    subprocess.call('ffmpeg -i {video} {dir_frames}/$filename%06d.jpg -loglevel panic'.format(video=video_fn,
                                                                                              dir_frames=dir_frames
                                                                                              ), shell=True)

    # Remove the video
    os.remove(video_fn)


def get_all_videos(dir, extension='mp4'):
    """ Return a list of the video filename from a directory and its subdirectories """

    list_video_fn = []
    for dirpath, dirnames, filenames in os.walk(dir):
        for filename in [f for f in filenames if f.endswith(extension)]:
            fn = os.path.join(dirpath, filename)
            list_video_fn.append(fn)

    return list_video_fn


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract frames')
    parser.add_argument('--dir', metavar='DIR',
                        default='/Users/fabien/Downloads/avi',
                        help='path to avi dir')
    parser.add_argument('--width', default=256, type=int,
                        metavar='W', help='Width')
    parser.add_argument('--height', default=256, type=int,
                        metavar='H', help='Height')
    parser.add_argument('--fps', default=30, type=int,
                        metavar='FPS',
                        help='Frames per second for the extraction, -1 means that we take the fps from the video')
    parser.add_argument('--extension', metavar='E',
                        default='mp4',
                        help='Extension of the video files')

    parser.add_argument('--extract-frames', dest='extract_frames', action='store_true',
                        help='whether to extract frames (if yes we do not keep the video)')

    args = parser.parse_args()

    main(args)
