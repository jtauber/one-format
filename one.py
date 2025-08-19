from collections import defaultdict, namedtuple

class One:
    def __init__(self, file_path):
        self.file_path = file_path
        self.load_data()

    def load_data(self):
        lines = open(self.file_path).readlines()
        self.header = lines[0].rstrip("\n").split("\t")
        Row = namedtuple("Row", self.header)
        self.data = []
        self.index = defaultdict(dict)
        for row_num, line in enumerate(lines[1:]):
            row = Row(*line.rstrip("\n").split("\t"))
            self.data.append(row)
            for col_num, col_name in enumerate(self.header):
                if col_name.endswith("_id"):
                    self.index[col_name][row[col_num]] = row_num

    def get(self, **kwargs):
        assert len(kwargs) == 1  # for now
        col_name, value = list(kwargs.items())[0]
        assert col_name.endswith("_id")  # for now
        return self.data[self.index[col_name][value]]
