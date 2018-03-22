import argparse
import os
import subprocess
import time


def main(args):
    # Parameters from the args
    dir, h, w, fps, extension = args.dir, args.height, args.width, args.fps, args.extension

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

            # Extract
            extract_frames(video_fn_rescaled, w, h, fps)

            # Log
            duration = time.time() - start
            op_time.update(duration, 1)
            print("{}/{} : {time.val:.3f} ({time.avg:.3f}) sec/video".format(i + 1, len(list_video_fn), time=op_time))
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


def rescale_video(video_fn, w, h, fps):
    """ Rescale a video according to its new width, height an fps """

    # Output video_name
    video_fn_rescaled = '/'.join(video_fn.split('/')[:-1]) + '/{}x{}_{}.mp4'.format(w, h, fps)

    # Run a subprocess using ffmepg
    subprocess.call('ffmpeg -i {video_input} -vf scale={w}:{h} -r {fps} -y {video_output} -loglevel panic'.format(
        video_input=video_fn,
        h=h,
        w=w,
        fps=fps,
        video_output=video_fn_rescaled
    ), shell=True)

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
    parser.add_argument('--width', default=320, type=int,
                        metavar='W', help='Width')
    parser.add_argument('--height', default=240, type=int,
                        metavar='H', help='Height')
    parser.add_argument('--fps', default=30, type=int,
                        metavar='FPS',
                        help='Frames per second for the extraction, -1 means that we take the fps from the video')
    parser.add_argument('--extension', metavar='E',
                        default='mp4',
                        help='Extension of the video files')

    args = parser.parse_args()

    main(args)
