import os
import time
import re


def LZ78_encode(path_file, encoded_path_file):
    print("Первоначальный файла - {} байт".format(os.path.getsize(path_file)))
    with open(path_file, 'r') as f:
        record = dict()
        key = ""
        index = 1
        for line in f.readlines():
            for char in line:
                key += char
                # print(key)
                if key not in record:
                    value = key[-1]
                    if (re.match(r'\d', value)) is not None:
                        value = '%' + value + '%'
                    if len(key) == 1:
                        record.update({key: (0, value, index)})
                    else:
                        link_index = record[key[:-1]][2]
                        record.update({key: (link_index, value, index)})
                    key = ""
                    index += 1

        if key != "":
            link_index = record[key[:-1]][2]
            record.update({key + '$': (link_index, '$', index)})
        else:
            record.update({'$': (0, '$', index)})

        with open(encoded_path_file, 'wb') as f2:
            for value in record.values():
                f2.write(str(value[0]).encode('utf-8'))
                f2.write(str(value[1]).encode('utf-8'))
        print("LZ78 закодированный файл - {} байт".format(os.path.getsize(encoded_path_file)))


def LZ78_decode(encoded_file_path, decoded_path_file):
    def __recreate(arr):
        record = []
        new_text = ''
        for items in arr:
            item = items[0]
            if items[1] != '':
                splitted = re.split('%', item)
                index = int(splitted[0])
                curr_char = splitted[1]
            else:
                index = int(item[:-1])
                curr_char = item[-1]
            if index == 0:
                new_text += curr_char
                record.append(curr_char)
            else:
                prefix = record[index - 1]
                new_text += prefix + curr_char
                record.append((prefix + curr_char))
        return new_text

    with open(encoded_file_path, 'rb') as f2:
        values = []
        for line in f2.readlines():
            items = (re.findall(r'(\d+(\%\d)?\D)', line.decode('utf-8')))
            values += items
        text = __recreate(values)
        with open(decoded_path_file, 'w') as f3:
            f3.write(text)


def main():
    start = time.time()
    LZ78_encode('texts/CrimeAndPunishmentEng.txt', 'data_LZ78_encoded.txt')
    LZ78_decode('data_LZ78_encoded.txt', 'data_LZ78_decoded.txt')
    end = time.time()
    print(f"Время потраченное на кодирование и декодирование: {end - start} сек.")


if __name__ == '__main__':
    main()
