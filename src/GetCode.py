from random import Random
from uuid import uuid1
from datetime import datetime

def encode(code):
    coden, resp, prev, key = 0, '', 0, Random(uuid1().node).randint(0,99999999999999999)*10+1
    for c in ''.join([str(bin(int(f'{int(c)//8}{int(c)%8}')))[2:].zfill(8) for c in code.split('.')]): coden = coden*2 + int(c)
    for c in str(coden)+''.join(code.split(".")): resp, prev = f'{resp}{(int(c)+prev)%10}', int(c)
    return (int(resp)*key)%(10**18), key

enc = encode(datetime.now().strftime('%m.%d.%H.%M'))
print(f'{enc[0]}{enc[1]}')
input("")
quit()
