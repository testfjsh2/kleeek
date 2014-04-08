#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Simplified chat demo for websockets.

Authentication, error handling, etc are left as an exercise for the reader :)
"""

import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import uuid
from tornado.options import define, options
from tornado.tcpserver import TCPServer

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            # (r"/", MainHandler),
            (r"/", FlashPolicyServer),
            (r"/chatsocket", ChatSocketHandler),
        ]
        settings = dict(
        # ========================================
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        # ========================================
        tornado.web.Application.__init__(self, handlers, **settings)


class FlashPolicyServer(TCPServer):

    def handle_stream(self, stream, address):
        self._stream = stream
        self._read_line()

    def _read_line(self):
        self._stream.read_until('\n', self._handle_read)

    def _handle_read(self, data):
        policyFile = """<cross-domain-policy> 
                            <allow-access-from domain="*" /> 
                            <allow-http-request-headers-from domain="*" headers="*"/> 
                        </cross-domain-policy>
                    """
        self._stream.write(policyFile + '\0')
        self._read_line()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        pass

class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = []
    cache_size = 200

    def allow_draft76(self):
        # for iOS 5.0 Safari
        return True

    def open(self):
        policyFile = """<cross-domain-policy> 
                            <allow-access-from domain="*" /> 
                            <allow-http-request-headers-from domain="*" headers="*"/> 
                        </cross-domain-policy>
                    """
        self.write_message(policyFile + '\0')
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        ChatSocketHandler.waiters.remove(self)

    @classmethod
    def update_cache(cls, chat):
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]

    @classmethod
    def send_updates(cls, chat):
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        logging.info("got message %r", message)
        ChatSocketHandler.update_cache(message)
        ChatSocketHandler.send_updates(message)


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
