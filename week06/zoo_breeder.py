# 作业背景：在使用 Python 进行《我是动物饲养员》这个游戏的开发过程中，有一个代码片段要求定义动物园、动物、猫、狗四个类。
# 这个类可以使用如下形式为动物园增加一只猫：
# if __name__ == '__main__':
#     # 实例化动物园
#     z = Zoo('时间动物园')
#     # 实例化一只猫，属性包括名字、类型、体型、性格
#     cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
#     # 增加一只猫到动物园
#     z.add_animal(cat1)
#     # 动物园是否有猫这种动物
#     have_cat = hasattr(z, 'Cat')
# 具体要求：
# 定义“动物”、“猫”、“狗”、“动物园”四个类，动物类不允许被实例化。
# 动物类要求定义“类型”、“体型”、“性格”、“是否属于凶猛动物”四个属性，是否属于凶猛动物的判断标准是：“体型 >= 中等”并且是“食肉类型”同时“性格凶猛”。
# 猫类要求有“叫声”、“是否适合作为宠物”以及“名字”三个属性，其中“叫声”作为类属性，除凶猛动物外都适合作为宠物，猫类继承自动物类。狗类属性与猫类相同，继承自动物类。
# 动物园类要求有“名字”属性和“添加动物”的方法，“添加动物”方法要实现同一只动物（同一个动物实例）不能被重复添加的功能。

from abc import ABCMeta, abstractmethod


class EnumException(BaseException):
    """自定义异常类"""
    pass


class Animal(metaclass=ABCMeta):
    """动物类-抽象基类
        category: 类型，必须三选一：'食肉', '食草', '杂食'
        figure: 体型，必须三选一：'小', '中', '大'
        character: 性格，必须三选一：'凶猛', '温顺', '佛系'
    """
    def __init__(self, category, figure, character):
        self._category = category
        self._figure = figure
        self._character = character
        self.check_category(category)
        self.check_figure(figure)
        self.check_character(character)
    
    @staticmethod
    def check_category(category):
        category_names = ['食肉', '食草', '杂食']
        if category not in category_names:
            raise EnumException(f"参数 category 必须三选一：{category_names}")
        return True
    
    @staticmethod
    def check_figure(figure):
        figure_names = ['小', '中', '大']
        if figure not in figure_names:
            raise EnumException(f"参数 figure 必须三选一：{figure_names}")
        return True
    
    @staticmethod
    def check_character(character):
        character_names = ['凶猛', '温顺', '佛系']
        if character not in character_names:
            raise EnumException(f"参数 character 必须三选一：{character_names}")
        return True
    
    @property
    def category(self):
        return self._category
    
    @property
    def figure(self):
        return self._figure

    @property
    def character(self):
        return self._character
    
    @category.setter
    def category(self, category):
        if self.check_category(category):
            self._category = category

    @figure.setter
    def figure(self, figure):
        if self.check_figure(figure):
            self._figure = figure

    @character.setter
    def character(self, character):
        if self.check_character(character):
            self._character = character

    @property
    def is_beast(self):
        return self.figure in ["中", "大"] and \
            self.category == "食肉" and \
            self.character == "凶猛"
    
    @abstractmethod
    def make_sound(self):
        pass


class Cat(Animal):
    """猫类
    """
    voice = 'miaow...'
    
    def __init__(self, name, category, figure, character):
        super().__init__(category, figure, character)
        self.name = name
        self.id = id(self)
    
    @property
    def is_pet(self):
        return not self.is_beast
    
    def make_sound(self):
        print("make sound:", self.voice)
        
    def __repr__(self):
        return f'<{self.__class__.__name__} object: {self.name}, id: {self.id}>'


class Dog(Animal):
    """狗类
    """
    voice = 'woof...'
    
    def __init__(self, name, category, figure, character):
        super().__init__(category, figure, character)
        self.name = name
        self.id = id(self)
    
    @property
    def is_pet(self):
        return not self.is_beast
    
    def make_sound(self):
        print("make sound:", self.voice)
    
    def __repr__(self):
        return f'<{self.__class__.__name__} object: {self.name}, id: {self.id}>'


class Zoo:
    """动物园类
    """
    def __init__(self, name):
      self.name = name
      self.animal_classes = set()
    
    def add_animal(self, animal):
        if not isinstance(animal, Animal):
            print(f"'{animal}' is not an animal, you can't add it.")
            return
        animal_class_name = animal.__class__.__name__
        if hasattr(self, animal_class_name):
            animal_set = getattr(self, animal_class_name)
        else:
            animal_set = set()
        if animal in animal_set:
            print(f"'{animal}' exists in the zoo, you can't add it again!")
        else:
            animal_set.add(animal)
            self.animal_classes.add(animal.__class__.__name__)
            setattr(self, animal_class_name, animal_set)
            print(f"A new animal '{animal}' has been added to {animal_class_name} category")
    
    def description(self):
        for k,v in self.__dict__.items():
            print(f"{k}: {v}")
    
    def __repr__(self):
        return f'<{self.__class__.__name__} object (animal category: {self.animal_classes})>'


if __name__ == "__main__":
    c = Cat('大花猫', '食草', '小', '温顺') 
    # d = Dog('大狼狗', '食肉', '中', '狂野')
    d = Dog('大狼狗', '食肉', '大', '凶猛')
    # d2 = Dog('小傻狗', '食豆', '小', '温顺')
    d2 = Dog('小傻狗', '杂食', '小', '温顺')
    # c2 = Cat('黑猫', '食肉', '微', '凶猛') 
    c2 = Cat('黑猫', '食肉', '小', '凶猛') 
    print("c.is_beast:", c.is_beast)
    print("c.is_pet:", c.is_pet)
    print("d.is_beast:", d.is_beast)
    print("d.is_pet:", d.is_pet)
    print("c2.is_beast:", c2.is_beast)
    print("c2.is_pet:", c2.is_pet)
    z = Zoo('时间动物园')
    print(z)
    # z.add_animal(2)
    # z.add_animal('哈哈')
    z.add_animal(d)
    z.add_animal(d)
    z.add_animal(d2)
    z.add_animal(c)
    z.add_animal(c)
    z.add_animal(c2)
    have_cat = hasattr(z, 'Cat')
    print(have_cat)
    have_tiger = hasattr(z, 'Tiger')
    print(have_tiger)
    z.description()    
