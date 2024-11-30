import os
import cv2
import matplotlib.pyplot as plt

# Define the path to the dataset
dataset_path = 'dataset/Closed_Eyes'

# List all files in the dataset directory
image_files = os.listdir(dataset_path)

# Access the first image in the dataset
first_image_path = os.path.join(dataset_path, image_files[0])

# Read the image using OpenCV
image = cv2.imread(first_image_path)

print(image.shape)

# Convert the image from BGR to RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Display the image using matplotlib
plt.imshow(image_rgb)
plt.title('First Image in Closed_Eyes Dataset')
plt.axis('off')  # Hide the axis
plt.show()