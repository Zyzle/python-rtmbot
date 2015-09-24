#!/usr/bin/env python
from __future__ import print_function

import time

from slackclient import SlackClient

from settings import *

class Bot(object):
    PLUGINS = []

    """docstring for Bot"""
    def __init__(self):
        self.slack_client = None
        self.last_ping = 0

    def connect(self):
        self.slack_client = SlackClient(TOKEN)
        self.slack_client.rtm_connect()

    def start(self):
        self.connect()
        while True:
            for msg in self.slack_client.rtm_read():
                self.input(msg)
            self.autoping()
            time.sleep(.2)

    def autoping(self):
        now = int(time.time())
        if now > self.last_ping + 5:
            self.slack_client.server.ping()
            self.last_ping = now

    def input(self, data):
        for msgType, plugin in self.PLUGINS:
            if msgType == data['type']:
                output = plugin(data)

    def output(self):
        pass
        #for plugin in self.plugins:
        #    limiter = False
        #    for output in plugin.do_output():
        #        channel = self.slack_client.server.channels.find(output[0])
        #        if channel != None and output[1] != None:
        #            if limiter:
        #                time.sleep(.2)
        #                limiter = False
        #            message = output[1].encode('ascii', 'ignore')
        #            channel.send_message("{}".format(message))
        #            limiter = True

    @classmethod
    def plugin(cls, msgType):
        def inner(func):
            cls.PLUGINS.append((msgType, func))
        return inner

@Bot.plugin("message")
def doSomething(data):
    return "Hi from the plugin"

@Bot.plugin("pong")
def showPong(data):
    return "got pong!"

if __name__ == '__main__':
    bot = Bot()
    bot.start()
