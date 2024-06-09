from gpiozero import LED, Button
from signal import pause
from time import sleep
from input import *


def exec_command(func):
    led_green.on()
    func([])
    sleep(0.1)
    led_green.off()


def shutdown():
    led_red.close()
    led_green.close()
    button_clear.close()
    button_push.close()
    button_play.close()
    button_shutdown.close()
    from subprocess import call
    call("sudo shutdown -h now", shell=True)


led_red         = LED(18)
led_green       = LED(4)
button_clear    = Button(17, bounce_time = 0.1)
button_push     = Button(27, bounce_time = 0.1)
button_play     = Button(22, bounce_time = 0.1)
button_shutdown = Button(10, bounce_time = 0.5)

setup()

led_red.on()

button_clear.when_pressed    = lambda : exec_command(clear_images)
button_push.when_pressed     = lambda : exec_command(push_image)
button_play.when_pressed     = lambda : exec_command(play)
button_shutdown.when_pressed = shutdown

pause()
