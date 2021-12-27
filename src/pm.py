class PM:
    def __init__(self):
        pass

    def get_possible_state(self, filled=True):
        if filled:
            state = self.user_info["state"]
            possible_states = self.state_info[state].get("possible_states", [])
            self.user_info["possible_states"] = possible_states
        else:
            state = self.user_info["state"]
            possible_states = [state]
            self.user_info["possible_states"] = possible_states

    def take_action(self, action):
        if action == "CLEAN_SLOT":
            for slot in self.slot_templet_info:
                if slot in self.user_info:
                    del self.user_info[slot]
        print('系统指令:', action)

    def get_actions(self):
        state = self.user_info['state']
        actions = self.state_info[state].get("actions", [])
        for action in actions:
            self.take_action(action)

    def policy_making(self, user_info, state_info, slot_templet_info):
        self.user_info = user_info
        self.state_info = state_info
        self.slot_templet_info = slot_templet_info

        needed_slots = self.user_info["needed_slots"]
        # 如果槽位已经足够了可以直接回应
        if not needed_slots:
            self.user_info["policy"] = "response"
            self.get_possible_state()
            self.get_actions()
        # 不然就可能的状态还是当前状态，接着填槽
        else:
            slot = needed_slots[0]
            self.get_possible_state(False)
            self.user_info["policy"] = "need:%s" % slot


def pm(user_info, state_info, slot_templet_info):
    po = PM()
    po.policy_making(user_info, state_info, slot_templet_info)
    return po.user_info


if __name__ == '__main__':
    user_info = {'possible_states': ['重填挂号信息'],
                 'query': '错了',
                 'state': '重填挂号信息',
                 'next_score': 1.0,
                 '#性别#': '男',
                 '#年龄#': '22',
                 'needed_slots': [],
                 'needed_slots_state': '重填挂号信息',
                 'policy': 'response'}

    state_info = {'填入挂号信息': {'state': '填入挂号信息',
                             'intents': ['我想要来医院挂号'],
                             'slot': ['#性别#', '#年龄#'],
                             'response': '系统消息:\n好的，请确认您的性别年龄：性别:#性别#;年龄:#年龄#',
                             'possible_states': ['支付挂号费', '重填挂号信息']},
                  '重填挂号信息': {'state': '重填挂号信息',
                             'intents': ['性别年龄信息有误', '重新输入', '错了有问题'],
                             'actions': ['CLEAN_SLOT'],
                             'response': '系统消息:\n好的，为您清楚当前信息，请重新输入挂号信息',
                             'possible_states': ['填入挂号信息']},
                  '确认挂号信息': {'state': '确认挂号信息',
                             'intents': ['确认'],
                             'response': '系统消息:\n好的',
                             'possible_states': ['支付挂号费']},
                  '支付挂号费': {'state': '支付挂号费',
                            'intents': ['确认'],
                            'actions': ['假装返回一个支付二维码链接:https://www.pleasepayyourbill.com/your_info'],
                            'response': '系统消息:\n请支付5元挂号费，支付后请刷新',
                            'possible_states': ['挂号成功']},
                  '挂号成功': {'state': '挂号成功',
                           'intents': ['刷新'],
                           'actions': ['假装将号码信息录入挂号系统:https://www.guahao.com/your_info'],
                           'response': '系统消息:\n您的排队号码为xx,祝您身体健康,万事如意',
                           'possible_states': []}}

    slot_templet_info = {'#性别#': ['请问您的性别为', '男|女'], '#年龄#': ['请问您的年龄为', '(\\d+)']}

    user_info = pm(user_info, state_info, slot_templet_info)
    print(user_info)
