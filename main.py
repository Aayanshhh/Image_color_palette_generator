import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex
import tkinter as tk
from tkinter import filedialog, simpledialog

def generate_palette(image_path, num_colors=5):
    # Read the image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB

    # Reshape the image to be a list of pixels
    pixels = image.reshape((-1, 3))

    # Apply k-means clustering
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)

    # Get the cluster centers and convert them to integer
    colors = np.array(kmeans.cluster_centers_, dtype=int)

    # Display the original image
    plt.figure(figsize=(14, 7))

    plt.subplot(1, 2, 1)
    plt.imshow(image)
    plt.title('Original Image')
    plt.axis('off')

    # Create and display the color palette
    palette = np.zeros((50, 50 * num_colors, 3), dtype=int)
    for i, color in enumerate(colors):
        palette[:, i * 50:(i + 1) * 50, :] = color

    plt.subplot(1, 2, 2)
    plt.imshow(palette)
    plt.title('Color Palette')
    plt.axis('off')

    # Display RGB values
    for i, color in enumerate(colors):
        plt.text(i * 50 + 25, 60, to_hex(color/255), ha='center', va='center', fontsize=12, color='black')

    plt.tight_layout()
    plt.show()

    # Save palette option
    save_option = simpledialog.askstring("Save Palette", "Do you want to save the palette image? (yes/no)").lower()
    if save_option == 'yes':
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if save_path:
            cv2.imwrite(save_path, cv2.cvtColor(palette, cv2.COLOR_RGB2BGR))

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Ask for the image file path
    image_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")])
    if not image_path:
        return

    # Ask for the number of colors
    num_colors = simpledialog.askinteger("Number of Colors", "Enter the number of colors for the palette:", minvalue=1, maxvalue=20, initialvalue=5)
    if not num_colors:
        return

    generate_palette(image_path, num_colors)

if __name__ == "__main__":
    main()
