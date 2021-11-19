# AutoInterrogate
An attempt to automate gameplay of the Android game [	
Indefinite: Interrogation Game](https://play.google.com/store/apps/details?id=air.me.brandlibel.indefinite)

## adb
Using the [adb](https://developer.android.com/studio/command-line/adb) cli tool for the following functions:
- Capture screenshots on the target device.
- Pull screenshots from the target device.
- Issue INPUT commands (taps) to the target device.
> Wireless ADB can be set up following instructions [here](https://developer.android.com/studio/command-line/adb#connect-to-a-device-over-wi-fi-android-11+)

## Pillow
Using the wonderful Python [Pillow](https://pypi.org/project/Pillow/) library for:
- Cropping images to get them ready to parse text

## pytesseract
[This OCR tool](https://pypi.org/project/pytesseract/) is being used to read (parse) the text off the cropped images.

## nltk
Just getting started with [nltk](https://www.nltk.org/), so it is seeming a bit overwhelming for now. Using this to tokenize the parsed text.

> Pixel coordinate values are currently hardcoded to a [Samsung Galaxy Note 10+](https://www.samsung.com/in/smartphones/galaxy-note10/). Should work for devices with similar displays.