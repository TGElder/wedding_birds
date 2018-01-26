page_to=`expr $1 + 1`
python3 download_images.py "https://ia801406.us.archive.org/BookReader/BookReaderImages.php?zip=/8/items/memorialeditiono02bewirich/memorialeditiono02bewirich_jp2.zip&file=memorialeditiono02bewirich_jp2/memorialeditiono02bewirich_{}.jp2&scale=1&rotate=0" "." --from_page=$1 --to_page=$page_to
printf -v p "%04d" $1
python3 image_extractor.py $p.jpg $2.png
xdg-open $2.png
