from random import sample
class TwoMix():
    def __init__(self):
        self.acid = ['зеленое яблоко', 'грейпфрут', 'лимон', 'вишня', 'апельсин',
                     'ананас', 'кола', 'виноград', 'клюква', 'бузина']
        self.sweet = ['дыня', 'арбуз', 'малина', 'банан', 'персик', 'ананас', 'клубника', 'киви', 'ежевика']
        self.candy = ['груша', 'печенье', 'шоколад', 'банан', 'ваниль', 'черника', 'чизкейк', 'малина', 'орех']
        self.percentages = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
        self.mix = []
        self.calc = []

    def get_mix_two(self, question):
        """Сколько вкусов в миксе"""
        if question == 'кислый':
            acid_copy = self.acid[:]
            self.mix = sample(acid_copy, 2)
        elif question == 'сладкий':
            sweet_copy = self.sweet[:]
            self.mix = sample(sweet_copy, 2)
        elif question == 'выпечка':
            candy_copy = self.candy[:]
            self.mix = sample(candy_copy, 2)
        return self.mix

    def calc_precent_two(self):
        """Считаем 100% для двух вкусов"""
        while True:
            nums = sample(self.percentages, 2)
            if sum(nums) == 100:
                break
        for num in sorted(nums, reverse=True):
            self.calc.append(num)

    def display_flavor(self):
        """Отображение микса"""
        result = "Микс состоит из:"
        for i in range(len(self.mix)):
            flavor = self.mix[i]
            proc = self.calc[i]
            result += f"\n{flavor} - {proc}%"
        return result

    def question_for_flavor(self, flavor_quest):
        """Передача ответа пользователя функции получения микса + отображение микса"""
        if self.get_mix_two(flavor_quest):
            self.calc_precent_two()
            return self.display_flavor()
        else:
            return "Категория не найдена."


# my_mix = TwoMix()
# flavor_quest = input("Какой вкус добавить? ")
# result = my_mix.question_for_flavor(flavor_quest)
# print(result)
