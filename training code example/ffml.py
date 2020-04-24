import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, optimizers, datasets, models
import matplotlib.pyplot as plt
import numpy as np
from glob import glob 
from tensorflow.keras.preprocessing import image
import pathlib

AUTOTUNE = tf.data.experimental.AUTOTUNE
IMG_WIDTH = 32
IMG_HEIGHT = 32

train_root_folder = 'c:\\temp\\ffml_dataset-master\\images\\'
	  
def get_labels():
	for (root,dirs,files) in os.walk(train_root_folder):
		return dirs
	#return class_labels

def get_num_files(labels):
	num_files = 0
	for folder in labels:
		#print(train_root_folder + folder)
		for (root, dirs, files) in os.walk(train_root_folder + folder + '/'):
			num_files += len(files)
	return num_files
	

	
data_dir = pathlib.Path(train_root_folder)
CLASS_NAMES = np.array([item.name for item in data_dir.glob('*')])

def decode_img(img):
	# convert the compressed string to a 3D uint8 tensor
	img = tf.image.decode_jpeg(img, channels = 3)
	img = tf.image.rgb_to_grayscale(img)
	# Use `convert_image_dtype` to convert to floats in the [0,1] range.
	img = tf.image.convert_image_dtype(img, tf.float32)
	img = tf.image.resize(img, [IMG_WIDTH, IMG_HEIGHT]) 
	img = tf.reshape(img, [IMG_WIDTH, IMG_HEIGHT])
	return img
  
def get_label(file_path):
	# convert the path to a list of path components
	parts = tf.strings.split(file_path, os.path.sep)
	# The second to last is the class-directory
	#print(parts)
	label_index = np.where(parts[-2] == CLASS_NAMES)[0][0]
	return label_index 
  
def process_path(file_path):
	label_index = get_label(file_path)
	# load the raw data from the file as a string
	img = tf.io.read_file(file_path)
	img = decode_img(img)
	return img, label_index
	
def get_training_test(labels):
	train_images = []
	train_labels = []
	test_images = []
	test_labels = []
	
	num_training = 0
	num_test = 0

	num_files = 0
	for folder in labels:
		#print(train_root_folder + folder)
		for (root, dirs, files) in os.walk(train_root_folder + folder + '\\'):
			#print(files)
			i = 0
			for file in files:
				image, label = process_path(train_root_folder + folder + str('\\') + file)
				if i < 2:
					train_images.append(image)
					train_labels.append(label)
					num_training += 1
					i += 1
				else:
					test_images.append(image)
					test_labels.append(label)
					num_test += 1
			
	return num_training, num_test, train_images, train_labels, test_images, test_labels
		
def main():
	os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # or any {'0', '1', '2'}

	labels_as_string = get_labels()
	num_classes = len(labels_as_string)
	print("num_classes = ", num_classes)
	num_training_data = get_num_files(labels_as_string)
	print('num num_training_data=' + str(num_training_data))

	#list_ds = tf.data.Dataset.list_files(str(train_root_folder + '*/*'))
	
	num_training, num_test, train_images, train_labels, test_images, test_labels = get_training_test(labels_as_string)
	print("num_training = ", num_training)
	print("num_test=", num_test)
	
	"""
	images = []
	labels = []
	for f in list_ds:
#		print(f)
		image, label = process_path(f)
#		print("Image shape: ", image.shape )
#		print("Label: ", label.shape)
		images.append(image)
		labels.append(label)
	"""
	train_images = np.array(train_images)
	train_labels = np.array(train_labels)
	train_images = train_images.reshape(num_training,IMG_WIDTH,IMG_HEIGHT,1)	

	test_images = np.array(test_images)
	test_labels = np.array(test_labels)
	test_images = test_images.reshape(num_test,IMG_WIDTH,IMG_HEIGHT,1)	
	
	#print(train_labels)
	#print(train_labels.shape)
	train_labels = tf.one_hot(train_labels, depth = num_classes)
	test_labels = tf.one_hot(test_labels, depth = num_classes)
	#print(train_images.shape)
	#print(train_labels.shape)
	print("done creating array")
	
	
	ds_train = tf.data.Dataset.from_tensor_slices((train_images, train_labels))
	ds_train = ds_train.shuffle(num_training).batch(100)
		
	#ds_test = tf.data.Dataset.from_tensor_slices((test_images, test_labels))

	model = models.Sequential()
	model.add(layers.Conv2D(32, (3, 3), activation='relu', 
			input_shape=(IMG_WIDTH, IMG_WIDTH, 1)))
	model.add(layers.MaxPooling2D((2, 2)))
	model.add(layers.Conv2D(64, (3, 3), activation='relu'))
	model.add(layers.MaxPooling2D((2, 2)))
	model.add(layers.Conv2D(64, (3, 3), activation='relu'))
	model.add(layers.Flatten())
	model.add(layers.Dense(64, activation='relu'))
	model.add(layers.Dense(num_classes))

	model.summary()
		
	model.compile(optimizer=optimizers.Adam(0.001),
				loss=tf.losses.CategoricalCrossentropy(from_logits=True),
				metrics=['accuracy'])

	model.fit(ds_train.repeat(), epochs = 3, steps_per_epoch = 500)
	print("training done")
	model.evaluate(test_images, test_labels)
	
if __name__ == '__main__':
	main()