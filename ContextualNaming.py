import os
import shutil
from datetime import datetime
from PIL import Image
from transformers import pipeline

def copy_folder_with_timestamp(input_folder):
    """Copy the input folder to a new folder with a timestamped name."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_folder = f"Context_{timestamp}"
    shutil.copytree(input_folder, new_folder)
    return new_folder

def describe_and_rename_images(folder):
    """Describe images in the folder and rename them based on the description."""
    image_captioner = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
    serial_number = 1

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        try:
            # Open the image and generate a description
            with Image.open(file_path) as img:
                description = image_captioner(img)[0]['generated_text']
            
            # Create a short, sanitized name
            short_name = "_".join(description.split()[:3]).replace(" ", "_").replace("/", "_")
            new_filename = f"{short_name}_{serial_number}.png"
            new_file_path = os.path.join(folder, new_filename)

            # Save the image with the new name
            img.save(new_file_path, format="PNG")
            os.remove(file_path)  # Remove the old file
            serial_number += 1

        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    input_folder = "OutputCells_Exp1_Correct"  # Replace with your input folder path
    new_folder = copy_folder_with_timestamp(input_folder)
    describe_and_rename_images(new_folder)