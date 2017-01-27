def get(self):
    if self.data_type == 0:
        return self.float_value
    if self.data_type == 1:
        return self.int_value
    if self.data_type == 2:
        return self.text_value


def set(self, value):
    self.modified_date = datetime.now()
    if value == '':
        value = get_default_value(self.data_type)
    if self.data_type == 0:
        self.float_value = value
        return
    if self.data_type == 1:
        self.int_value = value
        return
    if self.data_type == 2:
        self.text_value = value
        return