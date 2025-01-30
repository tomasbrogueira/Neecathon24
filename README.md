**This project was done in the context of a 30-hour hackathon (NEECATHON 2025).**


The project consists of a computer vision model applied to a live video feed to detect sleepiness connected to various alarms through the use of a microcontroller.

The datasets used for training the computer vision models are in the neecathon24-datasets repository, which is private for privacy purposes. These datasets consist of the MRL eye dataset and a custom dataset created during the competition, made up of 150 pictures of different people present in the competition itself.

The implementation is made for live video from a PC but can be easily adapted for a camera. For use, run computervision.py on one pc and main.py on another and connect the PC running main.py to a microcontroller with the proper capabilities to emit the alarms.
