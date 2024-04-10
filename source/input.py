from image_processing import *
from synth import *


# Imagem utilizada pelo comando 'push' sem argumentos:
DEFAULT_IMG_PATH = './img.bmp'


def display_help(input_args):
    for key, (func, args, desc) in command_dict.items():
        command = ' '.join([key] + args)
        print(f'{command}: {desc}')
    return True


def shut_down(input_args):
    return False


def push_image(input_args):
    img_path = input_args[1] if len(input_args) > 1 else DEFAULT_IMG_PATH
    img = load_image(img_path)
    bin_img = binarize_image(img, debug = False)
    notes = get_notes_from_image(bin_img, NUM_NOTES, 3)
    img_output = generate_audio_from_notes(notes)
    wav.write('output.wav', SAMPLE_RATE, img_output.astype(np.float32))
    return True


def clear_images(input_args):
    return True


def play(input_args):
    return True


command_dict = {
    'help':  (display_help, [],        'Display the command list.'),
    'quit':  (shut_down,    [],        'Shut down Synesthesia.'),
    'push':  (push_image,   ['image'], 'Load \'image\' to the end of the queue.'),
    'clear': (clear_images, [],        'Delete all images from the queue.'),
    'play':  (play,         [],        'Play your piece!')
}


def run():
    calculate_note_frequencies()

    is_running = True
    print('Running Synesthesia…')
    print('Try typing \'help\' for the command list!\n')

    while is_running == True:
        input_args = input('> ').split()
        if input_args[0] in command_dict:
            func = command_dict[input_args[0]][0]
            is_running = func(input_args)
        else:
            print('Couldn\'t find your command! Try \'help\', perhaps?')
        print()

    print('Shutting down Synesthesia…')


run()
