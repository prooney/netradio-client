
import sys
import json
from client import RadioClient
from client import printstreaminfo


if len(sys.argv) < 2:
    print('usage {} <serverip>'.format(argv[0]))

print('starting client: connecting to {}'.format(sys.argv[1]))
client = RadioClient('http://%s' % sys.argv[1])
cached_listing = client.list()


def printhelp():
    print('radio help:')
    print('commands')
    print(':e - exit')
    print(':h - print help')
    print(':p <uri-or-id> - play a radio stream')
    print(':v <volume> - set volume (between 0.0 and 10.0)')
    print(':s - stop')

def lookupstream(ident):

    for res in cached_listing:
        if res['id'] == ident:
            return res['streams'][0] # hope ther is one
    raise ValueError('invalid stream id')


def playcommand(param):
    
    if param.isdigit():
        uri = lookupstream(int(param))
        print('looked up stream for id %s is %s' % (param, uri))
    else:
        uri = param

    print('client will play with uri %s' % uri)
    client.play(uri)


def volumecommand(level):
    try:
        fltval = float(level)

        if 0.0 <= fltval <= 10.0:
            client.volume(fltval)
        else:
            print('out of range volume level')
    except ValueError:
        print('invalid volume level')


def getcommand():

    inp = raw_input('>')

    if len(inp) == 0:
        return None, None
    
    try:
        cmd, param = inp.split(' ')
        return cmd, param
    except ValueError:
        return inp, None
     


while True:

    try:
        cmd, param = getcommand()
        
    except KeyboardInterrupt:
        break

    if cmd == 'e':
        break

    elif cmd == 's':
        client.stop()

    elif cmd == 'h':
        printhelp()

    elif cmd =='p':
        if param:
            try:
                playcommand(param)
            except ValueError as ve:
                print(ve)
        else:
            print('must specify parameter')

    elif cmd == 'v':
        if param:
            volumecommand(param)
        else:
            print('must specify parameter')
        
    elif cmd == 'c':
        print('cachedinfo looks like: ')
        for cq in cached_listing:
            print(printstreaminfo(cq))

    elif cmd == 'l':
        print("get listing")
        res = client.list()
        print('There were {} results '.format(len(res)))
        cached_listing = res

    elif cmd == 'q':
        if param:
            res = client.search(param)

            print('There were {} results '.format(len(res)))

            for r in res:
                print(printstreaminfo(r))
        else:
            print('must specify parameter')

    else:
        print('unknown command')




        