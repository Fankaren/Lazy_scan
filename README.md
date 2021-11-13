a slow tool to scan and analyze ports.


### Hot to use
1. 将端口扫描文件放到scan文件夹
2. 执行`python3 lazy.py`
3. 端口分类文件输出到output文件夹
4. 自动在脚本同级目录下生成压缩包文件
```
usage: python3 lazy.py [-h] [-f FILE] [-d DIRECTORY] [-p PORT] [-o OUTPUT] [-i]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  指定同一目录下的扫描结果文件。
  -d DIRECTORY, --directory DIRECTORY
                        指定存放端口扫描结果的目录。不设置参数则默认为scan目录。
  -p PORT, --port PORT  指定要处理的端口。用','分隔。如：80,443
  -o OUTPUT, --output OUTPUT
                        指定输出的压缩文件名,不需要后缀。不设置参数则随机生成文件名。
  -i, --interface       产生交互。不设置参数则不进行交互，终端不显示任何信息。
```

### TODO
1. speed up
2. port scan

### Done
1. Auto port classification.
2. Output a zipfile.
3. Easy way to analyze CDN.

![lazy picture](https://github.com/Fankaren/Lazy_scan/blob/main/img/run.jpg)
