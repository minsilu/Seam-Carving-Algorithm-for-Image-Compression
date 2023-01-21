# Seam Carving Algorithm for Image Compression

## Environment
Language: Python
Interpreter: Python 3.10
Python package:
```
argparse=1.4.0
opencv-python=4.5.5.64
numpy=1.22.3
time=1.0.0
```
Please try to install a Python package with a version not lower than the above.

## Input
`-i`: the path of the image \
`-m`: The high compression rate of the image, a floating point number not greater than 1 \
`-n`: image width compression rate, a floating point number not greater than 1 

__Example input__: Open this program in the terminal, and under the absolute path of the folder where the program is located, enter the image path, height compression rate, and width compression rate as follows. After running, the height will be compressed to the original 0.8, and the width will be compressed to original 0.9
```
python seamcarving.py -i example/1.png -m 0.8 -n 0.9
```
If you do not enter the parameter `-m` or `-n`, the default value of these two parameters is 0.5, and the height and width are compressed to the original 0.5
```
python seamcarving.py -i example/1.png
```
Please try to input 3-channel RGB images. In this experiment, the 274*264 png image takes two and a half minutes to run, and the scale of the test image should not be too much larger than this image.

## Output
Take the above input as an example. After inputting the parameters, the program will output on the terminal command line interface:
```
Image read successfully!
Original image size (height, width, channels) = (283, 300, 3)
```
After entering the compression algorithm, the program outputs:
```
Compressing width...
```
```
In compression height...
```
After the compression is completed, output the time-consuming compression process, the size of the compressed image, and the path to save the image
```
Compression process time-consuming: 229.70470280002337 seconds
The size of the compressed image (height, width, channel) = (142, 150, 3)
The image save path is example/1_result.png
```