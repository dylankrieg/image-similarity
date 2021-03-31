# installing scikit-image
# python3 -m pip install -U scikit-image

# scikit-image support
# Windows 64-bit on x86 processors
# Mac OS X on x86 processors
# Linux 64-bit on x86 processors

# installing natsort
# python3 -m pip install -U natsort

# https://scikit-image.org/docs/dev/api/skimage.metrics.html?highlight=structural_similarity#skimage.metrics.structural_similarity
# https://scikit-image.org/docs/stable/auto_examples/transform/plot_ssim.html?highlight=structural_similarity

# natsort docs (https://pypi.org/project/natsort/)
# sci-kit image docs (https://scikit-image.org/docs/stable/)

import os
import shutil
from natsort import natsorted
from skimage import io
from skimage.metrics import structural_similarity as ssim

# returns a list of image file names with similarity > similarityThreshold
def getSimilarImages(imageNames,npImages,similarityThreshold):
	similarImages=[]
	if(len(imageNames)<2):
		return []
	for i in range(0,len(npImages)-1):
		frame1=npImages[i]
		frame2=npImages[i+1]
		imageSSIM=ssim(frame1,frame2,multichannel=True)
		print(str(imageNames[i+1]) + str(imageSSIM))
		if(imageSSIM > similarityThreshold):
			similarImages.append(imageNames[i+1])
	return similarImages

def getImages(dirPath):
	imageNames=[]
	for fileName in os.listdir(dirPath):
		if fileName.endswith(".jpg") or fileName.endswith(".png"):	
			imageNames.append(fileName)

	imageNames=natsorted(imageNames)
	npImages=[]
	for imageName in imageNames:
		imagePath=os.path.join(dirPath,imageName)
		npImages.append(io.imread(imagePath))

	return imageNames,npImages


# deletes or movesadjacent images with structural similarity > similarityThreshold
# if deleteImages=False then the still images are moved into a directory stillImages
# dirPath is the path from the script location to the directory of images
def removeStillImages(dirPath,deleteImages):
	stillImageDir="./stillImages"
	if(deleteImages==False):
		if(os.path.isdir(stillImageDir)==False):
			os.mkdir(stillImageDir)

	# similarityThreshold can be decreased to increase the sensitivity
	# between 0.92 - 0.975 is a good range
	similarityThreshold=0.975
	imageNames,npImages=getImages(dirPath)

	similarImages=getSimilarImages(imageNames,npImages,similarityThreshold)
	
	imagesRemoved=0
	# remove or move simlar images
	for imageName in similarImages:
		imagePath=os.path.join(dirPath,imageName)
		if(deleteImages==False):
			shutil.move(imagePath,stillImageDir)
		else:
			os.remove(imagePath)
		imagesRemoved+=1

	print(imagesRemoved + " images removed")


def main():
	similarityThreshold=0.975
	print("fast moving subset 1")
	movingSubset1Path='./test_data/moving_subset_1_large_full'
	movingSub1Names,movingSub1Images=getImages(movingSubset1Path)
	getSimilarImages(movingSub1Names,movingSub1Images,similarityThreshold)
	
	print("still subset 1")
	stillSubset1Path='./test_data/still_subset_1_full'
	stillSub1Names,stillSub1Images=getImages(stillSubset1Path)
	getSimilarImages(stillSub1Names,stillSub1Images,similarityThreshold)
	
	print("medium moving subset 2")
	movingSubset2Path='./test_data/moving_subset_2_medium_full'
	movingSub2Names,movingSub2Images=getImages(movingSubset2Path)
	getSimilarImages(movingSub2Names,movingSub2Images,similarityThreshold)
	
	print("continuous subset")
	contSubset2Path='./test_data/cont_subset_2_small_full'
	contSubset2Names,contSubset2Images=getImages(contSubset2Path)
	getSimilarImages(contSubset2Names,contSubset2Images,similarityThreshold)
	



	
if __name__=='__main__':
    main()


