import json

from FileUtil import  current_dir,get_files_in_directory

import base64
def image_to_base64(image_path):
    # Open the image in binary mode
    with open(image_path, "rb") as image_file:
        # Read the image and encode it to base64
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def get_image_hash(question):
    file_path = current_dir + "/inputs/W3Q4/"
    files = get_files_in_directory(file_path)

    payload = '''{
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract text from this image"},
                    {
                        "type": "image_url",
                        "detail": "low",
                        "image_url": {"url": "data:image/png;base64,'''+image_to_base64(file_path+files[0])+'''"}
                    }
                ]
            }
        ]
    }'''
    return json.dumps(payload)
