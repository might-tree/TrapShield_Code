d=$(pwd)

# convert pdf to image and create_output file
python3 convert_pdf_jpeg.py -f $1 -o $2 -d $3

i=1
for entry in "$2"*.jpg
do
    echo "$entry"
    # rotation correction
    #python transform.py -f $entry

    # for generating the table coordinates
    #cd './models/research/'
    #python testing.py -f $entry -o $3 -g $5
    #@surya
    #echo "calling testing.py"
    python testing.py -f $entry -o $3 -g $5
    #cd $d

    # run main script
    python checkout_header_v4.py -f $entry -o $3 -z $4

    # run the final display script and conversion script csv
    python convert_npy_to_csv.py -f $entry -o $3

    # wait for results 
    #@manju change sleep to 1 previous value 5
    #sleep 1

    # delete files
    rm $entry
done
