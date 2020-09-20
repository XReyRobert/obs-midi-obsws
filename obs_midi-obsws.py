import asyncio
import simpleobsws
import json
import sys
import getopt

loop = asyncio.get_event_loop()
ws = simpleobsws.obsws(host='127.0.0.1', port=4444,
                       loop=loop)

async def get_midi_scenes():
    '''return a json with all OBS scenes containing sources with "MIDI" in their name
       '''

    midiscenes = json.loads("{\"names\":[]}")

    data = {}
    result = await ws.call('GetSceneList', data)  # Make a request with the given data
    scenes = result["scenes"]

    for scene in scenes:
        sources = scene["sources"]
        sourcenames = list(map(lambda source: source['name'], sources))
        midisources = list(filter(lambda source: ("MIDI" in source), sourcenames))
        if len(midisources) > 0:
            midiscenes["names"].append(scene["name"])

    return midiscenes

async def send_request(request, data):
    '''send data message to all scenes containing sources with "MIDI" in their name
    ex:
        request = SetSceneItemRender
        data = "{\"source\": \"MIDI_1_"& data1 & "_" & data2 & "\", \"render\": false}
    '''

    scenes = await get_midi_scenes()

    # sourcename = "MIDI_"+channel+"_"+data1+"_"+data2

    for scene in scenes["names"]:
        data["scene"]=scene
        result = await ws.call(request, data)  # Make a request with the given data

async def connect():
    await ws.connect()  # Make the connection to OBS-Websocket


async def disconnect():
    await ws.disconnect()


def main(argv):
    if len(sys.argv) < 2:
        sys.exit()

    requeststring = argv[0]
    datastring = argv[1]

    #sys.stderr.write("arg0 = " + requeststring + "\n")
    #sys.stderr.write("arg1 = " + datastring + "\n")
    jsondata = json.loads(datastring)

    loop.run_until_complete(connect())
    loop.run_until_complete(send_request(requeststring, jsondata))
    loop.run_until_complete(disconnect())

main(sys.argv[1:])
