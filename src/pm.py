class PM:
    def __init__(self):
        pass

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

    def policy_making(self, user_info, state_info):
        self.user_info = user_info
        self.state_info = state_info

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


def pm(user_info, state_info):
    po = PM()
    po.policy_making(user_info, state_info)
    return po.user_info


if __name__ == '__main__':
    user_info = {'possible_states': ['state1'],
                 'query': '刷新',
                 'next_state': 'state3',
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

    user_info = pm(user_info, state_info)
    print(user_info)
