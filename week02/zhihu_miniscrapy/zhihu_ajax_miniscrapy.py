import requests
from pathlib import Path
import json
from jsonpath_ng import jsonpath, parse
from queue import Queue
import threading


class CrawlThread(threading.Thread):
    
    """爬虫类"""

    def __init__(self, thread_id, queue):
        super().__init__()
        self.thread_id = thread_id
        self.queue = queue
        self.headers = {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }

    def run(self):
    
        """重写run方法"""
        
        print(f'启动线程：{self.thread_id}')
        self.scheduler()
        print(f'结束线程：{self.thread_id}')

    def scheduler(self):
    
        """模拟任务调度"""
        
        while not self.queue.empty():
            # 队列为空不处理
            page = self.queue.get()
            print(f'下载线程：{self.thread_id}, 下载页面：{page}')
            url = f'https://www.zhihu.com/api/v4/questions/413341964/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=10&offset={page * 10}&platform=desktop&sort_by=default'

            try:
                # downloader 下载器
                response = requests.get(url, headers=self.headers)
                dataQueue.put(response.text)
            except Exception as e:
                print('下载出现异常', e)


class ParserThread(threading.Thread):

    """页面内容解析器类"""

    def __init__(self, thread_id, queue, file):
        super().__init__()
        self.thread_id = thread_id
        self.queue = queue
        self.file = file

    def run(self):
        print(f'启动线程：{self.thread_id}')
        while flag:
            try:
                item = self.queue.get(False)  # 参数为false时队列为空，抛出异常
                if not item:
                    continue
                self.parse_data(item)
                self.queue.task_done()
            except Exception as e:
                pass
        print(f'结束线程：{self.thread_id}')

    def save_json(self, json_data):
        json.dump(json_data, fp=self.file, ensure_ascii=False, indent=4)

    def parse_data(self, item):
    
        """解析网页内容的函数"""
        
        try:
            json_data = json.loads(item)
            try:
                author_name_exp = parse('$..author.name')
                author_names = [match.value for match in author_name_exp.find(json_data)]
                created_time_exp = parse('$..created_time')
                created_times = [match.value for match in created_time_exp.find(json_data)]
                updated_time_exp = parse('$..data[*].updated_time')
                updated_times = [match.value for match in updated_time_exp.find(json_data)]
                voteup_count_exp = parse('$..voteup_count')
                voteup_counts = [match.value for match in voteup_count_exp.find(json_data)]
                comment_count_exp = parse('$..comment_count')
                comment_counts = [match.value for match in comment_count_exp.find(json_data)]
                content_exp = parse('$..content')
                contents = [match.value for match in content_exp.find(json_data)]
                # 统计 item 中的内容数量
                cnt = len(contents)
                response = []
                for i in range(cnt):
                    response.append({})
                for i in range(cnt):
                    response[i]["author_name"] = author_names[i]
                    response[i]["created_time"] = created_times[i]
                    response[i]["updated_time"] = updated_times[i]
                    response[i]["voteup_count"] = voteup_counts[i]
                    response[i]["comment_count"] = comment_counts[i]
                    response[i]["content"] = contents[i]
                self.save_json(response)
            except Exception as e:
                print('answer parse error', e)
        
        except Exception as e:
            print('page error', e)


if __name__ == "__main__":

    # 爬取结果的保存路径
    dest_file = "saved_longmovie.json"
    
    # 计算总页数
    total_num = 408
    page_num = total_num // 10 + 1
    
    # 定义存放网页的任务队列
    pageQueue = Queue(50)
    for page in range(0, page_num):
        pageQueue.put(page)

    # 定义存放解析数据的任务队列
    dataQueue = Queue()

    # 爬虫线程
    crawl_threads = []
    crawl_name_list = ['crawl_1', 'crawl_2', 'crawl_3']
    for thread_id in crawl_name_list:
        thread = CrawlThread(thread_id, pageQueue)
        thread.start()
        crawl_threads.append(thread)

    # 将结果保存到一个json文件中
    with open(dest_file, 'a', encoding='utf-8') as pipeline_f:

        # 解析线程
        parse_threads = []
        parser_name_list = ['parse_1', 'parse_2', 'parse_3']
        flag = True
        for thread_id in parser_name_list:
            thread = ParserThread(thread_id, dataQueue, pipeline_f)
            thread.start()
            parse_threads.append(thread)

        # 结束crawl线程
        for t in crawl_threads:
            t.join()

        # 结束parse线程
        flag = False
        for t in parse_threads:
            t.join()

    print('任务结束，退出主线程')