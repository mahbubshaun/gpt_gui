import json
import os
import random
import sys
import threading
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv

from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog

from selenium.webdriver.support.wait import WebDriverWait
import argparse




global entry_3
script_path = sys.argv[0]
script_dir = os.path.dirname(os.path.abspath(script_path))
asset_file_path = os.path.join(script_dir, 'assets//frame0')

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = asset_file_path

global browser_opened
browser_opened = False
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def load_config():
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            try:
                config = json.load(f)
                entry_1.insert(0, config.get('entry_1', ''))
                entry_2.insert(0, config.get('entry_2', ''))
                entry_3.insert(0, config.get('entry_3', '')) # update this line
                entry_5.insert(0, config.get('entry_5', ''))
            except:
                print('error loading config values')



    elif os.path.isfile('file.csv'):
        entry_1.insert(0, os.path.abspath('file.csv'))
    else:
        entry_1.insert(0, "No CSV file found.")

    if entry_2.get() == '':
        entry_2.insert(0, '0')

    if entry_3.get() == '':
        entry_3.insert(0, '5:10')

    if entry_5.get() == '':
        entry_5.insert(0, 'https://chat.openai.com/')

def save_config():
    config = {
        'entry_1': entry_1.get(),
        'entry_2': entry_2.get(),
        'entry_3': entry_3.get(),
        'entry_5': entry_5.get(),
    }
    with open('config.json', 'w') as f:
        json.dump(config, f)
    update_status("Configuration saved.")

# Update command for button_1
def select_csv_file():
    filename = filedialog.askopenfilename(filetypes=(("CSV Files", "*.csv"), ("All files", "*.*")))
    if filename:  # If a file was selected
        entry_1.delete(0, 'end')  # Clear the entry_1
        entry_1.insert(0, filename)  # Insert the selected file path into entry_1

def update_status(message: str):
    print(message)
    entry_4.insert("end", message + "\n")  # Insert the new message at the end
    entry_4.see("end")  # Scroll the Text widget to show the new message


parser = argparse.ArgumentParser()
parser.add_argument('--start_bot', action='store_true', help='Starts the bot after launching the GUI.')
args = parser.parse_args()

window = Tk()
window.title("CHAT GPT RPA BOT")
window.geometry("487x606")
window.configure(bg = "#000000")
global driver
def launch_bot():
    global browser_opened
    print(entry_5.get())
    # Get the path of the original script
    script_path = sys.argv[0]

    # Get the directory name of the script
    script_dir = os.path.dirname(os.path.abspath(script_path))

    # json_file_path = os.path.join(script_dir, 'config.json')
    # # Read the JSON file
    # with open(json_file_path, 'r') as f:
    #     config = json.load(f)

    options = uc.ChromeOptions()
    # headless = config['headless_browser']

    # options.add_experimental_option('prefs', prefs)
    # if headless == 'yes':
    #     options.add_argument("--headless=new")
    options.add_argument("window-size=1920,1080")

    path = os.path.dirname(os.path.abspath(__file__))

    dir_name = 'gpt_browser'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # with zipfile.ZipFile(pluginfile, "w") as zp:
    #     zp.writestr("manifest.json", manifest_json)
    #     zp.writestr("background.js", background_js)

    # options.add_argument("--disable-extensions")
    # options.add_argument(
    #     f"--load-extension={os.path.abspath(dir_name)}\\")

    # provide location where chrome stores profiles
    options.add_argument(f"--user-data-dir={os.getcwd()}/profile_data/browser")
    # options.add_arguments = {'user-data-dir':f'{os.getcwd()}/{username}/browser'}
    # options.add_argument(f"user-data-dir={os.getcwd()}/{username}/browser")
    global driver
    driver = uc.Chrome(options=options)
    browser_opened = True
    # Load the cookies from the file

    driver.get('https://chat.openai.com/')

    # with open(input_path, 'r') as input_file:
    #     reader = csv.DictReader(input_file)
    #     for row_no, row in enumerate(reader):
    #         if row_no >= start_row:
    #             print(row['Question'])  # print the value from column "C"
    #             print(row['Answer'])  # print the value from column "C"


def start_bot():
    print('In start bot')
    global browser_opened
    if not browser_opened:
        launch_bot()
    global driver
    save_config()
    update_status("Loading gpt model")
    driver.get(entry_5.get())
    script_path = sys.argv[0]

    wait1 = WebDriverWait(driver, 120)
    wait2 = WebDriverWait(driver, 10)

    # Get the directory name of the script
    script_dir = os.path.dirname(os.path.abspath(script_path))
    csv_file_path = os.path.join(script_dir, 'file.csv')
    # Read the CSV file into a list of dictionaries


    # Modify the data
    while True:
        with open(csv_file_path, 'r') as input_file:
            reader = csv.DictReader(input_file)
            data = list(reader)
        for row_no, row in enumerate(data):
            if row_no >= int(entry_2.get()):
                print(row['Answer'])
                if row['Answer'] == '':
                    update_status("Reading csv question")
                    print(row['Question'])
                    wait1.until(EC.visibility_of_element_located((By.ID, "prompt-textarea")))
                    update_status("Sending questing to gpt")
                    driver.find_element(By.ID, 'prompt-textarea').send_keys(row['Question'])
                    random_waits(1, 5)
                    driver.find_element(By.XPATH, "//button/span[@data-state='closed']").click()
                    update_status("Question sent, waiting for answer")
                    random_waits(5, 10)
                    wait1.until(
                        EC.invisibility_of_element_located((By.XPATH, "//div[contains(text(),'Stop generating')]")))
                    update_status("Answer is present checking if more answer is available or not")
                    random_waits(1, 5)
                    try:
                        while True:
                            driver.find_element(By.XPATH, "//div[contains(text(),'Continue generating')]").click()
                            update_status("Continuing generating answer")
                            random_waits(5, 10)
                            wait1.until(
                                EC.invisibility_of_element_located(
                                    (By.XPATH, "//div[contains(text(),'Stop generating')]")))

                    except:
                        update_status("Answer generation finished, saving in csv")
                        pass

                    row['Answer'] = driver.find_element(By.XPATH, "(//div[contains(@class,'markdown')])[last()]").text
                    update_status('Saving CSV, Please make sure the csv is not open')

                    random_waits(5, 10)
                    # Write the data back to the file
                    try:
                        with open(csv_file_path, 'w', newline='') as output_file:
                            writer = csv.DictWriter(output_file, fieldnames=data[0].keys())
                            writer.writeheader()
                            writer.writerows(data)
                        update_status("CSV saved!")
                    except PermissionError:
                        update_status("Could not save the csv, as already opened, please close it!")

                    start_value, end_value = entry_3.get().split(":")
                    random_waits(int(start_value), int(end_value))
                else:
                    update_status("No unanswered question found.")

        start_value, end_value = entry_3.get().split(":")
        random_waits(int(start_value), int(end_value))




def random_waits(min_wait, max_wait):
    wait_time = random.uniform(min_wait, max_wait)
    update_status(f"waiting {wait_time} ")
    time.sleep(wait_time)


canvas = Canvas(
    window,
    bg = "#000000",
    height = 606,
    width = 487,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_text(
    159.0,
    63.0,
    anchor="nw",
    text="CHAT GPT RPA",
    fill="#FFFFFF",
    font=("Arial", 20 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))


button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: threading.Thread(target=start_bot, daemon=True).start(),
    relief="flat"
)

button_1.place(
    x=192.0,
    y=369.0,
    width=85.0,
    height=32.0
)

canvas.create_text(
    196.0,
    107.0,
    anchor="nw",
    text="IMPORT CSV",
    fill="#FFFFFF",
    font=("Arial", 15 * -1)
)

canvas.create_text(
    21.0,
    271.0,
    anchor="nw",
    text="STARTING ROW",
    fill="#FFFFFF",
    font=("Arial", 15 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    238.0,
    146.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=71.0,
    y=138.0,
    width=334.0,
    height=14.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    79.5,
    322.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=22.0,
    y=314.0,
    width=115.0,
    height=14.0
)

canvas.create_text(
    172.0,
    271.0,
    anchor="nw",
    text="SLEEP TIME",
    fill="#FFFFFF",
    font=("Arial", 15 * -1)
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    219.5,
    322.0,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=162.0,
    y=314.0,
    width=115.0,
    height=14.0
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    245.0,
    520.0,
    image=entry_image_4
)
entry_4 = Text(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=14.0,
    y=452.0,
    width=462.0,
    height=134.0
)

canvas.create_text(
    207.0,
    421.0,
    anchor="nw",
    text="STATUS",
    fill="#FFFFFF",
    font=("Arial", 15 * -1)
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=select_csv_file,
    relief="flat"
)
button_2.place(
    x=196.0,
    y=170.0,
    width=83.0,
    height=27.0
)

canvas.create_text(
    330.0,
    271.0,
    anchor="nw",
    text="MODEL URL",
    fill="#FFFFFF",
    font=("Arial", 15 * -1)
)

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    370.5,
    322.0,
    image=entry_image_5
)
entry_5 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_5.place(
    x=303.0,
    y=314.0,
    width=135.0,
    height=14.0
)

load_config()
if args.start_bot:
    start_bot()
else:
    launch_bot()
window.resizable(False, False)
window.mainloop()










