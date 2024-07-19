from scipy.signal import convolve2d
from scipy.ndimage import gaussian_filter
import numpy as np 
from PIL import Image
from matplotlib import pyplot as plt
import cv2
import time

def id_from_angle(angle):
    if angle == 180: return 4
    angle %= 180
    if   angle < 10:  return 0
    elif angle < 80:  return 1
    elif angle < 100: return 2
    elif angle < 170: return 3
    else:             return 0

def char_from_id(id):
    if id == 0: return '|'
    if id == 1: return '\\'
    if id == 2: return '-'
    if id == 3: return '/'
    if id == 4: return ' '

chars = ' .\'":!+}1248GH#@▮'
chars = ' .":+}14G#@'
def luminance_to_char(value):
    value = value / 256
    return chars[round(value * (len(chars) - 1))]

def asciify(image_in, width, height):
    image = image_in

    if image.width > image.height:
        dims = (height, round(height * (image.height / image.width)))
    else:
        dims = (round(width * (image.width / image.height)), width)
    

    np_image = np.array(image_in.convert('F'))

    gaussian_clip = (np_image) - gaussian_filter(np_image, 1)
    average = np.sum(abs(gaussian_clip)) / (image.width * image.height) * 1
    gaussian_clip = gaussian_clip > average

    sobelX = convolve2d(gaussian_clip, [[1,2,1],[0,0,0],[-1,-2,-1]], mode='same')
    sobelY = convolve2d(gaussian_clip, [[-1,0,1],[-2,0,2],[-1,0,1]], mode='same')

    angles = np.array(image.convert('L'))
    
    angles = np.arctan2(sobelX,sobelY) / np.pi * 180 + 180# / np.pi / 180 + 180

    for x in range(len(angles)):
        for y in range(len(angles[x])):
            angles[x][y] = id_from_angle(angles[x][y])

    luminance = image.convert('L').resize(dims)
    angles = Image.fromarray(angles).resize(dims, Image.Resampling.NEAREST)
    image = image.resize(dims)

    string = ''
    for y in range(image.height):
        for x in range(image.width):
            char_id = angles.getpixel((x,y))
            if char_id == 4:
                char = luminance_to_char(luminance.getpixel((x,y)))
            else:
                char = char_from_id(char_id)
            string += char
        string += '\n'

    return string

def ascii_video(filename, ascii_size, video_size, silent=False):
    video = cv2.VideoCapture(filename)

    frame_count = int(video.get(7))
    frame_rate = video.get(5)

    total_time = 0

    frames = []
    for i in range(frame_count):
        t = time.time()

        ret,frame = video.read()

        if not ret: break

        image = Image.fromarray(frame)
        if not video_size is None:
            image = image.resize(video_size)

        frame = asciify(image, ascii_size[0], ascii_size[1])

        frames.append(frame)

        time_taken = time.time() - t
        total_time += time_taken

        if silent: continue # don't print

        print(frame)

        percentage = i / frame_count
        fps        = 1 / (total_time / (i + 1))
        eta        = frame_count / fps * (1 - percentage)

        print(f"    {round(percentage * 100)}%, FPS: {round(fps, 1)} ETA: {round(eta, 1)}s")

    print(len(frames), frame_count, frame_rate)

    return (frames, len(frames), frame_rate)

if __name__ == '__main__':
    import mido
    import sys

    frames, frame_count, frame_rate = ascii_video(sys.argv[1], (60,60), (480,180))

    midi = mido.MidiFile()
    midi.tracks.append(mido.MidiTrack())

    for frame in frames:
        midi.tracks[0].append(mido.MetaMessage('lyrics', text=frame))
        midi.tracks[0].append(mido.Message('note_on', note=0, time=0))
        midi.tracks[0].append(mido.Message('note_off', note=0, time=80))

    midi.save(sys.argv[1] + '.mid')