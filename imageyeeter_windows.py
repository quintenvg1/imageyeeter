import os
import cv2

kernel = (5, 5) #for pictures between 900p and 1080p
print("imageyeeter windows version")
usbdevice = input("gebruik je een usb stick met een pictures directory? Y/N")
if(usbdevice == "y"):
    devicename = input("what's the driveletter of your usb device? : ")
    workingdirectory = devicename+":/pictures/"


manual_entry = input("enter a working directory manually? y/n")
if(manual_entry == "y"):
    print("do not forget the / at the end of your foldername. ex: name/pictures/")
    workingdirectory = input("directory: ")
print("current working directory = " + workingdirectory)

threshhold = 60 #value between 0 and 500 the lower the value the less sharp pictures can be before being deleted default 60
override_treshhold = input("override treshhold? default = 60 y/n ")
if(override_treshhold == "y"):
    threshhold = int(input("give a threshhold value between 0 and 500 default = 60. \r\n lower values = more kept but less sharper pictures, higher values = less kept but sharper pictures \r\n"))


#amount of unsharp and sharp images
unsharp = 0
sharp = 0
#allow to delete images
deleteimages = False


#ask if i can remove the images from the usb device
answer = input("can i delete the images if they're blurry? y/n \r\n" )
if(answer == "y"):
    deleteimages = True
    print("deleting the unsharp images")
else:
    print("blurry images will not yet be deleted")



images = os.listdir(workingdirectory)



def variance_of_laplacian(image):
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
    return cv2.Laplacian(image, cv2.CV_64F).var()

for item in images:
    try:
        print("---------------------------------")
        print("now working with " + str(item))
        image = cv2.imread(workingdirectory + item)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
        blur = variance_of_laplacian(blackhat)
        print(blur)
        if(blur < threshhold):
            print(str(item) + " will be deleted!")
            unsharp = unsharp + 1
            if(deleteimages == True):
                os.remove(workingdirectory + item)
        else:
            print(str(item) + " image is sharp and will be kept.")
            sharp = sharp + 1
            
        if(False): #show the images
            cv2.imshow("picture", image)
            cv2.waitKey(1)
    except:
        print("this file is not supported")

print("the program found " + str(unsharp) + " blurry images and found " + str(sharp) +" sharp images")
print("if you want to delete these images run the program again but press y on deletion prompt")

exit = input("press enter to exit")
