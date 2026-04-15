import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep

def open_images(prompt):
    folder_path = r"Data"
    prompt = prompt.replace(" ", "_")

    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)

        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)

        except IOError:
            print(f"Unable to open {image_path}")

API_URL = "add your api url"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}


async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

async def generate_images(prompt: str):
    tasks = []
    
    # Create Data directory if it doesn't exist
    os.makedirs("Data", exist_ok=True)

    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High Details, High Resolution, seed = {randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        image_path = os.path.join("Data", f"{prompt.replace(' ','_')}{i + 1}.jpg")
        with open(image_path, "wb") as f:  # Note 'wb' for binary write
            f.write(image_bytes)

def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)

def main():
    while True:
        try:
            # Create FrontEnd/Files directory if it doesn't exist
            os.makedirs(r"FrontEnd\Files", exist_ok=True)
            
            # Check if file exists, if not create it with default values
            if not os.path.exists(r"FrontEnd\Files\ImageGeneration.data"):
                with open(r"FrontEnd\Files\ImageGeneration.data", "w") as f:
                    f.write(",False")
            
            with open(r"FrontEnd\Files\ImageGeneration.data", "r") as f:
                Data: str = f.read().strip()

            if Data:  # Only proceed if data is not empty
                parts = Data.split(",")
                if len(parts) >= 2:
                    Prompt, Status = parts[0], parts[1]
                else:
                    sleep(1)
                    continue

                if Status == "True" and Prompt:  # Ensure Prompt is not empty
                    print("Generating Images ....")
                    GenerateImages(prompt=Prompt)
                    with open(r"FrontEnd\Files\ImageGeneration.data", "w") as f:
                        f.write("False,False")
                    break

            sleep(1)

        except Exception as e:
            print(f"Error occurred: {e}")
            sleep(1)

if __name__ == "__main__":
    main()