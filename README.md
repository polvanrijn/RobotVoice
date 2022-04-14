# RobotVoice
_Verified Set of TTS Voices for Common Robots_


## Installation
Setup a virtual environment and install the dependencies:
```shell
pip install opencv-python
pip install matplotlib
pip install beautifulsoup4
pip install requests
```

## Scraping for robots
To create a json with all meta information from the robots listed at https://robots.ieee.org/robots/, run:
```
python scrape_ieee.py 
```

## Selecting the robots
To select the images for the robots, run the following script. 
```shell
mkdir "images"
python select_robots.py 
```

An array with images will pop up. Either specify the image index (starts at 1!) or reject the image by entering `n`.
