# main.py
import random
import sys
from grille import Grille
from bateau import PorteAvion, Croiseur, Torpilleur, SousMarin, Bateau

SHIP_CLASSES = [PorteAvion, Croiseur, Torpilleur, SousMarin]

def place_ships_randomement(grille: Grille, ship_classes):
    """
    随机地把每个 ship_class 的一艘船放入 grille（不重叠）。
    返回放置好的船对象列表。
    若放置失败会尝试若干次重试。
    """
    max_attempts = 30
    for attempt in range(max_attempts):
        # 清空格子
        grille.matrice = [grille.vide for _ in range(grille.lignes * grille.colonnes)]
        placed_ships = []
        ok = True
        for cls in ship_classes:
            placed = False
            # 收集可用候选位置
            candidates = []
            for r in range(grille.lignes):
                for c in range(grille.colonnes):
                    for vertical in (False, True):
                        # 构造 temporary 船用于检查
                        tmp = cls(r, c, vertical=vertical)
                        # 检查是否越界或与已放船重叠（不修改实际格子）
                        pos = tmp.positions
                        valid = True
                        for (lr, lc) in pos:
                            if not (0 <= lr < grille.lignes and 0 <= lc < grille.colonnes):
                                valid = False
                                break
                            val = grille.get(lr, lc)
                            if val != grille.vide and val != "x":
                                valid = False
                                break
                        if valid:
                            candidates.append((r, c, vertical))
            if not candidates:
                ok = False
                break
            r, c, vertical = random.choice(candidates)
            new_ship = cls(r, c, vertical=vertical)
            try:
                grille.ajoute(new_ship)
            except ValueError:
                ok = False
                break
            placed_ships.append(new_ship)
        if ok:
            return placed_ships
    raise RuntimeError("无法在给定的格子上随机放置所有船（尝试多次失败）")


def display_for_player(grille: Grille) -> str:
    """把格子中的船标记隐藏成 '.'，只显示命中 'x' 与空格 '.'"""
    rows = []
    for r in range(grille.lignes):
        row_chars = []
        for c in range(grille.colonnes):
            ch = grille.get(r, c)
            if ch == "x":
                row_chars.append("x")
            else:
                row_chars.append(".")
        rows.append("".join(row_chars))
    return "\n".join(rows)


def find_ship_by_cell(ships, ligne, colonne):
    """返回占据 (ligne,colonne) 的船对象（若有），否则返回 None"""
    for s in ships:
        for (l, c) in s.positions:
            if l == ligne and c == colonne:
                return s
    return None


def all_ships_sunk(ships, grille):
    """判断 ships 列表中是否所有船都已沉没"""
    return all(s.coule(grille) for s in ships)


def input_coords(prompt, max_lines, max_cols):
    """读取并解析玩家输入坐标，若输入 q 返回 None"""
    raw = input(prompt).strip()
    if raw.lower() in ("q", "quit", "exit"):
        return None
    parts = raw.split()
    if len(parts) != 2:
        print("请输入 2 个整数（行 列），或输入 q 退出。例如：2 3")
        return False
    try:
        l = int(parts[0])
        c = int(parts[1])
    except ValueError:
        print("请确保输入的是整数。")
        return False
    if not (0 <= l < max_lines and 0 <= c < max_cols):
        print(f"坐标越界：请保证 0 <= ligne < {max_lines} 且 0 <= colonne < {max_cols}")
        return False
    return (l, c)


def simple_game_loop():
    # 游戏参数：8 行 x 10 列（老师要求示例）
    L, C = 8, 10
    grille = Grille(L, C)
    # 创建船类实例的“样板”（用于长度/marker 信息）
    ship_samples = [PorteAvion(0,0), Croiseur(0,0), Torpilleur(0,0), SousMarin(0,0)]
    # 随机摆放
    try:
        ships = place_ships_randomement(grille, ship_samples)
    except RuntimeError as e:
        print("摆放船失败：", e)
        sys.exit(1)

    coups = 0
    print("=== Bataille Navale 简易版 ===")
    print("地图大小：", L, "x", C)
    print("请输入行 列（以空格分隔），从 0 开始计数。例如：2 3 。输入 q 退出。")
    while True:
        # 显示对玩家的隐藏地图
        print(display_for_player(grille))
        res_in = input_coords("你的射击 (ligne colonne) => ", L, C)
        if res_in is None:
            print("退出游戏。")
            break
        if res_in is False:
            # 输入格式错误，继续循环
            continue
        l, c = res_in
        try:
            result = grille.tirer(l, c, touche="x")
        except ValueError:
            print("坐标无效或越界。")
            continue
        coups += 1
        if result == "miss":
            print("Dans l'eau（未命中）。")
        elif result == "already":
            print("你已经在这里射过了。")
        elif result == "hit":
            # 判断这次命中属于哪艘船（若有）
            ship = find_ship_by_cell(ships, l, c)
            if ship:
                print(f"Touché！命中 {ship.marker}（类型：{ship.__class__.__name__}）")
                if ship.coule(grille):
                    print(f"你已击沉一艘 {ship.__class__.__name__}（marker={ship.marker}）！")
            else:
                # 理论上不可能：hit 一定对应一个船
                print("Touché！")
        # 检查是否游戏结束
        if all_ships_sunk(ships, grille):
            print("恭喜！你击沉了所有舰船！")
            print(f"你总共射击了 {coups} 次。")
            # 显示完整地图（带上船的位置）
            print("\n最终地图（显示所有船和命中位置）：")
            print(str(grille))
            break


if __name__ == "__main__":
    simple_game_loop()
