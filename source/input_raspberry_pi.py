# module dedicated to running the application from raspberry pi.


from image_processing import take_photo, pre_process_image
from composer import get_audio_from_image
from synthesizer import write_wav, initialize_audio_player, play_audio

import numpy as np
from gpiozero import LED, Button
from signal import pause
from subprocess import call
from time import sleep


audio_list = []
# list of generated audio tracks, one per image.


def shut_down():
    led_red.close()
    led_green.close()
    button_shutdown.close()
    button_play.close()
    button_push.close()
    button_clear.close()
    call("sudo shutdown -h now", shell=True)


def play():
    if len(audio_list) > 0:
        output = np.concatenate(audio_list)
        write_wav('out.wav', output)
        play_audio('out.wav')


def push_image():
    img = take_photo()
    bin_img, color_img = pre_process_image(img)
    audio = get_audio_from_image(bin_img, color_img)
    audio_list.append(audio)


def clear_images():
    audio_list.clear()


def execute_command(func):
    led_green.on()
    func()
    sleep(0.1)
    led_green.off()


led_red         = LED(18)
led_green       = LED(4)
button_shutdown = Button(10, bounce_time = 0.5)
button_play     = Button(22, bounce_time = 0.1)
button_push     = Button(27, bounce_time = 0.1)
button_clear    = Button(17, bounce_time = 0.1)

initialize_audio_player()

led_red.on()

button_shutdown.when_pressed = shut_down
button_play.when_pressed     = lambda : execute_command(play)
button_push.when_pressed     = lambda : execute_command(push_image)
button_clear.when_pressed    = lambda : execute_command(clear_images)

pause()
