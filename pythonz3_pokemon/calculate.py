import type_table

# レベル50統一、ダメージ計算
def calculate_damage(attack_move_power, attack_move_type, attack_pokemon_type1, attack_pokemon_type2, defense_pokemon_type1, defense_pokemon_type2, attack_stats, defense_stats):
    damage1 = 22 * attack_move_power * attack_stats / defense_stats
    # もとのダメージ
    damage = damage1 / 50 + 2
    # ここにタイプ相性を入れる
    magnification = type_compatibility(attack_move_type, attack_pokemon_type1, attack_pokemon_type2, defense_pokemon_type1, defense_pokemon_type2)
    damage = damage * magnification
    return damage

## ポケモンのHPを計算
# 個体値 = 31, level = 50
def calculate_hp(ev, bs):
    stats = (bs * 2 + 31 + ev / 4) / 2 + 60
    return stats

## ポケモンのHP以外の能力を計算
def calculate_hpother(ev, bs):
    stats = (bs * 2 + 31 + ev / 4) / 2 + 5
    return stats

## ポケモンのタイプ相性の判断
def type_compatibility(attack_move_type, attack_pokemon_type1, attack_pokemon_type2, defense_pokemon_type1, defense_pokemon_type2):
    # 威力の倍率
    val = 1
    # タイプ一致なら1.5倍
    if attack_move_type == (attack_pokemon_type1 or attack_pokemon_type2):
        print("タイプ一致!")
        val = val * 3/2

    for i in range(18):
        if defense_pokemon_type1 == type_table.type_table[i][1]:
            defense_pokemon_type1_id = type_table.type_table[i][0]
            break
    if defense_pokemon_type2 != None:
        for i in range(18):
            if defense_pokemon_type2 == type_table.type_table[i][1]:
                defense_pokemon_type2_id = type_table.type_table[i][0]
                break
    
    for i in range(18):
        if attack_move_type == type_table.type_table[i][1]:
            val1 = type_table.type_table[i][defense_pokemon_type1_id + 1]
            val = val * val1
            if defense_pokemon_type2 != None:
                val2 = type_table.type_table[i][defense_pokemon_type2_id + 1]
                val = val * val2
            break
    print("攻撃力" + str(val) + "倍!")
    return val