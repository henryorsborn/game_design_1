class AttackEffect(object):

    def __init__(self, type_: str, args_: str):
        self.type_ = type_
        if self.type_ == "stat":
            self.args = args_.split("|")
        else:
            self.args = int(args_)
