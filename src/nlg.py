import re


class NLG:
    def __init__(self):
        pass

    def fill_slot(self, response):
        for slot in self.slot_templet_info:
            if slot in self.user_info and slot in response:
                response = re.sub(slot, self.user_info[slot], response)
        return response

    def nlg(self, user_info, state_info, slot_template):
        self.user_info = user_info
        self.state_info = state_info
        self.slot_templet_info = slot_template

        response = '没有回应？！'
        policy = self.user_info["policy"]
        state = self.user_info["state"]
        if policy == "response":
            response = self.state_info[state]["response"]
            response = self.fill_slot(response)
        elif policy.startswith("need:"):
            slot = policy.split(':')[1]
            response, _ = self.slot_templet_info[slot]
        print(response)


def nlg(user_info, state_info, slot_template_info):
    nl = NLG()
    nl.nlg(user_info, state_info, slot_template_info)
    return nl.user_info


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

    user_info = nlg(user_info, state_info, slot_templet_info)
    print(user_info)
