import json
import pandas
import os
import re

from config import config

from src.loader import load_schema
from src.nlu import nlu
from src.dst import dst
from src.pm import pm
from src.nlg import nlg


class ChatBot:
    def __init__(self, config):
        self.state_info = {}  # 状态信息
        self.slot_templet_info = {}  # 所需槽信息
        self.user_info = config['user_info']  # 用户暂存信息
        self.config = config
        self.load()

    # 加载信息
    def load(self):
        self.state_info, self.slot_templet_info = load_schema(self.config)

    def query(self, sentence):
        self.user_info['query'] = sentence
        self.user_info = nlu(self.user_info, self.state_info, self.slot_templet_info)
        self.user_info = dst(self.user_info, self.state_info)
        self.user_info = pm(self.user_info, self.state_info, self.slot_templet_info)
        self.user_info = nlg(self.user_info, self.state_info, self.slot_templet_info)


'''
user_info参考
{
    'possible_states': [],
    'query': '刷新',
    'state': 'state3',
    'next_score': 1.0,
    '#性别#': '男',
    '#年龄#': '22',
    'needed_slots': [],
    'needed_slots_state': 'state3',
    'policy': 'response'
}
'''

if __name__ == '__main__':
    print('-' * 20)
    cb = ChatBot(config)
    while True:
        inputs = input('请您输入:')
        print('-' * 20)
        cb.query(inputs)
        if not cb.user_info["possible_states"]:
            print('本轮挂号对话结束，欢迎下次使用')
            break
