

input_file1=$1
input_file2=$2
cd $3
diff $input_file1 $input_file2 |grep '<' |wc -l


