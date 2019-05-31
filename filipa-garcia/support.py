import json

from datetime import *


def remove_columns(data):
    """ Selecting Only the Necessary Columns """
    data_small = dict()  # new dictionary with only the time and duration columns
    for item in data['entry']:
        timestamp = datetime.strptime(item['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
        duration = item['duration']
        data_small[timestamp] = duration
    return data_small


def moving_average(mapping, window=10):
    """ Calculating Moving Average """
    t_min = min(mapping)
    t_max = max(mapping)
    one = timedelta(minutes=1)
    times = list(mapping.keys())
    round_minute = t_min.replace(second=0, microsecond=0)

    # initialize variables
    ma = 0  # ma -> moving average
    s = 0
    i = 0
    duration_list = []
    age = []

    yield round_minute, s
    while round_minute <= t_max:
        for j in range(len(age)):
            age[j] += 1
        round_minute += one

        if window in age:
            index = age.index(window)
            s -= duration_list[index]
            del duration_list[index]
            del age[index]
            i = len(duration_list)
            if i == 0:
                ma = 0
            else:
                ma = s / i

        if times[0] < round_minute:
            i += 1
            duration = mapping[times[0]]
            duration_list.append(duration)
            age.append(0)
            s += mapping[times[0]]
            times.remove(times[0])
            ma = s / i

        yield round_minute, ma


def save_to_file(ma_data, dictionary, output_file):
    """ Save the Output Data to a File """
    if output_file != '':
        dictionary['entry'].append({
            'date': ma_data[0].strftime('%Y-%m-%d %H:%M:%S.%f'),
            'average_delivery_time': ma_data[1]
        })
    with open(output_file, 'w') as outfile:
        json.dump(dictionary, outfile)
