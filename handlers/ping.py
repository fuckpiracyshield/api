import sys
import os
import random

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from ioutils.request import RequestHandler

class PingHandler(RequestHandler):

    """
    Handle simple pings to check the API availability.
    """

    # let's be fun
    responses = [
        'Pong!',
        'Do APIs dream of electric requests?',
        'So long and thanks for all the requests'
    ]

    def get(self):
        self.success(data = random.choice(self.responses))
