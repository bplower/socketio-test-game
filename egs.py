from aiohttp import web
import socketio
import random

class Player(object):
    def __init__(self, sid):
        self.sid = sid
        self.posx = random.randint(0, 800)
        self.posy = random.randint(0, 600)
        self.velx = 0
        self.vely = 0
        self.icon = random.choice(['jack-o-lantern1'])

    def state(self):
        return {
            'sid': self.sid,
            'posx': self.posx,
            'posy': self.posy,
            'velx': self.velx,
            'vely': self.vely,
            'icon': self.icon
        }

async def index(request):
    """Serve the client-side application."""
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


sio = socketio.AsyncServer()
app = web.Application()
app.router.add_static('/static', 'static')
app.router.add_get('/', index)
sio.attach(app)

players = {}


@sio.on('connect')
async def connect(sid, environ):
    players[sid] = Player(sid)
    print("connected: {} (total players: {})".format(sid, len(players)))
    sio.enter_room(sid, 'allplayers')
    # Tells the newcomer who is already on the server
    await sio.emit("addplayers", list(map(lambda x: players[x].state(), players)), room=sid)
    # Notifies everyone else
    await sio.emit("addplayer", players[sid].state(), room='allplayers', skip_sid=sid)

@sio.on('disconnect')
async def disconnect(sid):
    del players[sid]
    print("disconnected: {} (total players: {})".format(sid, len(players)))
    await sio.emit("removeplayer", sid, room='allplayers', skip_sid=sid)



@sio.on('playerupdate')
async def playerupdate(sid, data):
    print('playerupdate: ', sid)
    if 'velx' in data:
        players[sid].velx = data['velx']
    if 'vely' in data:
        players[sid].vely = data['vely']
    if 'posx' in data:
        players[sid].posx = data['posx']
    if 'posy' in data:
        players[sid].posy = data['posy']
    data['sid'] = sid

    # data = list(map(lambda x: players[x].state(), players))
    await sio.emit('setplayermovement', data, room='allplayers')

if __name__ == '__main__':
    try:
        web.run_app(app, port=8000)
    except KeyboardInterrupt:
        for i in players:
            sio.disconnect(i)
