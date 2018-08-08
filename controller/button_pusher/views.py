import serial
import termios

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


def push_button(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    port = '/dev/ttyACM0'

    # Disable reset after hangup
    with open(port) as f:
        attrs = termios.tcgetattr(f)
        attrs[2] = attrs[2] & ~termios.HUPCL
        termios.tcsetattr(f, termios.TCSAFLUSH, attrs)

    with serial.Serial(port, 9600) as arduino:
        arduino.write(b"{'action': 'motor'}")

    return HttpResponseRedirect(reverse('index'))
