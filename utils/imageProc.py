import matplotlib.image as mpimg
import os
import numpy



def setWhiteAsTrans(imagePath):
    img = mpimg.imread(imagePath)
    for i in range(len(img)-1):
        for j in range(len(img[0]) - 1):
            if img[i][j][0] > 0.95 and img[i][j][1] > 0.95 and img[i][j][2] > 0.95:
                img[i][j][3] = 0
    outputPath = imagePath[0:-4] + "Transparent.png"
    mpimg.imsave(outputPath,img)


def createBoundaryImg(imagePath):
    img = mpimg.imread(imagePath)
    img2 = numpy.zeros((len(img),len(img[0]),4))
    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i][j][3] > 0:
                img2[i][j][0] = 0 # occupied
            else:
                img2[i][j][0] = 1 # free

    outputPath = imagePath[0:-4] + "Boundaries.png"
    mpimg.imsave(outputPath, img2)


if __name__ == '__main__':
    curDirectory = os.getcwd()
    assetsPath = curDirectory.replace("utils", "assets")
    imageName = "submarineLayout1.png"
    imagePath = os.path.join(assetsPath,imageName)

    # set all white pixel to transparent
    setWhiteAsTrans(imagePath)



    imageNameTrans = "submarineLayout1Transparent.png"
    imagePathTrans = os.path.join(assetsPath,imageNameTrans)
    # create boundaries based on transparency
    createBoundaryImg(imagePathTrans)
    print("Done")