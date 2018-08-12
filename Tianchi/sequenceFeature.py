# encodig=utf-8
# Writer : lgy
# dateTime : 2018-07-27

from preprocess import loaddata
import pickle as pkl

output_path_dir = "Data/sequencefeature/"

apiMap = None
returnMap = None

with open(output_path_dir + "/api_idmap.pkl", "wb") as api_idmap_file:
    # print(len(apiMap))
    apiMap = pkl.load(api_idmap_file)

with open(output_path_dir + "/return_idMap.pkl", "wb") as return_idMap_file:
    # print(len(returnMap))
    returnMap = pkl.load(return_idMap_file)


def getSequence(file="Data/SourceData/train.csv"):
    print(file)
    data_iter = loaddata(file)
    lines = next(data_iter)
    data = {}
    for lines in data_iter:
        # print(lines[0])
        for line in lines:
            user_id = line[0]
            api_name = line[2]
            return_value = line[-2]
            order_index = int(line[-1])
            tid = line[3]
            d = list((tid, order_index, api_name, return_value))
            if user_id in data:
                data[user_id].append(d)
            else:
                data[user_id] = [d]
        # break
    new_data = {}
    for user_id in data:
        user_data = data[user_id]
        if not user_data:
            continue
        user_data = sorted(user_data, key=lambda s: s[1])
        user_data = sorted(user_data, key=lambda s: s[0])
        api_features = [line[2] for line in user_data]
        return_value_features = [line[3] for line in user_data]
        new_data[user_id] = [api_features, return_value_features]
    return new_data


def dealAllDataSequence(input_dir="Data/SourceData/train/", output_dir="Data/sequencefeature/", device_size=60):
    with open(output_dir + "sequence.txt", "w") as fp:
        for i in range(device_size):
            print("deal the %05d.txt file" % i)
            sequecen_feature = getSequence(input_dir + ("%05d" % i) + ".txt")
            for key in sequecen_feature:
                fp.write(
                    key + "\t" + ",".join(sequecen_feature[key][0]) + "\t" + ",".join(sequecen_feature[key][1]) + "\n")
            print("finished the %05d.txt file!" % i)

dealAllDataSequence()

def getTestApiSequence(file="Data/SourceData/test.csv"):
    print(file)
    data_iter = loaddata(file)
    lines = next(data_iter)
    data = {}
    for lines in data_iter:
        # print(lines[0])
        for line in lines:
            user_id = line[0]
            api_name = line[1]
            # return_value = line[-2]
            order_index = int(line[-1])
            tid = line[3]
            d = list((tid, order_index, api_name))
            if user_id in data:
                data[user_id].append(d)
            else:
                data[user_id] = [d]
        # break
    new_data = {}
    for user_id in data:
        user_data = data[user_id]
        if not user_data:
            continue
        user_data = sorted(user_data, key=lambda s: s[1])
        user_data = sorted(user_data, key=lambda s: s[0])
        api_features = [apiMap[line[2]]5 for line in user_data]
        # return_value_features = [line[3] for line in user_data]
        new_data[user_id] = [api_features]
    return new_data
