import os

def get_file_list(directory):
    try:
        # 获取目录下的所有文件和文件夹
        files = os.listdir(directory)
        # 过滤只保留文件
        file_list = [f for f in files if os.path.isfile(os.path.join(directory, f))]
        return file_list
    except Exception as e:
        print(f"Error reading directory: {e}")
        return []

# 示例用法
directory = "./audio"  # 指定目录
file_list = get_file_list(directory)
print("文件列表:", file_list)

if __name__ == '__main__':
    get_file_list("./audio")