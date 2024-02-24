pip install -r requirements.txt
python3 main.py

searches the given path for image files in the top-level directory
testes with TIFF files only, potentially can support every pillow format
resizes pictures to fit 1080x1350 instagram maximal picture size in case they are larger 
adds black border if necessary 
puts them in /insta subfolder in jpeg format

converts the original pictures to jpeg and saves them in /high_res subfolder
