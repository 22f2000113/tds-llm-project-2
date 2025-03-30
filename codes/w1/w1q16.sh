
input_directory=$1
empty_directory=$2
echo "Current directory is: $current_directory"
cd ../..

find $input_directory f -exec mv {} $input_directory/empty_folder \;

cd  $input_directory/empty_folder
grep . * | LC_ALL=C sort | sha256sum