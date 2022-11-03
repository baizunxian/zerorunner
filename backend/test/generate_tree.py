import os
import os.path

BRANCH = '├─'
LAST_BRANCH = '└─'
TAB = '│  '
EMPTY_TAB = '   '


def get_dir_list(path, placeholder=''):
    folder_list = [folder for folder in os.listdir(path) if
                   os.path.isdir(os.path.join(path, folder)) and '.' not in folder]
    # file_list = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
    result = ''
    for folder in folder_list[:-1]:
        result += placeholder + BRANCH + folder + '\n'
        result += get_dir_list(os.path.join(path, folder), placeholder + TAB)
    # if folder_list:
    #     result += placeholder + (BRANCH if file_list else LAST_BRANCH) + folder_list[-1] + '\n'
    #     result += get_dir_list(os.path.join(path, folder_list[-1]), placeholder + (TAB if file_list else EMPTY_TAB))
    # for file in file_list[:-1]:
    #     result += placeholder + BRANCH + file + '\n'
    # if file_list:
    #     result += placeholder + LAST_BRANCH + file_list[-1] + '\n'
    return result


if __name__ == '__main__':
    print(get_dir_list('../'))
