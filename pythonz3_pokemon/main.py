from z3 import *
import calculate

"""
自分のポケモンのステータス
"""
# bs = base stats, ev = effort value

# ニャオハ
pokemon_main_bs = {"h_bs": 40, "a_bs": 61, "b_bs": 54, "c_bs": 45, "d_bs": 45, "s_bs": 65}
h_ev = Int("h_ev")
a_ev = Int("a_ev")
b_ev = Int("b_ev")
c_ev = Int("c_ev")
d_ev = Int("d_ev")
s_ev = Int("s_ev")
pokemon_me_type = {"type1": "grass", "type2": None}


"""
敵のポケモンのステータス
"""
# ピカチュウ
pokemon_opposite1_bs = {"h_bs": 35, "a_bs": 55, "b_bs": 40, "c_bs": 50, "d_bs": 50, "s_bs": 90}
pokemon_opposite1_ev = {"h_ev": 0, "a_ev": 252, "b_ev": 0, "c_ev": 0, "d_ev": 0, "s_ev": 252}
pokemon_opposite1_type = {"type1": "electric", "type2": None}

# 努力値の制限
s = Solver()
s.add(0 <= h_ev, h_ev <= 252, h_ev % 4 == 0)
s.add(0 <= a_ev, a_ev <= 252, a_ev % 4 == 0)
s.add(0 <= b_ev, b_ev <= 252, b_ev % 4 == 0)
s.add(0 <= c_ev, c_ev <= 252, c_ev % 4 == 0)
s.add(0 <= d_ev, d_ev <= 252, d_ev % 4 == 0)
s.add(0 <= s_ev, s_ev <= 252, s_ev % 4 == 0)
s.add((h_ev + a_ev + b_ev + c_ev + d_ev + s_ev) <= 508)

attack_move_sample = 100


"""
攻撃を受けるとき
"""
# 自ポケモンの体力を計算
pokemon_me_stats_hp = calculate.calculate_hp(h_ev, pokemon_main_bs["h_bs"])

# 自ポケモンの防御力を計算
pokemon_me_stats_b = calculate.calculate_hpother(b_ev, pokemon_main_bs["b_bs"])

# 敵ポケモンの攻撃力を計算
pokemon_opposite1_stats_a = calculate.calculate_hpother(pokemon_opposite1_ev["a_ev"], pokemon_opposite1_bs["a_bs"])

# ダメージ計算
# 10万ボルト
attack_move = {"power": 90, "type": "electric"}
damage = calculate.calculate_damage(
    attack_move["power"], attack_move["type"], pokemon_opposite1_type["type1"], pokemon_opposite1_type["type2"], pokemon_me_type["type1"], pokemon_me_type["type2"], pokemon_opposite1_stats_a, pokemon_me_stats_b)

# 条件を追加
s.add(pokemon_me_stats_hp - damage > 0)


"""
特殊攻撃を受けるとき
"""
# 自ポケモンの体力を計算
pokemon_me_stats_hp = calculate.calculate_hp(h_ev, pokemon_main_bs["h_bs"])

# 自ポケモンの特殊防御力を計算
pokemon_me_stats_d = calculate.calculate_hpother(d_ev, pokemon_main_bs["d_bs"])

# 敵ポケモンの特殊攻撃力を計算
pokemon_opposite1_stats_c = calculate.calculate_hpother(pokemon_opposite1_ev["c_ev"], pokemon_opposite1_bs["c_bs"])

# ダメージ計算
#damage = calculate.calculate_damage(attack_move_sample, pokemon_opposite1_stats_c, pokemon_me_stats_d)

# 条件を追加
#s.add(pokemon_me_stats_hp - damage > 0)


"""
攻撃を与えるとき
"""
# 自ポケモンの攻撃力を計算
pokemon_me_stats_attack = calculate.calculate_hpother(a_ev, pokemon_main_bs["a_bs"])

# 敵ポケモンのHPを計算
pokemon_opposite1_stats_h = calculate.calculate_hp(pokemon_opposite1_ev["h_ev"], pokemon_opposite1_bs["h_bs"])

# 敵ポケモンの防御力を計算
pokemon_opposite1_stats_b = calculate.calculate_hpother(pokemon_opposite1_ev["b_ev"], pokemon_opposite1_bs["b_bs"])

# ポケモンに与えるダメージを計算
#damage = calculate.calculate_damage(attack_move_sample, pokemon_me_stats_attack, pokemon_opposite1_stats_b)

# 条件を追加
#s.add(pokemon_opposite1_stats_h - damage <= 0)
#s.add(c_ev == 0)


"""
特殊攻撃を与えるとき
"""


"""
素早さの比較
"""
# 自ポケモンの素早さを計算
pokemon_me_stats_s = calculate.calculate_hpother(s_ev, pokemon_main_bs["s_bs"])

# 敵ポケモンの素早さを計算
pokemon_opposite1_stats_s = calculate.calculate_hpother(pokemon_opposite1_ev["s_ev"], pokemon_opposite1_bs["s_bs"])

# 条件を追加
s.add(pokemon_me_stats_s > pokemon_opposite1_stats_s)


"""
解があるか確かめる
"""

if s.check() == sat:
    # 解の表示
    m = s.model()
    print(m)

    # 解を制約条件に追加
    s.add(Not(And(h_ev == m[h_ev], a_ev == m[a_ev], b_ev == m[b_ev], c_ev == m[c_ev], d_ev == m[d_ev], s_ev == m[s_ev])))
else:
    print("failed to solve")

# 解を取得
# ans_p = is_true(m[p])
"""

# 解を探索
while(s.check() == sat):
    # 解の表示
    m = s.model()
    print(m)

    # 解を制約条件に追加
    s.add(Not(And(h_ev == m[h_ev], a_ev == m[a_ev], b_ev == m[b_ev], c_ev == m[c_ev], d_ev == m[d_ev], s_ev == m[s_ev])))
"""

