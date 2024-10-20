import time
import os
from PIL import Image, ImageOps
import numpy as np
import cv2

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_valid_image(file_path):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    return os.path.splitext(file_path)[1].lower() in valid_extensions

def analyze_image(img):
    """Analyze the image for unique pixel values."""
    unique_values = set(img.getdata())
    return len(unique_values)

def automatic_resize(input_image, fixed_scale_factor=None, resampling_filter=Image.LANCZOS):
    """Resize the image based on unique pixel value analysis or a fixed scale factor."""
    img = input_image.convert("L")  # Convert to grayscale if not already
    
    # Determine scale factor
    if fixed_scale_factor is not None:
        scale_factor = fixed_scale_factor
        print(f"Using fixed scale factor: {scale_factor}")
    else:
        unique_count = analyze_image(img)
        if unique_count < 10:  
            scale_factor = 4
        elif unique_count < 50:  
            scale_factor = 2
        else:  
            scale_factor = 1
        print(f"Calculated scale factor based on unique pixel values: {scale_factor}")
    
    new_width = int(img.width / scale_factor)
    new_height = int(img.height / scale_factor)

    if scale_factor > 1:
        img = img.resize((new_width, new_height), resample=resampling_filter)

    return img, scale_factor

def invert_colors(img):
    """Invert the colors of an image."""
    try:
        inverted_img = ImageOps.invert(img.convert("L"))
        print("Colors inverted successfully.")
        return inverted_img
    except Exception as e:
        print(f"Error during color inversion: {e}")
        return None

def main():
    print("We convert colored images to black and white images.")
    while True:
        user_choice = input("What do you want to do:\n1: Proceed\n2: Exit\n")
        user_choice = handle_input(user_choice)

        if user_choice in (2, 'exit'):
            print("Exiting...")
            time.sleep(1)
            return
        elif user_choice in (1, "proceed"):
            break
        else:
            print("Invalid input. Please choose again.")

    while True:
        image_path = input("Write the path for the image: ").strip('"')
        if not os.path.isfile(image_path):
            print("Error: The specified path does not point to a file.")
            continue
        if not is_valid_image(image_path):
            print("Error: The file is not a valid image format.")
            continue

        directory_path = os.path.dirname(image_path)
        file_name, _ = os.path.splitext(os.path.basename(image_path))
        is_inverted = False  # Track inversion status for filename

        while True:
            threshold_choice = input("Choose the threshold calculation method:\n"
                                     "1: Fixed threshold\n2: Otsu's Method\n"
                                     "3: Adaptive Thresholding\n4: Invert colors\n"
                                     "5: Help\n6: Back\n7: Exit\n")

            threshold_choice = handle_input(threshold_choice)

            if threshold_choice in (6, 'back'):
                break
            elif threshold_choice in (7, 'exit'):
                print("Exiting...")
                time.sleep(1)
                return
            elif threshold_choice == 4:
                img = Image.open(image_path)
                inverted_img = invert_colors(img)
                if inverted_img:
                    is_inverted = True  # Mark as inverted
                    output_filename = f"inverted_{file_name}.png"
                    output_path = os.path.join(directory_path, output_filename)
                    inverted_img.save(output_path)
                    print(f"Inverted image saved as {output_filename} in the path {directory_path}")
                continue

            try:
                img = Image.open(image_path)
            except Exception as e:
                print(f"Failed to open the image: {e}")
                continue

            width, height = img.size
            print(f"Image dimensions before converting: Width = {width}, Height = {height}\n")
            method_selected = process_choice(threshold_choice)

            try:
                if method_selected == "fixed threshold method":
                    bw_image = fixed_threshold_method(img)
                elif method_selected == "otsu's method":
                    bw_image = otsu_method(img.convert("L"))
                elif method_selected == "adaptive thresholding method":
                    bw_image = adaptive_thresholding_method(img.convert("L"))
                elif method_selected == "help":
                    continue
                else:
                    continue
            except Exception as e:
                print(f"Error during processing: {e}")
                continue

            # Post-conversion invert option
        
            while True:
                post_conversion_choice = input("Do you want to invert the colors after conversion?\n1: Yes\n2: No\n")
                post_conversion_choice = handle_input(post_conversion_choice)

                if post_conversion_choice in (1, "yes"):
                    bw_image = invert_colors(bw_image)
                    if bw_image is None:
                        print("Skipping inversion due to an error.")
                    else:
                        is_inverted = True  # Mark as inverted only if inversion succeeds
                    break
                elif post_conversion_choice in (2, "no"):
                    print("Continuing without inverting colors.")
                    is_inverted = False  # Ensure the flag remains False if inversion is not done
                    break
                else:
                    print("Invalid choice. Try again.")


            while True:
                choice = input("Do you want to optimize the image before saving?\n1: Yes\n2: No\n")
                choice = handle_input(choice)
                if choice in (1, "yes"):
                    while True:
                        choice = input("Scaling size options\n1: Auto\n2: Variable\n")
                        choice = handle_input(choice)
                        if choice in (1, "auto"):
                            bw_image, scale_factor = automatic_resize(bw_image)
                            optimization = f"_optimized with auto scale factor of {scale_factor}"
                            break
                        elif choice in (2, "variable"):
                            while True:
                                scale_factor = input("Enter your preferred scale factor: ")
                                if is_float(scale_factor):
                                    scale_factor = float(scale_factor)
                                    bw_image, scale_factor = automatic_resize(bw_image, scale_factor)
                                    optimization = f"_optimized with scale factor of {scale_factor}"
                                    break
                                else:
                                    print("Invalid input. We need a float value.")
                            break
                        else:
                            continue
                    break
                elif choice in (2, "no"):
                    optimization = ""
                    break
                else:
                    print("Invalid choice. Try again.")

            # Add _inverted to the filename if the image was inverted
            inversion_text = "_inverted" if is_inverted else ""
            output_filename = f"black_and_white_using_{method_selected}{optimization}{inversion_text}_{file_name}.png"
            output_path = os.path.join(directory_path, output_filename)

            try:
                bw_image.save(output_path)
                print(f"Black and white image saved as {output_filename} in the path {directory_path}")
                width, height = bw_image.size
                print(f"Image dimensions after converting: Width = {width}, Height = {height}\n")
            except Exception as e:
                print(f"Failed to save the image: {e}")

def process_choice(choice):
    if choice in (1, 'fixed threshold'):
        print("You chose Fixed threshold.")
        return "fixed threshold method"
    elif choice in (2, "otsu's method"):
        print("You chose Otsu's Method.")
        return "otsu's method"
    elif choice in (3, 'adaptive thresholding'):
        print("You chose Adaptive Thresholding.")
        return "adaptive thresholding method"
    elif choice in (5, 'help'):
        print("Help: You can use numeric input or string input.\n"
              "Available choices:\n1: Fixed threshold\n2: Otsu's Method\n"
              "3: Adaptive Thresholding\n4: Invert colors\n5: Help\n6: Back\n7: Exit")
        return "help"
    else:
        print("Invalid choice. Please try again.")
        return "invalid"

def fixed_threshold_method(img):
    gray_img = img.convert("L")
    while True:
        threshold_choice = input("Which threshold do you want to use:\n1: Default (128)\n2: Variable threshold\n")
        threshold_choice = handle_input(threshold_choice)
        
        if threshold_choice in (1, "default", "default(128)"):
            threshold = 128  # Use the default threshold
            break
        elif threshold_choice in (2, "variable threshold"):
            while True:
                action_choice = input("What do you want to do:\n1: Proceed\n2: Back\n")
                action_choice = handle_input(action_choice)
                if action_choice in (2, 'back'):
                    break  # Go back to the previous choice
                elif action_choice in (1, "proceed"):
                    threshold_input = input("Enter your preferred threshold (0-255): ")
                    if threshold_input.isdigit() and 0 <= int(threshold_input) <= 255:
                        threshold = int(threshold_input)
                        break
                    else:
                        print("Invalid input. Allowed input is an integer from 0 to 255.")
                else:
                    print("Invalid choice. Please try again.")
                    continue
            if action_choice in ("back", 2):
                continue
            elif action_choice in ("proceed", 1):
                break
            
        else:
            print("Invalid choice. Please try again.")
            continue
    
    bw_image = gray_img.point(lambda x: 255 if x > threshold else 0, '1')
    return bw_image  # Return the black-and-white image

def adaptive_thresholding_method(pil_img):
    img_array = np.array(pil_img)
    bw_image = cv2.adaptiveThreshold(img_array, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    final_image = Image.fromarray(bw_image)
    return final_image

def otsu_method(pil_img):
    img_array = np.array(pil_img)
    _, bw_image = cv2.threshold(img_array, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    final_image = Image.fromarray(bw_image)
    return final_image

def handle_input(user_input):
    if user_input.isdigit():
        return int(user_input)
    else:
        return user_input.lower()

if __name__ == "__main__":
    main()
