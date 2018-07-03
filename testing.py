file_name = "seed_data/u.item"


def get_max_len_title(file_name):
    file = open(file_name)

    max_length = 0
    max_length2 = 0

    for line in file:
        items = line.split("|")
        title = items[1]
        title_len = len(title)
        if title_len > max_length:
            max_length = title_len
        url = items[4]
        # print(item2[4])
        url_len = len(url)
        # print(url_len)
        if url_len > max_length2:
            max_length2 = url_len

    print(max_length)
    print(max_length2)


get_max_len_title(file_name)
