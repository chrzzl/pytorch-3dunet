import os
import SimpleITK as sitk
import tifffile

def convert_mhd_to_tiff(input_folder, output_folder):
    # Iterate through MHD files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.mhd'):
            file_path = os.path.join(input_folder, filename)

            # get first part of filename before first -
            worm_name = os.path.splitext(filename)[0].split('-')[0]

            # Read MHD file
            image = sitk.ReadImage(file_path)

            # Convert to NumPy array
            image_array = sitk.GetArrayFromImage(image)

            # Save as TIFF
            output_path = os.path.join(output_folder_path, f'{worm_name}.tif')
            tifffile.imwrite(output_path, image_array)

            print(f"Converted {filename} to TIFF: {output_path}")

# Example usage
input_folder_path = r"C:\Users\ckarg\Documents\Datasets\c_elegans\mhd_raw\label_gt" # label_gt also
output_folder_path = r"C:\Users\ckarg\Documents\Datasets\c_elegans\tiff\train\masks" # label_gt also

convert_mhd_to_tiff(input_folder_path, output_folder_path)
