import matplotlib.pyplot as plt
import os
import pydicom

# Function to read a DICOM file
def read_dicom(file_path):
    dicom_data = pydicom.dcmread(file_path)
    # Access the pixel data
    pixel_array = dicom_data.pixel_array
    return dicom_data, pixel_array

# Example of reading and displaying metadata
def show_dicom_metadata(dicom_data):
    print("Patient Name:", dicom_data.PatientName)
    print("Modality:", dicom_data.Modality)
    print("Study Date:", dicom_data.StudyDate)
    print("Image size:", dicom_data.Rows, "x", dicom_data.Columns)

# Function to display a DICOM image using matplotlib
def plot_dicom_image(pixel_array, title="DICOM Image"):
    if len(pixel_array.shape) == 3:
        # If the pixel array is 3D, display the first slice
        pixel_array = pixel_array[0]

    plt.imshow(pixel_array, cmap='gray')
    plt.title(title)
    plt.axis('off')  # Hide the axis
    plt.show()

# Example of reading and plotting a DICOM file
file_path = "C:/Users/lucke/Downloads/dicom_viewer_0004/0003.DCM"
dicom_data, pixel_array = read_dicom(file_path)

# Show metadata and plot the image
show_dicom_metadata(dicom_data)
plot_dicom_image(pixel_array)

# Function to read and plot multiple DICOM files from a directory
def analyze_dicom_directory(directory_path):
    dicom_files = [f for f in os.listdir(directory_path) if f.endswith('.dcm')]

    for dicom_file in dicom_files:
        file_path = os.path.join(directory_path, dicom_file)
        dicom_data, pixel_array = read_dicom(file_path)

        # Display metadata and plot each image
        print(f"\nAnalyzing {dicom_file}...")
        show_dicom_metadata(dicom_data)
        plot_dicom_image(pixel_array, title=f"DICOM: {dicom_file}")

# Usage example
directory_path = "C:/Users/lucke/Downloads/dicom_viewer_0004"
analyze_dicom_directory(directory_path)