a slow tool to scan ports and analyze ports.


### Hot to use
usage: get_ip.py [-h] [-f FILE] [-d DIRECTORY] [-p PORT] [-o OUTPUT] [-i]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  指定同一目录下的扫描结果文件。
  -d DIRECTORY, --directory DIRECTORY
                        指定存放端口扫描结果的目录。不设置参数则默认为scan目录。
  -p PORT, --port PORT  指定要处理的端口。用','分隔。如：80,443
  -o OUTPUT, --output OUTPUT
                        指定输出的压缩文件名,不需要后缀。不设置参数则随机生成文件名。
  -i, --interface       产生交互。不设置参数则不进行交互，终端不显示任何信息。

### TODO
1. speed up
2. port scan

### Done
1. Auto port classification.
2. Output a zipfile.

![lazy picture](https://github.com/Fankaren/Lazy_scan/blob/main/img/run.jpg)