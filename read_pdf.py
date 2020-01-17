from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import csv

PDF_FILE = 'pdfs/2018/01/acrisio_sena_01_2018.pdf'
OUTPUT_FILE = 'txt/output.txt'
IMG_FILE = 'images/1.jpg'
csv_file = r"text1.csv"

images = convert_from_path(PDF_FILE, dpi=400)
for image in images:
    image.save(IMG_FILE, 'JPEG')

outfile = OUTPUT_FILE
f = open(outfile, "a")
text = str(((pytesseract.image_to_string(Image.open(IMG_FILE), lang='por'))))
text = text.replace('-\n', ',')

f.write(text)
f.close()

in_txt = csv.reader(open(text, "rb"), delimiter = '\t')
out_csv = csv.writer(open(csv_file, 'wb'))

out_csv.writerows(in_txt)
