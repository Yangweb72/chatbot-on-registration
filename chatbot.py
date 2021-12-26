import json
import pandas
import os
import re


class chatbot:
    def __init__(self, user_info):
        self.state_info = {}  # 状态信息
        self.slot_templet_info = {}  # 所需槽信息
        self.user_info = user_info  # 用户暂存信息
        self.load()

    # 加载信息
    def load(self):
        self.load_slot_template('./slot_template.xlsx')
        self.load_state('./register_states.json')

    # 加载对话状态
    def load_state(self, path):
        with open(path, encoding="utf8") as f:
            state_list = json.loads(f.read())
            for state_info in state_list:
                state_name = state_info["state"]
                self.state_info[state_name] = state_info

    # 加载槽模板
    def load_slot_template(self, path):
        df = pandas.read_excel(path)
        for index in range(len(df)):
            slot = df["slots"][index]
            values = df["values"][index]
            query = df["queries"][index]
            self.slot_templet_info[slot] = [query, values]

    # 获取匹配分值，也是规则和模型两种
    # 没有数据就用jaccard距离直接算，也可以用编辑距离、词袋后的余弦相似度等简单算法
    def sentence_similarity(self, string1, string2):
        jaccard_distance = len(set(string1) & set(string2)) / len(set(string1) | set(string2))
        return jaccard_distance

    # 意图识别
    def get_intent(self):
        query = self.user_info['query']
        scores = []
        for state in self.user_info["possible_states"]:
            intents = self.state_info[state]["intents"]
            score = 0
            for intent in intents:
                score = max(score, self.sentence_similarity(query, intent))  # 这里可以用文本分类或匹配的算法来提高效果，但没数据就直接用规则类的算法做了
            scores.append([state, score])
        scores = sorted(scores, reverse=True, key=lambda x: x[1])
        next_state, next_score = scores[0]
        self.user_info['next_state'] = next_state
        self.user_info['next_score'] = next_score

    def get_slot_value(self):
        query = self.user_info['query']
        state = self.user_info['next_state']
        slots = self.state_info[state].get("slot", [])
        for slot in slots:
            _, pattern = self.slot_templet_info[slot]
            if re.search(pattern, query):
                self.user_info[slot] = re.search(pattern, query).group()

    def nlu(self):
        self.get_intent()
        self.get_slot_value()

    def dialogue_state_track(self):
        state = self.user_info['next_state']
        needed_slots = self.state_info[state].get("slot", [])
        self.user_info["needed_slots"] = []
        for needed_slot in needed_slots:
            if needed_slot not in self.user_info:
                self.user_info['needed_slots'].append(needed_slot)
        self.user_info['needed_slots_state'] = state  # 记录还需要填槽的状态

    def get_possible_state(self):
        state = self.user_info["next_state"]
        possible_states = self.state_info[state].get("possible_states", [])
        self.user_info["possible_states"] = possible_states

    def take_action(self, action):
        print('系统指令:', action)

    def get_actions(self):
        state = self.user_info['next_state']
        actions = self.state_info[state].get("actions", [])
        for action in actions:
            self.take_action(action)

    def policy_making(self):
        needed_slots = self.user_info["needed_slots"]
        # 如果槽位已经足够了可以直接回应
        if not needed_slots:
            self.user_info["policy"] = "response"
            self.get_possible_state()
            self.get_actions()
        # 不然就可能的状态还是当前状态，接着填槽
        else:
            slot = needed_slots[0]
            self.user_info["policy"] = "need:%s" % slot

    def fill_slot(self, response):
        for slot in self.slot_templet_info:
            if slot in self.user_info and slot in response:
                response = re.sub(slot, self.user_info[slot], response)
        return response

    def nlg(self):
        response = '没有回应？！'
        policy = self.user_info["policy"]
        state = self.user_info["next_state"]
        if policy == "response":
            response = self.state_info[state]["response"]
            response = self.fill_slot(response)
        elif policy.startswith("need:"):
            slot = policy.split(':')[1]
            response, _ = self.slot_templet_info[slot]
        print(response)
        print(self.user_info)
        print('-' * 20)

    def query(self, sentence):
        self.user_info["query"] = sentence
        self.nlu()  # 理解句子获得意图和槽
        self.dialogue_state_track()  # 判断还有那些slot没填充完毕
        self.policy_making()
        self.nlg()


if __name__ == '__main__':
    print('-' * 20)
    user_info = {"possible_states": ["state1"]}
    cb = chatbot(user_info)
    while True:
        inputs = input('请您输入:')
        cb.query(inputs)
