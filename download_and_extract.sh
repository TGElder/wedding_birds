page_to=`expr $1 + 1`
python3 download_images.py "https://ia802708.us.archive.org/BookReader/BookReaderImages.php?zip=/5/items/memorialeditiono01bewirich/memorialeditiono01bewirich_jp2.zip&file=memorialeditiono01bewirich_jp2/memorialeditiono01bewirich_{}.jp2&scale=1&rotate=0" "." --from_page=$1 --to_page=$page_to
printf -v p "%04d" $1
python3 bird_extractor.py $p.jpg $2.png
xdg-open $2.png
