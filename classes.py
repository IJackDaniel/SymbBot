class Order:
    def __init__(self):
        self.category = ""
        self.sub_category = ""
        self.properties = ""

    def clean(self):
        self.category = ""
        self.sub_category = ""
        self.properties = ""

    def set_category(self, inp):
        inp = str(inp)
        self.category = inp

    def get_category(self):
        return self.category

    def set_sub_category(self, inp):
        inp = str(inp)
        self.sub_category = inp

    def get_sub_category(self):
        return self.sub_category

    def set_properties(self, inp):
        inp = str(inp)
        self.properties = inp

    def get_properties(self):
        return self.properties

    def show(self):
        print(f"Категория: {self.category}\nПодкатегория: {self.sub_category}\nСвойства:\n{self.properties}\n")
