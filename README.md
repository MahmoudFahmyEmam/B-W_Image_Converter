# B&W_Image_Converter

This Python script converts colored images to black and white (binary) images using various thresholding methods. It also provides options to invert colors and optimize image size.

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Method Descriptions](#method-descriptions)
   - [Thresholding Methods](#thresholding-methods)
   - [Image Inversion](#image-inversion)
   - [Automatic Resizing](#automatic-resizing)
6. [File Naming Convention](#file-naming-convention)
7. [Example](#example)
8. [Contributing](#contributing)
9. [License](#license)

## Features

- **Image Conversion**: Converts color images to black and white using:
  - Fixed Threshold
  - Otsu's Method
  - Adaptive Thresholding
- **Color Inversion**: Option to invert colors before or after conversion.
- **Automatic Resizing**: Resize images based on unique pixel value analysis.
- **User-Friendly Interface**: Interactive command-line interface for selecting options.

## Requirements

- Python 3.x
- Pillow library (for image processing)
- NumPy (for numerical operations)
- OpenCV (for advanced image processing)

## Installation
1. Download the executable file `image_converter.exe` from the releases section.
2. (Optional) If you want to run the source code directly, clone the repository or download the source code files and install the required libraries:

   pip install Pillow numpy opencv-python


## Usage
1. Run the Script: Execute the script in your terminal.
    - python B&W_Image_Converter.py
    - Select an Action: The program will prompt you to choose whether to proceed with the conversion or exit the program.

    - Input Image Path: Enter the file path of the image you want to convert. The program will validate if the path is correct and if the file is a valid image format (JPEG, PNG, BMP, GIF).

    - Choose Thresholding Method: You will be presented with three options for thresholding methods:

        - Fixed Threshold: Allows you to manually set a threshold value.
        - Otsu's Method: Automatically calculates the optimal threshold value based on the histogram of the image.

        - Adaptive Thresholding: Computes the threshold for smaller regions, allowing for varying lighting conditions.

    - Invert Colors: After converting the image to black and white, you can choose to invert the colors. This can be done either before or after the conversion process.

    - Image Optimization: You can choose to optimize the image size before saving by selecting automatic or variable scaling options based on the unique pixel values.

    - Save the Output: The program will save the processed image in the same directory as the input image, with a filename reflecting the chosen methods and options.

 2. Run the executable:
    - Double-click the image_converter.exe file or run it from the command line:
        path\to\B&W_Image_Converter.exe
    


    - Follow the prompts to:

        - Choose a thresholding method.
        - Specify the image file path.
        - Decide if you want to optimize the image size.
        - Choose to invert colors if applicable.
    - The converted image will be saved in the same directory as the input image with the appropriate filename indicating the processing method and inversion status.

## Method Descriptions
- Thresholding Methods
    - Fixed Thresholding:

        - The user specifies a threshold value. Pixels with intensity values above this threshold are set to white (255), while those below are set to black (0).

        - Use Case: Simple images where foreground and background can be easily distinguished.
    - Otsu's Method:

        - This is a histogram-based method that automatically calculates the optimal threshold to minimize the intra-class variance. It works by maximizing the variance between two classes (foreground and background).

        - Technical Detail: The algorithm evaluates all possible thresholds, computing the variance for each, and selects the threshold that results in the best separation.
    - Adaptive Thresholding:

        - This method calculates thresholds for smaller regions of the image, allowing for better results in varying lighting conditions.

        - Technical Detail: It computes the threshold for each pixel based on the average of the pixel values in a defined neighborhood area, adjusted with a constant value.
- Image Inversion
    - Color Inversion: The program can invert colors in both color (RGB) and grayscale (L) images.
    - Technical Detail: Inversion is performed using the ImageOps.invert() function from the Pillow library, which flips the color values (0 becomes 255, and 255 becomes 0) for each pixel.
- Automatic Resizing
    - The resizing is based on the analysis of unique pixel values in the grayscale image.
    - Technical Detail:
        - If the number of unique pixel values is low (less than 10), the image is aggressively downsampled (scale factor of 4).
        
        - If there are moderate unique values (between 10 and 50), the scale factor is set to 2.
        - If there are many unique values (greater than 50), the original size is maintained.
    - This is done to reduce the file size while preserving as much detail as possible based on the image's complexity.
## File Naming Convention
- The output file will be named based on the selected thresholding method and whether the colors were inverted. For example:

    - black_and_white_using_otsu_method_optimized_with_auto_scale_factor_of_2_image.png
    - black_and_white_using_fixed_threshold_inverted_image.png
## Example
- Run the script and follow the prompts.
- When asked for the image path, provide a valid image file path (e.g., path/to/image.jpg).
- Choose the desired thresholding method.
- Decide if you want to invert the colors after conversion.
- The output will be saved in the same directory.

## Contributing
- If you would like to contribute to this project, feel free to submit a pull request or report issues. - Improvements and feature requests are welcome!


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.