import h5py
import numpy as np
import os
import SimpleITK as itk


# Replace these with your actual file paths
DATA_ROOT = r"../c_elegans"
RAW_FOLDER = "imagesAsMhdRawAligned"
LABEL_FOLDER = "groundTruthLabelsAligned"
TRAIN_FOLDER = "train"
VAL_FOLDER = "val"
train_count = 27


'''
This function reads a '.mhd' file using SimpleITK and returns the image array, origin and spacing of the image.
The '.mhd' file needs to be in the same directory as the corresponding '.raw' file.
Note that the array has the x and z coordinate flipped, so you want to acces array[z,y,x].
'''
def load_itk(filename):
    # Reads the image using SimpleITK
    itkimage = itk.ReadImage(filename)

    # Convert the image to a  numpy array first and then shuffle the dimensions to get axis in the order z,y,x
    array = itk.GetArrayFromImage(itkimage)
    # NOTE: Unclear yet if transpose is needed as UNet seems to process (z,y,x) coordinates. - ck
    array = np.transpose(array, (2, 1, 0))  # Change the order of dimensions

    # Read the origin of the ct_scan, will be used to convert the coordinates from world to voxel and vice versa.
    origin = np.array(list(reversed(itkimage.GetOrigin())))

    # Read the spacing along each dimension
    spacing = np.array(list(reversed(itkimage.GetSpacing())))
    return array, origin, spacing


raw_path = os.path.join(DATA_ROOT, RAW_FOLDER)
label_path = os.path.join(DATA_ROOT, LABEL_FOLDER)
train_path = os.path.join(DATA_ROOT, TRAIN_FOLDER)
val_path = os.path.join(DATA_ROOT, VAL_FOLDER)

file_count = 0
# Loop through all files in raw_source
for label_file_name in os.listdir(label_path):
    if label_file_name.endswith(".mhd"):
        worm_name = label_file_name.split("-")[0]
        raw_file_name = f"{worm_name}.mhd"

        raw_data, _, _ = load_itk(os.path.join(raw_path, raw_file_name))
        label_data, _, _ = load_itk(os.path.join(label_path, label_file_name))

        output_path = train_path if file_count < train_count else val_path
        output_file = os.path.join(output_path, f"{worm_name}.h5")
        # Create an HDF5 file and save the NumPy array
        with h5py.File(output_file, 'w') as hf:
            hf.create_dataset('raw', data=raw_data)
            hf.create_dataset('label', data=label_data)
        file_count += 1
        print(f'Data has been successfully converted to {output_file}.')

