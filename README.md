pip install -r requirements.txt
python3 main.py

searches the given path for image files (pillow-supported files listed here: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html)
resizes pictures to fit 1080x1350 instagram maximal picture size in case they are larger 
adds black border if necessary 
puts them in /insta subfolder in jpeg format

converts the original pictures to jpeg and saves them in /high_res subfolder
