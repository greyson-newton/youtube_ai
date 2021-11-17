import cv2
import os
import argparse
def main(img_folder, vid_name):
	img2vid(img_folder,vid_name)

def img2vid(img_folder, video_name):
	images = [img for img in os.listdir(img_folder)]
	print(images)
	frame = cv2.imread(os.path.join(img_folder, images[0]))
	height, width, layers = frame.shape

	video = cv2.VideoWriter(video_name, 0, .3, (width,height))

	for image in images:
	    video.write(cv2.imread(os.path.join(img_folder, image)))

	cv2.destroyAllWindows()
	video.release()
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = 'parzen_window')
	parser.add_argument('--imgs',
	    help='enter images to convert')
	parser.add_argument('--out',
	    help='enter output videoname')

	args = parser.parse_args()

	main(args.imgs,args.out)


