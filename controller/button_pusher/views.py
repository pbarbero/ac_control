import serial
import termios

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import TemplateView

from .models import ButtonPush


ARDUINO_PORT = '/dev/ttyACM0'


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['push_count'] = ButtonPush.objects.count()
        context['temperature'] = self.get_temperature()
        return context

    @staticmethod
    def get_temperature():
        # Disable reset after hangup
        with open(ARDUINO_PORT) as f:
            attrs = termios.tcgetattr(f)
            attrs[2] = attrs[2] & ~termios.HUPCL
            termios.tcsetattr(f, termios.TCSAFLUSH, attrs)

        with serial.Serial(ARDUINO_PORT, 9600) as arduino:
            arduino.write(b"{'action': 'temperature'}")
            return arduino.readline().strip().decode('ascii')


def push_button(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    # Disable reset after hangup
    with open(ARDUINO_PORT) as f:
        attrs = termios.tcgetattr(f)
        attrs[2] = attrs[2] & ~termios.HUPCL
        termios.tcsetattr(f, termios.TCSAFLUSH, attrs)

    with serial.Serial(ARDUINO_PORT, 9600) as arduino:
        arduino.write(b"{'action': 'motor'}")

    button_push = ButtonPush(user=request.user)
    button_push.save()

    return HttpResponseRedirect(reverse('index'))
