# name=Yamaha NP-31 QOL
# receiveFrom=Yamaha Piaggero NP-31

"""
[[
	Surface:	Yamaha Piaggero NP-31
	Developer:	ZbP86
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
    MODE_CONTROL=1

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

    BANK_DEFAULT=0x7A

    PROGRAMME_01 = 0x007A # piano 1
    PROGRAMME_02 = 0x0070 # piano 2
    PROGRAMME_03 = 0x057A # e-piano 1
    PROGRAMME_04 = 0x047A # e-piano 2
    PROGRAMME_05 = 0x137B # organ 1
    PROGRAMME_06 = 0x137A # organ 2
    PROGRAMME_07 = 0x307A # strings
    PROGRAMME_08 = 0x0B7A # vibes
    PROGRAMME_09 = 0x067A # harpischord 1
    PROGRAMME_10 = 0x067B # harpischord 2

    COMMAND_BANK_SELECT_LSB=0x20

    def __init__(self):
        self.bank=self.BANK_DEFAULT
        self.mode=self.MODE_NONE
        self.actionKeys = self.extractActionKeys()

    # Picks all constants starting with KEY_ACTION_ prefix
    def extractActionKeys(self):
        actionKeys = []
        for attr in dir(self):
            if attr.startswith('KEY_ACTION_'):
                actionKeys.append(getattr(self, attr))
        return actionKeys

    def channelSelect(self, move, event):
        nextSelection = channels.selectedChannel() + move
        if (nextSelection >= channels.channelCount()):
            nextSelection = 0
        if (nextSelection < 0):
            nextSelection = channels.channelCount() - 1
        print("about to select channel: ", nextSelection)
        channels.selectOneChannel(nextSelection)
        event.handled = True

    def bankSelect(self, event):
        self.bank = event.data2
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

        if event.status == self.EVENT_NOTE_OFF and event.note in self.actionKeys: #prevent sounds on action key release
            event.handled = True

    def OnMidiMsg(self, event):
        if event.midiId == midi.MIDI_PROGRAMCHANGE:
            mask = self.bank + (event.progNum << 8)

            if mask == self.PROGRAMME_01 or mask == self.PROGRAMME_02:
                self.switchMode(event) #code is in event.data1
            elif mask == self.PROGRAMME_03:
                print('el. piano 1', mask)
            elif mask == self.PROGRAMME_04:
                print('el. piano 2', mask)
            elif mask == self.PROGRAMME_05:
                print('organ 1', mask)
            elif mask == self.PROGRAMME_06:
                print('organ 2', mask)
            elif mask == self.PROGRAMME_07:
                print('strings', mask)
            elif mask == self.PROGRAMME_08:
                print('vibes', mask)
            elif mask == self.PROGRAMME_09:
                print('harpischord 1', mask)
            elif mask == self.PROGRAMME_10:
                print('harpischord 2', mask)
            else:
                print('unknown: ', mask)
        elif event.midiId == midi.MIDI_CONTROLCHANGE and event.data1 == self.COMMAND_BANK_SELECT_LSB:
            self.bankSelect(event)


    def dump(self, obj):
        for attr in dir(obj):
            print("obj.%s = %r" % (attr, getattr(obj, attr)))

# Instantiate and hook handling
_YamahaPiaggeroNP31QOL = YamahaPiaggeroNP31QOL()

def OnMidiIn(event):
    _YamahaPiaggeroNP31QOL.OnMidiIn(event)

def OnMidiMsg(event):
    _YamahaPiaggeroNP31QOL.OnMidiMsg(event)