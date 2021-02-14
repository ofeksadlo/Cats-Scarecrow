# Cats-Scarecrow
![showcase](showcase.gif)</br>
Scare away your cats from your sofa.</br>
[yolov3.weights](https://pjreddie.com/media/files/yolov3.weights)

# Requirements
1) [OpenCV](https://pypi.org/project/opencv-python/)
2) [Numpy](https://pypi.org/project/numpy/)

# How to make it work
1) Download the [model](https://pjreddie.com/media/files/yolov3.weights) and put it in the repository folder you downloaded.
2) Your VLC installed folder path needs to be added to the [environment path](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/).</br>
Because that way we can launch the sound easily with cmd.
3) Make sure your sofa is in the camera frame and launch main.py
4) Select the Range Of Intrest (ROI) in the frame and press enter.

Now when a cat is in the ROI the sound will launch after it's done it will close.</br>
And keep looking for cats in the ROI.

You'll notice the frame rate is quite slow. The reason is</br>
we favor accuracy in this problem rather than efficence.</br>
So we used a rather slow model.</br></br>
You can use whatever sound you want just name it Sound.mp3

Developed in [Python 3.7.7](https://www.python.org/ftp/python/3.7.7/python-3.7.7-amd64.exe)
