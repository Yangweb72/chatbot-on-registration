import re


class NLU:
    def __init__(self):
        pass

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
        state, score = scores[0]
        self.user_info['state'] = state
        self.user_info['score'] = score

    # 获取匹配分值，也是规则和模型两种
    # 没有数据就用jaccard距离直接算，也可以用编辑距离、词袋后的余弦相似度等简单算法
    def sentence_similarity(self, string1, string2):
        jaccard_distance = len(set(string1) & set(string2)) / len(set(string1) | set(string2))
        return jaccard_distance

    def get_slot_value(self):
        query = self.user_info['query']
        state = self.user_info['state']
        slots = self.state_info[state].get("slot", [])
        for slot in slots:
            _, pattern = self.slot_templet_info[slot]
            if re.search(pattern, query):
                self.user_info[slot] = re.search(pattern, query).group()

    def nlu(self, user_info, state_info, slot_template_info):

        self.user_info = user_info
        self.state_info = state_info
        self.slot_templet_info = slot_template_info

        self.get_intent()
        self.get_slot_value()
        return self.user_info


def nlu(user_info, state_info, slot_templet_info):
    nl = NLU()
    user_info = nl.nlu(user_info, state_info, slot_templet_info)
    return user_info


if __name__ == '__main__':
    user_info = {'possible_states': ['state1'],
                 'query': '刷新',
                 'state': 'state3',
                 'next_score': 1.0,
                 '#性别#': '男',
                 '#年龄#': '22',
                 'needed_slots': [],
                 'needed_slots_state': 'state3',
                 'policy': 'response'}

    state_info = {'state1': {'state': 'state1',
                             'intents': ['我想要来医院挂号'],
                             'slot': ['#性别#', '#年龄#'],
                             'response': '好的，请确认您的性别年龄：#性别#、#年龄#',
                             'possible_states': ['state2']},
                  'state2': {'state': 'state2',
                             'intents': ['确认'],
                             'actions': ['假装返回一个支付二维码链接:https://www.pleasepayyourbill.com/your_info'],
                             'response': '请支付挂号费5元,支付后请刷新界面获取排队号码',
                             'possible_states': ['state3']},
                  'state3': {'state': 'state3',
                             'intents': ['刷新'],
                             'actions': ['假装将号码信息录入挂号系统:https://www.guahao.com/your_info'],
                             'response': '您的排队号码为xx,祝您身体健康,万事如意',
                             'possible_states': []}}

    slot_templet_info = {'#性别#': ['请问您的性别为', '男|女'],
                         '#年龄#': ['请问您的年龄为', '(\\d+)']}

    user_info = nlu(user_info, state_info, slot_templet_info)
    print(user_info)
