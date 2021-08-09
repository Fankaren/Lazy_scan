import sys
import time
from asyncio import Queue, gather
from typing import List
import warnings
warnings.filterwarnings("ignore")


class CheckCDN(object):
    def __init__(self, domains: List[str] = None, time_out: float = 0.1, port: List[int] = None,
                 concurrency: int = 1000):
        # if not ip:
        #     raise ValueError(f'wrong ip! {ip}')
        # self.ip = ip
        # self.port = port
        if domains is None:
            raise ValueError(f'No domain found!')
        self.domains: List[str] = domains
        self.result: List[int] = []
        self.loop = self.get_event_loop()
        # 队列的事件循环需要用同一个，如果不用同一个会报错，这里还有一点不明白
        self.queue = Queue(loop=self.loop)
        self.timeout = time_out
        # 并发数
        self.concurrency = concurrency

    # 创建获取当前事件循环
    @staticmethod
    def get_event_loop():
        """
        判断不同平台使用不同的事件循环实现

        :return:
        """
        if sys.platform == 'win32':
            # 只支持sockets，Pipes和subprocesses
            from asyncio import ProactorEventLoop
            # 用 "I/O Completion Ports" (I O C P) 构建的专为Windows 的事件循环
            return ProactorEventLoop()
        else:
            # 只支持sockets，不支持Pipes和subprocesses
            from asyncio import SelectorEventLoop
            return SelectorEventLoop()

    # 判断CDN函数
    async def check_cdn(self):
        while True:
            domain = await self.queue.get()
            try:
                ip_list = []
                addrs = await self.loop.getaddrinfo(domain, None, family=0)
                for item in addrs:
                    get_ip = item[4][0]
                    if item[4][0] not in ip_list:
                        if item[4][0].count('.') == 3:
                            ip_list.append(item[4][0])
                        else:
                            pass
                if len(ip_list) > 1:
                    # print('{} may has CDN!'.format(domain))
                    self.queue.task_done()
                else:
                    print('{},{}'.format(domain, get_ip))
                    self.queue.task_done()
            except:
                # print(domain)
                # print('domain: {} CDN检测失败，请检查输入格式, 也可能无法访问'.format(domain))
                self.queue.task_done()


    async def start(self):
        banner = '''
===============================================================================
 _____           _
|  ___|_ _ _ __ | | ____ _ _ __ ___ _ __
| |_ / _` | '_ \| |/ / _` | '__/ _ \ '_ \   github: https://github.com/Fankaren
|  _| (_| | | | |   < (_| | | |  __/ | | |  auth: Fankaren 
|_|  \__,_|_| |_|_|\_\__,_|_|  \___|_| |_|  tool: 基于socket的批量域名CDN筛查脚本
===============================================================================
            '''
        print(banner)
        print('在跑了等等吧，有CDN或无法访问的domain不显示...')
        print()
        start = time.time()
        # 使用nowait非阻塞方法将端口号添加进队列，最好做一下异常处理
        for a in self.domains:
            self.queue.put_nowait(a)

        task = [self.loop.create_task(self.check_cdn()) for _ in range(self.concurrency)]

        '''
        join()方法，阻塞至队列中所有的元素都被接收和处理完毕。
        
        当条目添加到队列的时候，未完成任务的计数就会增加。
        每当消费协程调用 task_done() 表示这个条目已经被回收，该条目所有工作已经完成，未完成计数就会减少。
        当未完成计数降到零的时候， join() 阻塞被解除。
        '''
        await self.queue.join()
        # 依次退出
        for a in task:
            a.cancel()
        # gather，捕获任务返回结果以及错误信息。Wait until all worker tasks are cancelled.
        await gather(*task, return_exceptions=True)
        print(f'扫描所用时间为：{time.time() - start:.2f}')


if __name__ == '__main__':
    filepath = "D:\\subs.txt"
    domains = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                if 'http://' or 'https://' in line:
                    line = line.strip('http://').strip('https://')
                if line.count('.') >= 1:
                    domains.append(line.strip('\n'))
    except IOError as err:
        print("Domains not found. Please check it out. Default in D:\\domains.txt.")
    scan = CheckCDN(domains)
    scan.loop.run_until_complete(scan.start())
