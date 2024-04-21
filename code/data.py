class Data:
    def __init__(self, ui):
        self.ui = ui
        self._coins = 0
        self._health = 5
        self._jacket_collected = False
        self._backpack_collected = False
        self._win = False
        self.ui.create_hearts(self._health)
        

        self.unlocked_level = 0
        self.current_level = 0

    @property
    def coins(self):
        return self._coins

    @coins.setter
    def coins(self, amount):
        self._coins = amount
        if self.coins >= 100:
            self.coins -= 100
            self.health += 1
        self.ui.show_coins(self.coins)

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value
        self.ui.create_hearts(value)

    @property
    def jacket_collected(self):
        return self._jacket_collected

    @jacket_collected.setter
    def jacket_collected(self, boolean):
        self._jacket_collected = boolean
        self.health += 1
        self.ui.show_jacket(self.jacket_collected)

    @property
    def backpack_collected(self):
        return self._backpack_collected

    @backpack_collected.setter
    def backpack_collected(self, boolean):
        self._backpack_collected = boolean
        self.health += 1
        self.ui.show_backpack(self.backpack_collected)

    @property
    def win(self):
        return self._win

    @win.setter
    def win(self, boolean):
        self._win = boolean
