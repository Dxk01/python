#encodig=utf-8
# Writer : lgy
# dateTime : 2018-07-27

from preprocess import loaddata

file="test"

input_file="Data/SourceData/"+file+".csv"

print(input_file)

def devidefile(input=input_file, decide_size=60, output_dir="Data/SourceData/"+file+"/"):
    data_iter = loaddata(input)
    files_fps = [open(output_dir+("%05d"%i)+".txt", "w") for i in range(decide_size)]
    for lines in data_iter:
        for line in lines:
            value = int(int(line[0])%decide_size)
            write_line = ",".join(line)+"\n"
            files_fps[value].write(write_line)

devidefile()
