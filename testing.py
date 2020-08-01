from fish_map import MAP

def print_self(s):
    print(repr(s))
    return

def __repr__(self):
        s = "---FISH---\n"
        s += "state = {}\n".format(self.state)
        s += "pos = {:.3f}, {:.3f}\n".format(self.pos.x, self.pos.y)
        s += "traits = {}\n".format("{" + ", ".join(["{}: {}".format(k, str(round(v, 3))) for k, v in self.traits.items()]) + "}")
        s += "----------"
        return s