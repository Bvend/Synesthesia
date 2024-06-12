# test module dedicated to running the application from the terminal.


from image_processing import load_image, pre_process_image
from composer import get_audio_from_image
from synthesizer import write_wav, play_audio

import numpy as np


DEFAULT_IMG = '8.jpg' # image used by the 'push' command without arguments.

audio_list = []
# list of generated audio tracks, one per image.


def display_help(input_args):
    for key, (func, args, desc) in command_dict.items():
        command = ' '.join([key] + args)
        print(f'{command}: {desc}')
    return True


def shut_down(input_args):
    return False


def push_image(input_args):
    file_name = input_args[1] if len(input_args) > 1 else DEFAULT_IMG
    img = load_image(file_name)
    bin_img, color_img = pre_process_image(img, debug = True)
    audio = get_audio_from_image(bin_img, color_img, debug = True)
    audio_list.append(audio)
    return True


def clear_images(input_args):
    audio_list.clear()
    return True


def play(input_args):
    if len(audio_list) == 0:
        print('The queue is empty!')
    else:
        output = np.concatenate(audio_list)
        write_wav('out.wav', output)
        play_audio('out.wav')
    return True


command_dict = {
    'help':  (display_help, [],      'Display the command list.'),
    'quit':  (shut_down, [],         'Shut down Synesthesia.'),
    'push':  (push_image, ['image'], 'Load \'image\' to the end of the queue.'),
    'clear': (clear_images, [],      'Delete all images from the queue.'),
    'play':  (play, [],              'Play your piece!')
}


def setup():
    pass


def run():
    is_running = True
    print('Running Synesthesia…')
    print('Try typing \'help\' for the command list!\n')

    while is_running == True:
        input_args = input('> ').split()
        if len(input_args) > 0 and input_args[0] in command_dict:
            func = command_dict[input_args[0]][0]
            is_running = func(input_args)
        else:
            print('Couldn\'t find your command! Try \'help\', perhaps?')
        print()

    print('Shutting down Synesthesia…')


def main():
    setup()
    run()


if __name__ == "__main__":
    main()
