def dst(user_info, state_info):
    '''dialogue_state_track'''
    state = user_info['state']
    needed_slots = state_info[state].get('slot', [])
    user_info['needed_slots'] = []
    for needed_slot in needed_slots:
        if needed_slot not in user_info:
            user_info['needed_slots'].append(needed_slot)
    user_info['needed_slots_state'] = state  # 记录还需要填槽的状态
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
    user_info = dst(user_info, state_info)
    print(user_info)
