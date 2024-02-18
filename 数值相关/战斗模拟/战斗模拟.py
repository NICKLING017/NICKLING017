import math
import pandas as pd
from collections import defaultdict

# 伤害系数
DAMAGE_COEFFICIENT = 200
# 设置最大回合数
MAX_ROUNDS = 50

# 创建兵种克制系数映射表
restraint_coefficients = {
    ("infantry", "infantry"): 1,
    ("infantry", "archers"): 0.95,
    ("infantry", "cavalry"): 1.05,
    ("infantry", "charioteers"): 1.15,
    ("archers", "infantry"): 1.05,
    ("archers", "archers"): 1,
    ("archers", "cavalry"): 0.95,
    ("archers", "charioteers"): 1.15,
    ("cavalry", "infantry"): 0.95,
    ("cavalry", "archers"): 1.05,
    ("cavalry", "cavalry"): 1,
    ("cavalry", "charioteers"): 1.15,
    ("charioteers", "infantry"): 1,
    ("charioteers", "archers"): 1,
    ("charioteers", "cavalry"): 1,
    ("charioteers", "charioteers"): 1
}


class Troop:
    def __init__(self, name):
        self.name = name
        self.units = []

    def add_unit(self, unit, quantity):
        self.units.append({'unit': unit, 'quantity': quantity})

    def remove_unit(self, unit, quantity):
        self.units.remove({'unit': unit, 'quantity': quantity})

    def update_unit_quantity(self, unit, new_quantity):
        for unit_info in self.units:
            if unit_info['unit'].unit_type == unit.get_unit_type() and unit_info['unit'].level == unit.level:
                unit_info['quantity'] = new_quantity
                break

    def get_unit_quantity(self, unit_type, unit_level):
        for unit_info in self.units:
            if unit_info['unit'].unit_type == unit_type.get_unit_type() and unit_info['unit'].level == unit_level:
                return unit_info['quantity']
        return 0  # 如果找不到对应的部队信息，则返回默认数量（这里假设为0）

    def get_average_attribute(self, unit_type, attribute):
        # 获取士兵平均属性
        total_value = 0
        total_quantity = 0
        for unit_info in self.units:
            unit = unit_info['unit']
            quantity = unit_info['quantity']
            if unit.unit_type == unit_type:
                if attribute == 'attack':
                    total_value += unit.attack * quantity
                elif attribute == 'defence':
                    total_value += unit.defence * quantity
                elif attribute == 'hp':
                    total_value += unit.hp * quantity

                total_quantity += quantity

        if total_quantity == 0:
            return 0
        else:
            return total_value / total_quantity

    def get_unit_type_counts(self):
        """
        获取军团中各类兵种的士兵数量

        Returns:
            dict: 包含各类兵种士兵数量的字典
        """
        unit_type_counts = {}

        for unit_info in self.units:
            unit = unit_info['unit']
            quantity = unit_info['quantity']
            unit_type = unit.unit_type

            # 计算每类兵种的士兵数量
            if unit_type in unit_type_counts:
                unit_type_counts[unit_type] += quantity
            else:
                unit_type_counts[unit_type] = quantity

        return unit_type_counts


class BaseUnit:
    def get_unit_type(self):
        raise NotImplementedError

    def __init__(self, unit_type, level, attributes):
        self.unit_type = unit_type
        self.level = level

        # 根据兵种等级从字典中获取对应属性
        if level in attributes:
            unit_attributes = attributes[level]
            self.attack = unit_attributes['attack']
            self.defence = unit_attributes['defence']
            self.hp = unit_attributes['hp']
            self.load = unit_attributes['load']
            self.power = unit_attributes['power']
            self.speed = unit_attributes['speed']
        else:
            raise ValueError(f"Invalid {unit_type} level: {level}")


class Infantry(BaseUnit):  # 步兵
    def __init__(self, level):
        infantry_attributes = infantry_attributes_excel
        super().__init__("infantry", level, infantry_attributes)
        self.type = "infantry"

    def get_unit_type(self):
        return 'infantry'


class Cavalry(BaseUnit):  # 骑兵
    def __init__(self, level):
        cavalry_attributes = cavalry_attributes_excel
        super().__init__("cavalry", level, cavalry_attributes)
        self.type = "cavalry"

    def get_unit_type(self):
        return 'cavalry'


class Archers(BaseUnit):  # 弓兵
    def __init__(self, level):
        archers_attributes = archers_attributes_excel
        super().__init__("archers", level, archers_attributes)
        self.type = "archers"

    def get_unit_type(self):
        return 'archers'


class Charioteers(BaseUnit):  # 车兵
    def __init__(self, level):
        charioteers_attributes = charioteers_attributes_excel
        super().__init__("charioteers", level, charioteers_attributes)
        self.type = "charioteers"

    def get_unit_type(self):
        return 'charioteers'


# 计算伤害
# calculate_damage(攻击方军团, 防御方军团, 攻击方士兵类型, 防御方士兵类型, 攻击方总兵力,攻击方士兵数量字典, 伤害参数)
def calculate_damage(attacker, defender, attacker_unit_type, defender_unit_type, attacker_total_soldiers,
                     attacker_results, damage_coefficient):
    attacker_attack = attacker.get_average_attribute(attacker_unit_type, "attack")
    defender_defence = defender.get_average_attribute(defender_unit_type, "defence")

    # 根据兵种判断克制系数
    if (attacker_unit_type, defender_unit_type) in restraint_coefficients:
        restraint_coefficient = restraint_coefficients[(attacker_unit_type, defender_unit_type)]
    else:
        restraint_coefficient = 1  # 默认克制系数

    if defender_defence == 0:
        return 0
    else:
        attacker_results_key = f"{attacker.name}_{attacker_unit_type}_vs_{defender_unit_type}_count"
        attacker_results_value = attacker_results.get(attacker_results_key, 0)
        damage = 0
        if attacker_results_value != 0:
            damage = (attacker_attack / defender_defence) * damage_coefficient * \
                     math.sqrt(attacker_total_soldiers) * \
                     attacker_results_value / attacker_total_soldiers * restraint_coefficient

        return math.ceil(damage)


# 计算总伤害 每个回合结束之后都要重新计算
def calculate_total_damage(attacker_unit_types, defender_unit_types, attacker, defender, attacker_total_soldiers,
                           attacker_results):
    defender_total_damage = {
        'infantry': 0,
        'archers': 0,
        'cavalry': 0,
        'charioteers': 0
    }

    for defender_unit_type in defender_unit_types:
        for attacker_unit_type in attacker_unit_types:
            damage = calculate_damage(attacker, defender, attacker_unit_type, defender_unit_type,
                                      attacker_total_soldiers, attacker_results, DAMAGE_COEFFICIENT)
            defender_total_damage[defender_unit_type] += damage
    return defender_total_damage  # 返回各兵种受到的总伤害


# 计算死兵数量 每个回合结束之后都要重新计算
def calculate_dead_count(damage, troop, unit_type):
    dead_count = {}  # 用于存储不同等级士兵的死亡人数
    total_hp = 0

    # 获取军团中特定类型士兵的信息
    for unit in troop.units:
        if unit['unit'].type == unit_type:
            level = unit['unit'].level
            quantity = troop.get_unit_quantity(globals()[unit_type.capitalize()](level), level)
            unit_hp = unit['unit'].hp
            total_hp += quantity * unit_hp

    for unit in troop.units:
        if unit['unit'].type == unit_type:
            level = unit['unit'].level
            unit_hp = unit['unit'].hp

            if damage == 0 or unit_hp == 0:
                if unit_type not in dead_count:
                    dead_count[unit_type] = {}
                dead_count[unit_type][level] = 0
            else:
                # 计算伤害对应的死亡人数
                quantity = troop.get_unit_quantity(globals()[unit_type.capitalize()](level), level)
                proportion = (quantity * unit_hp) / total_hp
                if unit_type not in dead_count:
                    dead_count[unit_type] = {}
                dead_count[unit_type][level] = math.ceil(damage * proportion / unit_hp)

    return dead_count


# 军团信息打印
def print_troop_info(troop):
    print(troop.name)
    for unit_info in troop.units:
        unit = unit_info['unit']
        quantity = unit_info['quantity']
        print(
            f"{unit.unit_type}\t等级:{unit.level}\t数量:{quantity}\t攻击力:{unit.attack}\t防御力:{unit.defence}\t生命值:{unit.hp}\t负载力:{unit.load}\t")
    for unit_type in unit_types:
        average_attack = troop.get_average_attribute(unit_type, "attack")
        average_defence = troop.get_average_attribute(unit_type, "defence")
        average_hp = troop.get_average_attribute(unit_type, "hp")
        print(f"{troop.name}_{unit_type}的平均攻击力：", average_attack)
        print(f"{troop.name}_{unit_type}的平均防御力：", average_defence)
        print(f"{troop.name}_{unit_type}的平均生命值：", average_hp)
    print("\n")
    troop_proportions = troop.get_unit_type_counts()
    infantry_count = troop_proportions.get('infantry', 0)
    archers_count = troop_proportions.get('archers', 0)
    cavalry_count = troop_proportions.get('cavalry', 0)
    charioteers_count = troop_proportions.get('charioteers', 0)

    print(f"{troop.name}步兵的数量：", infantry_count)
    print(f"{troop.name}弓兵的数量：", archers_count)
    print(f"{troop.name}骑兵的数量：", cavalry_count)
    print(f"{troop.name}车兵的数量：", charioteers_count)
    print("\n")


# 军团兵力和士兵占比计算 每个回合结束之后都要重新计算
def calculate_troop_stats(troop):
    total_soldiers = sum(unit_info['quantity'] for unit_info in troop.units)
    if total_soldiers == 0:
        return 0, {}  # 返回零士兵数量和空的兵种统计字典

    infantry_proportion = troop.get_unit_type_counts().get('infantry', 0) / total_soldiers
    archers_proportion = troop.get_unit_type_counts().get('archers', 0) / total_soldiers
    cavalry_proportion = troop.get_unit_type_counts().get('cavalry', 0) / total_soldiers
    charioteers_proportion = troop.get_unit_type_counts().get('charioteers', 0) / total_soldiers

    units = {
        'infantry': {
            'count': troop.get_unit_type_counts().get('infantry', 0),
            'proportion': infantry_proportion
        },
        'archers': {
            'count': troop.get_unit_type_counts().get('archers', 0),
            'proportion': archers_proportion
        },
        'cavalry': {
            'count': troop.get_unit_type_counts().get('cavalry', 0),
            'proportion': cavalry_proportion
        },
        'charioteers': {
            'count': troop.get_unit_type_counts().get('charioteers', 0),
            'proportion': charioteers_proportion
        }
    }

    return total_soldiers, units


# 确定交战分兵结果 每个回合结束之后都要重新计算
def calculate_troop_vs_troop_results(attacking_troop, defending_troop):
    results = {}

    for unit1, count1 in attacking_troop.items():
        for unit2, proportion2 in defending_troop.items():
            count_vs_unit2 = math.ceil(count1['count'] * proportion2['proportion'])
            key1 = f"{attacking_troop.name}_{unit1}_vs_{unit2}_count"
            results[key1] = count_vs_unit2

    for unit2, count2 in defending_troop.items():
        for unit1, proportion1 in attacking_troop.items():
            count_vs_unit1 = math.ceil(count2['count'] * proportion1['proportion'])
            key2 = f"{defending_troop.name}_{unit2}_vs_{unit1}_count"
            results[key2] = count_vs_unit1

    return results


# 伤兵计算和军团信息更新 每个回合结束之后都要重新计算
def update_troop_after_battle(troop, damage_received):
    # 定义所有可能的单位类型
    unit_types = ['infantry', 'archers', 'cavalry', 'charioteers']
    # 存储每个单位类型的伤亡情况
    casualties_by_unit_type = {}
    print(troop.name)
    # 计算每个单位类型的伤亡情况
    for unit_type in unit_types:
        damage = damage_received[unit_type]
        print(calculate_dead_count(damage, troop, unit_type))
        casualties_by_unit_type[unit_type] = calculate_dead_count(damage, troop, unit_type)

    # 遍历每个单位类型的伤亡情况
    for unit_type, unit_type_casualties in casualties_by_unit_type.items():
        for unit_type, casualty_count_dict in unit_type_casualties.items():
            for level, count in casualty_count_dict.items():
                if count > 0:
                    # 根据单位类型和等级创建相应等级的兵种对象
                    unit = globals()[unit_type.capitalize()](level)
                    # 获取当前数量
                    current_quantity = troop.get_unit_quantity(unit, level)
                    new_quantity = max(current_quantity - count, 0)
                    troop.update_unit_quantity(unit, new_quantity)


# 战斗流程
def battle_loop(troop1, troop2, max_rounds):
    for round_num in range(1, max_rounds + 1):
        print(f"Round {round_num}:")

        # 准备回合
        troop1_results = {}
        troop2_results = {}

        troop1_total_soldiers, troop1_units = calculate_troop_stats(troop1)
        troop2_total_soldiers, troop2_units = calculate_troop_stats(troop2)

        # 计算 troop1 对 troop2 的结果
        for unit1, count1 in troop1_units.items():
            for unit2, proportion2 in troop2_units.items():
                count_vs_unit2 = math.ceil(count1['count'] * proportion2['proportion'])
                key1 = f"troop1_{unit1}_vs_{unit2}_count"
                troop1_results[key1] = count_vs_unit2

        # 计算 troop2 对 troop1 的结果
        for unit2, count2 in troop2_units.items():
            for unit1, proportion1 in troop1_units.items():
                count_vs_unit1 = math.ceil(count2['count'] * proportion1['proportion'])
                key2 = f"troop2_{unit2}_vs_{unit1}_count"
                troop2_results[key2] = count_vs_unit1

        # 各兵种承受伤害计算
        troop1_get_damage = calculate_total_damage(unit_types, unit_types,
                                                   troop2, troop1, troop2_total_soldiers, troop2_results)
        troop2_get_damage = calculate_total_damage(unit_types, unit_types,
                                                   troop1, troop2, troop1_total_soldiers, troop1_results)

        # 伤兵计算和军团信息更新
        update_troop_after_battle(troop1, troop1_get_damage)
        update_troop_after_battle(troop2, troop2_get_damage)

        # 打印本回合的战斗结果和军团信息
        print("troop1_results\n", troop1_results)
        print("troop2_results\n", troop2_results)
        print("troop1_units\n", troop1_units)
        print("troop2_units\n", troop2_units)
        print("troop1_get_damage\n", troop1_get_damage)
        print("troop2_get_damage\n", troop2_get_damage)

        # 判断终止条件，例如士兵数量是否小于某个值
        if troop1_total_soldiers <= 0 or troop2_total_soldiers <= 0:
            print("Battle ended!")
            break


def load_unit_attributes_from_excel(file_path, unit_type):
    # 从 Excel 文件中加载属性数据
    df = pd.read_excel(file_path, sheet_name='属性')

    # 创建一个默认字兵种类型分组数据的字典
    unit_attributes = defaultdict(dict)

    # 遍历 DataFrame 中的每一行，按兵种类型和等级构建嵌套字典
    for index, row in df.iterrows():
        current_unit_type = row['unit_type']
        if current_unit_type == unit_type:
            level = row['level']

            # 构建属性字典
            attributes = {
                'attack': row['attack'],
                'defence': row['defence'],
                'hp': row['hp'],
                'speed': row['speed'],
                'load': row['load'],
                'power': row['power']
            }

            # 将属性字典添加到兵种类型和等级的嵌套字典中
            unit_attributes[unit_type][level] = attributes

    # 返回相应兵种的属性字典
    return unit_attributes[unit_type]


unit_types = {'infantry', 'cavalry', 'archers', 'charioteers'}
############################################################################
# main.py

# 调用函数加载兵种属性数据
infantry_attributes_excel = load_unit_attributes_from_excel('战斗测试.xlsx', 'infantry')
archers_attributes_excel = load_unit_attributes_from_excel('战斗测试.xlsx', 'archers')
cavalry_attributes_excel = load_unit_attributes_from_excel('战斗测试.xlsx', 'cavalry')
charioteers_attributes_excel = load_unit_attributes_from_excel('战斗测试.xlsx', 'charioteers')

# 创建军团
troop1 = Troop("troop1")
troop2 = Troop("troop2")

# 添加不同等级和数量的兵种到军团中 之后和excel关联
troop1.add_unit(Infantry(1), 100)

troop2.add_unit(Infantry(1), 100)
############################################################################
# 打印军团信息和平均属性值
troops = [troop1, troop2]
for troop in troops:
    print_troop_info(troop)
print("###########战斗开始!###########")
# 开始战斗循环
battle_loop(troop1, troop2, MAX_ROUNDS)

print("###########战斗结束!###########")
for troop in troops:
    print_troop_info(troop)
