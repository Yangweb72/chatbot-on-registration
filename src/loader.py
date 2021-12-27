import json
import pandas as pd


class Loader:
    def __init__(self, config):
        self.slot_templet_info = {}
        self.state_info = {}
        self.config = config
        self.load()

    # 加载信息
    def load(self):
        self.load_slot_template(self.config['slot_template_path'])
        self.load_state(self.config['state_path'])
        print('''
        欢迎使用医院自助问答系统系统
           请问您想做些什么呢？''')
    # 加载对话状态
    def load_state(self, path):
        with open(path, encoding="utf8") as f:
            state_list = json.loads(f.read())
            for state_info in state_list:
                state_name = state_info["state"]
                self.state_info[state_name] = state_info

    # 加载槽模板
    def load_slot_template(self, path):
        df = pd.read_excel(path)
        for index in range(len(df)):
            slot = df["slots"][index]
            values = df["values"][index]
            query = df["queries"][index]
            self.slot_templet_info[slot] = [query, values]


def load_schema(config):
    shcema = Loader(config)
    return shcema.state_info, shcema.slot_templet_info


if __name__ == '__main__':
    import sys

    sys.path.append("..")
    from config import config

    config['slot_template_path'] = '../slot_template.xlsx'
    config['state_path'] = '../register_states.json'

    state_info, slot_templet_info = load_schema(config)
