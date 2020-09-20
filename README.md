
# Quick hack to allow OBS control from [MidiPipe](http://www.subtlesoft.square7.net/MidiPipe.html) / AppleScript

# It's not clean / It's not supported / It's a hack
# but it might be usefull as a starter for others. 

OBS Hotkey support is buggy on macOS and AppleScript key stroking requires app to be in focus. OBS Midi plugin is being rewritten and do not support all actions like making sources visible/hidden

This integration is using [OBS-websocket plugins](https://obsproject.com/forum/resources/obs-websocket-remote-control-obs-studio-from-websockets.466/) and [simpleobsws python library](https://github.com/IRLToolkit/simpleobsws)

My trick:

Make a groupe named "MIDI_{channel}_{Data1}_{Data2}" put the sources you wanna act on from AppleScript in it.

in Applescript setup a datastring according to the [obs-websocket protoco]l(https://github.com/Palakis/obs-websocket/blob/4.x-current/docs/generated/protocol.md#getscenelist)

and invoke obs_midi-obsws.py <Request> <datatring>

python will parse all scene with sources named "MIDI_*" and will send the request to them.

### last minute: There's is a bug in obs-websockets that prevent item visibility to be updated if they are not part of the active scene....

AppleScript code ex:

```
property fromChannel : 1
property toChannel : 12

on runme(message)

set data1 to item 1 of message
set data2 to item 2 of message
if item 3 of message > 0 
	set datastring to "'{\"source\": \"MIDI_1_"& data1 & "_" & data2 & "\", \"render\": true}'"
end if

if item 3 of message = 0 
	set datastring to "'{\"source\": \"MIDI_1_"& data1 & "_" & data2 & "\", \"render\": false}'"
end if
do shell script "~/.pyenv/shims/python3 ~/obs-midi-obsws/obs_midi-obsws.py SetSceneItemRender " & datastring

end runme
```








