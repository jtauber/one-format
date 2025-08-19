from collections import defaultdict, namedtuple


class Ref:
    def __init__(self, value):
        self.raw = value
        if "-" in value:
            self.start, self.end = value.split("-")

    def __eq__(self, other):
        if isinstance(other, Ref):
            return self.raw == other.raw
        return False


def wrap(col_name, value):
    if col_name.endswith("_ref"):
        return Ref(value)
    else:
        return value


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
            row = Row(
                *[
                    wrap(col_name, value)
                    for (col_name, value) in zip(
                        self.header, line.rstrip("\n").split("\t")
                    )
                ]
            )
            self.data.append(row)
            for col_num, col_name in enumerate(self.header):
                if col_name.endswith("_id"):
                    self.index[col_name][row[col_num]] = row_num

    def get(self, **kwargs):
        assert len(kwargs) == 1  # for now
        col_name, value = list(kwargs.items())[0]
        assert col_name.endswith("_id")  # for now
        return self.data[self.index[col_name][value]]

    def rows(self, **kwargs):
        assert len(kwargs) == 1  # for now
        col_name, value = list(kwargs.items())[0]
        assert col_name.endswith("_ref")  # for now
        col_name = col_name[:-4] + "_id"
        assert isinstance(value, Ref)
        if "-" in value.raw:
            start = self.index[col_name][value.start]
            end = self.index[col_name][value.end]
            return self.data[start : end + 1]
        else:
            return [self.data[self.index[col_name][value.raw]]]

    def frag(self, field="text", **kwargs):
        assert len(kwargs) == 1  # for now
        col_name, value = list(kwargs.items())[0]
        assert col_name.endswith("_ref")  # for now
        col_name = col_name[:-4] + "_id"
        assert isinstance(value, Ref)
        # can currently only handle foo#bar-#baz
        assert value.raw.count("-")
        assert value.raw.count("#") == 2
        block_ref = value.start.split("#")[0]
        start_char_offset = int(value.start.split("#")[1])
        end_char_offset = int(value.end.split("#")[1])
        row = self.data[self.index[col_name][block_ref]]
        return getattr(row, field)[start_char_offset : end_char_offset + 1]
