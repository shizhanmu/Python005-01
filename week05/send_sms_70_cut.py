# 作业二：在使用短信群发业务时，公司的短信接口限制接收短信的手机号，每分钟最多发送五次，请基于 Python 和 redis 实现如下的短信发送接口：
# 已知有如下函数：

# def sendsms(telephone_number: int, content: string, key=None)：
#     # 短信发送逻辑, 作业中可以使用 print 来代替
#     pass
#     # 请实现每分钟相同手机号最多发送五次功能, 超过 5 次提示调用方,1 分钟后重试稍后
#     pass
#     print("发送成功")
# 期望执行结果：

# sendsms(12345654321, content=“hello”) # 发送成功
# sendsms(12345654321, content=“hello”) # 发送成功
# …
# sendsms(88887777666, content=“hello”) # 发送成功
# sendsms(12345654321, content=“hello”) # 1 分钟内发送次数超过 5 次, 请等待 1 分钟
# sendsms(88887777666, content=“hello”) # 发送成功
# …
# 选做：
# 1.content 为短信内容，超过 70 个字自动拆分成两条发送
# XX 2. 为 sendsms() 函数增加装饰器 send_times()，通过装饰器方式实现限制手机号最多发送次数，如：

# @send_times(times=5)
# sendsms()

import redis
import time
from datetime import timedelta

client = redis.Redis(host='127.0.0.1', password='123456', decode_responses=True)

def sendsms(telephone_number: int, content: str, key=None):
    client.set(telephone_number, 0, nx=True, ex=timedelta(seconds=10))
    client.incr(telephone_number)
    
    if int(client.get(telephone_number)) <= 5:
        print('发送成功: ', telephone_number)
        print('发送内容: ', content)
    else:
        print('1 分钟内发送次数超过 5 次，请等待 1 分钟')
        client.rpush(f'sms_{telephone_number}', content)
    time.sleep(1)

def main_sendsms(telephone_number: int, content: str, key=None):
    while True:
        if len(content) > 70:
            left, content = content[:70], content[70:]
            client.lpush(f'sms_{telephone_number}', left)
        else:
            client.lpush(f'sms_{telephone_number}', content)
            break
    while client.llen(f'sms_{telephone_number}') >0:
        content = client.rpop(f'sms_{telephone_number}')
        sendsms(telephone_number, content=content, key=None)

if __name__ == "__main__":
    big_text = """
    第1卦　乾为天（乾卦）刚健中正　上上卦
象曰：困龙得水好运交，不由喜气上眉梢，一切谋望皆如意，向后时运渐渐高。
这个卦是同卦（下乾上乾）相叠。象征天，喻龙（德才的君子），又象征纯粹的阳和健，表明兴盛强健。乾卦是根据万物变通的道理，以“元、亨、利、贞”为卦辞，示吉祥如意，教导人遵守天道的德行。
第2卦　坤为地（坤卦）柔顺伸展　上上卦
象曰：肥羊失群入山岗，饿虎逢之把口张，适口充肠心欢喜，卦若占之大吉昌。
这个卦是同卦（下坤上坤）相叠，阴性。象征地（与乾卦相反），顺从天。承载万物，伸展无穷无尽。坤卦以雌马为象征，表明地道生育抚养万物，而又依天顺时，性情温顺。它以“先迷后得”证明“坤”顺从“乾”，依随“乾”，才能把握正确方向，遵循正道，获取吉利。
第3卦　水雷屯（屯卦）起始维艰　下下卦
象曰：风刮乱丝不见头，颠三倒四犯忧愁，慢从款来左顺遂，急促反惹不自由。
这个卦是异卦（下震上坎）相叠，震为雷，喻动；坎为雨，喻险。雷雨交加，险象丛生，环境恶劣。“屯”原指植物萌生大地。万物始生，充满艰难险阻，然而顺时应运，必欣欣向荣。
第4卦　山水蒙（蒙卦）启蒙奋发　中下卦
象曰：卦中爻象犯小耗，君子占之运不高，婚姻合伙有琐碎，做事必然受苦劳。
这个卦是异卦（下坎上艮）相叠，艮是山的形象，喻止；坎是水的形象，喻险。卦形为山下有险，仍不停止前进，是为蒙昧，故称蒙卦。但因把握时机，行动切合时宜，因此，具有启蒙和通达的卦象。"""
    while True:
        time.sleep(1)
        main_sendsms(16678695867, big_text)
        main_sendsms(13377958376, big_text)