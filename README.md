VidToMid.py:
usage: VidToMid.py i [args]
Generate a MIDI file from WAV

positional arguments:
  i                     File name

options:
  -h, --help            show this help message and exit
  -r R                  Minimum bin size
  -o O                  Overlap between fft bins. Increases notes per second with higher numbers. range 0.0 to 0.99.
  -t T                  Number of midi tracks.
  -m M                  How much to add to the multiplier when the minimum bin size is reached
  -n N                  Note count.
  --threads THREADS     How many threads the script uses to process. More threads use more ram.
  --ppqn PPQN           PPQN of the midi file.
  --bpm BPM             Bpm of the midi
  --ascii-res ASCII_RES Resolution of output ascii. default=60,60
  --video-res VIDEO_RES Resolution the video is scaled to before being processed. default=480,135

AsciiImage.py:
AsciiImage.asciify(image_in, width, height) 
AsciiImage.ascii_video(filename, ascii_size: tuple, video_size: tuple, silent=False):
