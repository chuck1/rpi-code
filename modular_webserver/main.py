import asyncio
import functools
import math

import base64
import aiohttp
from aiohttp import web


async def websocket_handler(request):
    
    robot = request.app['robot']

    print('create websocket response')
        
    ws = web.WebSocketResponse()

    print('await prepare')
    await ws.prepare(request)

    print('prepare complete')
     
    async for msg in ws:
        print(msg)
        if msg.type == aiohttp.WSMsgType.JSON:

            ev = msg.json()

            element = app['program'].map_elements[ev["element"]]

            f = getattr(element, "on_" + ev["event_type"])

            f(ev)

        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' % ws.exception())

        program.update()

    print('websocket connection closed')

    return ws

###########################################

class Element:
    def __init__(self, name):
        self.name = name

class ButtonUp(Element):
    def on_mousedown(self, ev):
        self.program.state.up = True
    def on_mouseup(self, ev):
        self.program.state.up = False
    def on_mouseleave(self, ev):
        self.program.state.up = False

class ButtonDown(Element):
    def on_mousedown(self, ev):
        self.program.state.down = True
    def on_mouseup(self, ev):
        self.program.state.down = False
    def on_mouseleave(self, ev):
        self.program.state.down = False

class RangeInput(Element):
    def on_range_input(self, ev):
        self.program.state.speed = ev["value"]

class State:
    def __init__(self):
        self.speed = 0
        self.direction = 0
        self.down = False
        self.up = False

    def direction(self):
        if self.down and self.up: return 0
        if self.down: return -1
        if self.up: return 1
        return 0

class Program:
    def __init__(self, app, elements=[]):
        self.elements = elements

        for element in elements:
            element.program = self

        self.map_elements = dict((e.name, e) for e in self.elements)

        self.state = State()

    def update(self):
        
        # send message to arduino 

        b = struct.pack('fi', self.state.speed, self.state.direction())

        if hasattr(self, "server_protocol"):
            self.server_protocol.transport.write(b)

######################################

class ServerProtocol(asyncio.Protocol):
    def __init__(self, program):
        self.program = program
        self.program.server_protocol = self

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

######################################

async def run(fut):

    app = web.Application()

    p = Program(
            app,
            elements=[
                ButtonUp("up"),
                ],
            );
    
   
    app['prog'] = p

    server = await loop.create_server(functools.partial(ServerProtocol, p), '0.0.0.0', 40000)
    
    app.router.add_get('/ws', websocket_handler)
    app.router.add_static('/', 'static')
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start() 

    await fut
    
loop = asyncio.get_event_loop()
fut = loop.create_future()
loop.run_until_complete(run(fut))








