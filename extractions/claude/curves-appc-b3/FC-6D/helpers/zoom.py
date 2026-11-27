"""Enlarge a PNG (an overlay crop) by an integer factor for viewing. usage: zoom.py in.png out.png factor"""
import sys
from PIL import Image
im = Image.open(sys.argv[1])
k = int(sys.argv[3])
im.resize((im.width * k, im.height * k), Image.NEAREST).save(sys.argv[2])
