import pandas as pd

def snapshot(csv, starting, count):
    data = pd.read_csv(csv, header=None)
    return list(data[starting-1:starting+count-1][1])

def validate_snapshot(snapshot_data, csv, starting, count):
    validity = True
    data = snapshot(csv, starting, count)
    if len(snapshot_data) != len(data):
        validity = False
        return validity
    else:
        for i in range(len(snapshot_data)):
            print(snapshot_data[i],data[i])
            if snapshot_data[i] != data[i]:
                validity = False

        return validity # which will be true if all the data are the same


if __name__ == '__main__':
    fil = "DATA-2024.02.20-14.53.07.692179.csv"
    sn_d = snapshot(fil, 69, 10)
    print(validate_snapshot(sn_d, fil, 69, 10))