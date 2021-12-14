import os
import argparse
import shutil
from zipfile import ZipFile, ZIP_DEFLATED
from uuid import uuid4
import xlsxwriter

'''
# TODO 进行端口扫描
1. 对端口进行分类
2. 打包成zip输出
'''
class Ports():
    def __init__(self):
        self.output_dir = 'output'
        self.make_dir(self.output_dir)

    def get_all_ip(self, directory, ports, files):
        # files_list = []
        for port in ports:
            ip_list = []
            string = ":" + port
            # read file
            for file in files:
                file = os.path.join(directory, file)
                # 打开文件，忽略编码错误
                with open(file, 'r', errors='ignore') as f:
                    # 读取所有行
                    lines = f.readlines()
                    for line in lines:
                        # 加换行符，防止下面tail数组为空报错，相当于在文件结尾添加空行
                        if '\n' not in line:
                            line = line + '\n'
                        if string in line:
                            head, sep, tail = line.partition(string)
                            if tail[0].isdigit() or len(head) < 8 or len(head) > 16:
                                pass
                            else:
                                ip_list.append(head)
            self.write_file(port, ip_list)
        print('saving result to xls...')
        self.generate_excel(self.output_dir)

    def make_dir(self, dir_name):
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        else:
            print('Deleting output folder ...')
            shutil.rmtree(dir_name)
            os.mkdir(dir_name)

    def write_file(self, port, ip_list):
        ip_list = list(set(ip_list))
        port_file = port + '.txt'
        output_file_path = os.path.join(self.output_dir, port_file)
        if os.path.exists(port_file) or len(ip_list) == 0:
            pass
        else:
            with open(output_file_path, 'w', encoding='utf-8') as f:
                # print(string)
                for ip in ip_list:
                    if len(ip) <= 15:
                        f.writelines(ip)
                        f.write('\n')

    def generate_excel(self, dir_name):
        xls_path = dir_name+'/output.xlsx'
        workbook = xlsxwriter.Workbook(xls_path) # 建立文件
        files = os.listdir(dir_name)
        files.sort(key=lambda x:int(x.split('.txt')[0]))
        for filename in files:
            with open(dir_name+'/'+filename,'r', encoding="utf-8") as f:
                worksheet = workbook.add_worksheet(filename) # 建立sheet， 可以work.add_worksheet('employee')来指定sheet名，但中文名会报UnicodeDecodeErro的错误
                worksheet.write('A1', 'IP')
                i = 1
                for line in f.readlines():
                    worksheet.write(i,0,line)
                    i = i + 1
        workbook.close()

    def backupZip(self, zipfile):  # 这个函数只做文件夹打包的动作，不判断压缩包是否存在
        folder = self.output_dir
        with ZipFile(zipfile, 'w') as zfile:  # 以写入模式创建压缩包
            for foldername, subfolders, files in os.walk(folder):  # 遍历文件夹
                print('Adding files in ' + zipfile + '...')
                zfile.write(foldername)
                for i in files:
                    zfile.write(os.path.join(foldername, i))
                    # print('Adding ' + i)
        print('Done.')

    def folder2zip(self, zipfile, interface):  # 文件夹打包为zip的函数
        if interface:
            if not os.path.exists(zipfile):  # 检查压缩包是否存在，如果已存在则询问是否继续
                self.backupZip(zipfile)
            else:
                response = input("Zipfile exists. Coutinue?('q' for quit): ")
                if response != 'q':
                    self.backupZip(zipfile)
        else:
            self.backupZip(zipfile)

    @staticmethod
    def get_ports_list():
        ports = []
        for i in range(1, 65536):
            ports.append(str(i))
        return ports



if __name__ == '__main__':
    # 设置交互参数
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, default="",
                        help="指定同一目录下的扫描结果文件。")
    parser.add_argument("-d", "--directory", type=str, default="scan",
                        help="指定存放端口扫描结果的目录。不设置参数则默认为scan目录。")
    parser.add_argument("-p", "--port", type=str, default="",
                        help="指定要处理的端口。用','分隔。如：80,443")
    parser.add_argument("-o", "--output", type=str, default="",
                        help="指定输出的压缩文件名,不需要后缀。不设置参数则随机生成文件名。")
    # 这个暂时没啥用
    parser.add_argument("-i", "--interface", action='store_false', default=True,
                        help="产生交互。不设置参数则不进行交互，终端不显示任何信息。")
    args = parser.parse_args()

    # 获取参数
    directory = args.directory
    interface = args.interface
    # 实例化端口处理对象
    handle = Ports()
    # 获取存放扫描结果的目录路径
    path = os.getcwd()
    dir_path = os.path.join(path, directory)
    if args.output == '':
        zipfile = str(uuid4()).split('-')[0] + '.zip'
    else:
        zipfile = args.output + '.zip'

    # 获取处理端口，默认是1-65535
    if args.port == '':
        ports = handle.get_ports_list()
    else:
        ports = args.port.split(',')
        # 处理空格
        for i in range(len(ports)):
            ports[i] = ports[i].strip()

    # 没有指定处理文件
    if args.file == '':
        # 创建目录
        if not os.path.exists(directory):
            os.mkdir(dir_path)
            print("请将扫描结果存放到{directory}中,或通过-f指定单个文件。".format(directory=directory))
        else:
            # 检查文件夹是否为空，非空则进行处理
            for root, dirs, files in os.walk(dir_path, topdown=False):
                # print(root)     # 当前目录路径
                # print(dirs)     # 当前目录下所有子目录
                # print(files)  # 当前路径下所有非目录子文件
                if files is not []:
                    print("...I am running...")
                    # 端口ip分类，输出到output文件夹
                    handle.get_all_ip(args.directory, ports, files)
                    # 压缩output文件夹，生成zip压缩包，可以使用-o指定压缩包文件名
                    handle.folder2zip(zipfile, interface)
                    # TODO 使用线程或者携程，提高处理效率
    else:
        file = list(args.file)
        handle.get_all_ip('.', ports, file)


# 正则
# import re
# 127.0.0.1:8080
# (?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?):\d*