# name=Yamaha NP-31 QOL
# receiveFrom=Yamaha Piaggero NP-31

"""
[[
	Surface:	Yamaha Piaggero NP-31
	Developer:	Zenithies ZbP86
	Version:	Beta 0.1
]]
"""

import channels
import device
import midi
import plugins
import ui

class YamahaPiaggeroNP31QOL:
    MODE_NONE=0
    MODE_CHANNEL_CONTROLS=1
    MODE_PRESET_CONTROLS=2
    MODE_CONTROL=3

    KEY_ACTION_NEXT_CHANNEL=103
    KEY_ACTION_PREVIOUS_CHANNEL=101
    KEY_ACTION_OPEN_EDITOR=102

    KEY_ACTION_NEXT_PRESET=29
    KEY_ACTION_PREVIOUS_PRESET=28

    KEY_MODE_SWITCH_0=0
    KEY_MODE_SWITCH_1=5
    KEY_MODE_SWITCH_2=19
    KEY_MODE_SWITCH_3=48
    KEY_MODE_SWITCH_4=6

    EVENT_NOTE_ON=0x90
    EVENT_NOTE_OFF=0x91

    def __init__(self):
        self.mode=self.MODE_NONE

    def getActionKeys(self):
        return [
            self.KEY_ACTION_NEXT_CHANNEL,
            self.KEY_ACTION_PREVIOUS_CHANNEL,
            self.KEY_ACTION_OPEN_EDITOR,
            self.KEY_ACTION_PREVIOUS_PRESET,
            self.KEY_ACTION_NEXT_PRESET
        ]

    def channelSelect(self, move, event):
        nextSelection = channels.selectedChannel() + move
        if (nextSelection >= channels.channelCount()):
            nextSelection = 0
        if (nextSelection < 0):
            nextSelection = channels.channelCount() - 1
        print("about to select channel: ", nextSelection)
        channels.selectOneChannel(nextSelection)
        event.handled = True

    #def reset(self, event):
     #   device.midiOutMsg(0xC0, event.midiChan, 0x06, 0x00)
     #   device.midiOutMsg(0xC0, event.midiChan, 0x00, 0x06)
     #   device.midiOutMsg(0xC006)
     #   device.midiOutMsg(0xB7, event.midiChan, 0x5B, 0x33)
     #   device.midiOutMsg(0xC0, event.midiChan, 0x06, 0x00)

    def switchMode(self, event):
        event.handled = True
        if self.mode == self.MODE_NONE:
            self.mode = self.MODE_CONTROL
        else:
            self.mode = self.MODE_NONE

    def OnMidiIn(self, event):
        if self.mode == self.MODE_NONE:
            return

        event.handled = False

        if event.status == self.EVENT_NOTE_ON and event.velocity > 0:
            event.handled = True
            if event.note == self.KEY_ACTION_PREVIOUS_CHANNEL:
                self.channelSelect(-1, event)
            elif event.note == self.KEY_ACTION_NEXT_CHANNEL:
                self.channelSelect(1, event)
            elif event.note == self.KEY_ACTION_OPEN_EDITOR:
                channels.showEditor(channels.selectedChannel())
            elif event.note == self.KEY_ACTION_PREVIOUS_PRESET:
                plugins.prevPreset(channels.selectedChannel())
            elif event.note == self.KEY_ACTION_NEXT_PRESET:
                plugins.nextPreset(channels.selectedChannel())
            else:
                event.handled = False

        if event.status == self.EVENT_NOTE_OFF and event.note in self.getActionKeys(): #prevent sounds on action key release
            event.handled = True

    def OnMidiMsg(self, event):
        if event.midiId == midi.MIDI_PROGRAMCHANGE:
            self.switchMode(event) #code is in event.data1

    def dump(self, obj):
        for attr in dir(obj):
            print("obj.%s = %r" % (attr, getattr(obj, attr)))

# Instantiate and hook handling
_YamahaPiaggeroNP31QOL = YamahaPiaggeroNP31QOL()

def OnMidiIn(event):
    _YamahaPiaggeroNP31QOL.OnMidiIn(event)

def OnMidiMsg(event):
    _YamahaPiaggeroNP31QOL.OnMidiMsg(event)