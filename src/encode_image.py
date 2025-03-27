import base64

with open("C:/Users/Ryan/PycharmProjects/PythonProject/assets/CCASH_logo_banner.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
print(f"data:image/png;base64,{encoded_string}")