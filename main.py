import pyautogui
import os
import time
import img2pdf
from enum import Enum
from PIL import ImageGrab


# if we scan a book spread, then divide the number of pages by 2
class PagesOnTheScreen(Enum):
    ONE = 1
    TWO = 2


def clear_directory(directory_path):
    try:
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"All files in {directory_path} have been deleted.")
    except Exception as e:
        print(f"Error: {e}")


def countdown_timer():
    for i in range(5, 0, -1):
        print(f"Work will start after: {i} seconds")
        time.sleep(1)


def convert_jpegs_to_pdf(image_folder, pdf_path):
    images = [image for image in os.listdir(image_folder) if image.lower().endswith(('.jpg', '.jpeg'))]
    images = sorted(images, key=lambda x: int(x.split('.')[0]))

    with open(pdf_path, "wb") as pdf_file:
        pdf_file.write(img2pdf.convert([os.path.join(image_folder, img) for img in images]))
    print(f"All done. Your file in {pdf_path}")


def scan(num_pages, save_directory, num_pages_on_the_screen):
    screenshots_count = num_pages

    # if we scan a book spread, then divide the number of pages by 2
    if num_pages_on_the_screen == PagesOnTheScreen.TWO:
        screenshots_count = screenshots_count // 2

    # Create the directory if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    countdown_timer()

    for screenshot_number in range(screenshots_count):
        # Create a unique filename for each screenshot
        filename = os.path.join(save_directory, f"{screenshot_number}.jpg")

        screenshot = ImageGrab.grab()
        screenshot = screenshot.convert("RGB")
        screenshot.save(filename, "JPEG")

        print(f"screenshot {screenshot_number}.jpg ... done")

        # Pause for 1 second (you can adjust this based on your needs)
        pyautogui.PAUSE = 1

        # Press the right arrow key to go to the next page
        pyautogui.press('right')


if __name__ == '__main__':
    num_pages = 328
    # Set the directory where you want to save the screenshots
    save_screenshot_tmp_directory = "/Users/pingvinus/Desktop/tmp"
    # Set the full output.pdf file name
    pdf_name = "/Users/pingvinus/Desktop/output.pdf"

    clear_directory(save_screenshot_tmp_directory)
    scan(num_pages, save_screenshot_tmp_directory, PagesOnTheScreen.TWO)
    convert_jpegs_to_pdf(save_screenshot_tmp_directory, pdf_name)
