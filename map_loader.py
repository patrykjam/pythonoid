import json
from pprint import pprint
from block import Block


class Map_Loader(object):
    def __init__(self):
        with open('mapy.json', encoding='utf-8') as data_file:
            data = json.load(data_file)
            self.blocks = data["blocks"]
            self.maps = data["maps"]
            self.title = "None"
        self.level = -1

    def next_map(self):
        if len(self.maps) - 1 > self.level:
            self.level += 1
            self.title = self.maps[self.level]["title"]
            return self.level
        return None

    def get_blocks(self):
        return [Block(block["x"], block["y"], *self.blocks[block["kind"]]) for block in self.maps[self.level]["blocks"]]


