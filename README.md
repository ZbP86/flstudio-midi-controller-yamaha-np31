# FL Studio MIDI controller script for Yamaha Piaggero NP-31

## Installation

### Windows

* Create Folder: ``{user-folder}\Documents\Image-Line\Data\FL Studio\Settings\Hardware\Yamaha NP-31``
* Copy ``_device_Yamaha NP-31 QOL.py`` into newly created folder
* In FL Studio - ``Options > MIDI Settings -> MIDI -> Input -> Controller Type`` select ``Yamaha NP-31 QOL (user)``

## Usage

Pressing variation button (or any program button) switches betwen 2 modes

### default mode ### 

Only program switch buttons are remaped as script mode switches.

### control mode ###

Selected note keys are mapped as follows:

* E0 -> previous plugin preset
* F0 -> next plugin preset
* F6 -> previous channel
* G6 -> next channel
* F#6 -> open / close channel plugin
