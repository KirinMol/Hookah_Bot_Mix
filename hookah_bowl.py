import random

class HookahBowl():
    def __init__(self):
        self.packs = ['оверпак', 'воздушная', 'плотная', 'с колодцем']
        self.struct = ['слоями', 'секторами']

    def choice_bowl(self, bowl):
        """Выводим забивку чаши исходя из результата пользователя"""
        if bowl == 'турка':
            return self.search_packs()
        elif bowl == 'фанел':
            while True:
                result = self.search_packs()
                if 'с колодцем' not in result:
                    break
            return result
        elif bowl == 'evil':
            while True:
                result = self.search_packs()
                if 'оверпак' not in result:
                    break
            return result

    def search_packs(self):
        """Рандомный выбор забивки"""
        copy_pack = self.packs[:]
        copy_struct = self.struct[:]
        pack = random.choice(copy_pack)
        struc = random.choice(copy_struct)
        result = f"cпособ забивки:\n{pack}, {struc}"
        return result