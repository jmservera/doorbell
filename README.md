# Doorbell

A raspi hack for the golmar video doorbell.

Work In Progress
---

These are some hacks for the [Golmar Tekna Plus SE][teknaplusse] video-doorbell that allow you to stream the video to HomeAssistant via rtsp and interact with the door when someone rings the bell.

The Video Stream folder contains a script to capture the video using an EasyCap dongle connected to a Rpi2 and the controller will get the doorbell signal and notify the HomeAssistant via mqtt.


TO-DO
---

* Add EasyCap and ffmpeg instructions, based on: https://www.arrow.com/en/research-and-events/articles/pi-bandwidth-with-video
* Use the https://github.com/aler9/rtsp-simple-server release for the installer
* Add wiring schemas for the Tekna Plus
* Add circuit design for GPIO
* Create BOM:
  * Raspberry Pi 2 or superior
  * EasyCap
  * 1K&Omega; and 220&Omega; Resistors, 1&micro;F capacitor and 1N4148 diode, similar to this circuit
    [![CircuitLab Schematic 8683944b6u3b](https://www.circuitlab.com/circuit/8683944b6u3b/screenshot/540x405/)](https://www.circuitlab.com/circuit/8683944b6u3b/stackexchange-2019-11-10-14_48_56/)
  * Relay for open door signal


[teknaplusse]: https://www.golmar.es/productos/monitor-color-con-pantalla-de-3,5-tekna-plus-se
