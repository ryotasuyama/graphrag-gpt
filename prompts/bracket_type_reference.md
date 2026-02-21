## ブラケット型番参照テーブル

helpファイル（`about_ship_settings.html`）から抽出したEvoShip CADのブラケット関連型番一覧。
LLMがブラケットパラメータを決定する際に参照してください。

---

### BracketType（形状種別）

#### 2面ブラケット

| BracketType | 形状名 | BracketParams のパラメータ | 備考 |
|-------------|--------|--------------------------|------|
| **1501** | 2-B | なし（空リスト） | Profile FL × Profile FL の標準形 |
| 1502 | 2-B | `[R]` | |
| 1503 | 2-C | `[D, R]` | |
| 1508 | 2-C2 | `[D, R]` | |
| 1504 | 2-D | `[R]` | |
| **1505** | 2-E | `[R]` → デフォルト `["200"]` | Plate PLS × Profile FL の標準形 |
| 1506 | 2-F | `[D, R]` | |
| 1507 | 2-G | `[D, R]` | |
| 1509 | 2-G2 | `[D, R]` | |

#### 3面ブラケット

| BracketType | 形状名 | BracketParams のパラメータ | 備考 |
|-------------|--------|--------------------------|------|
| 1512 | 3-B | `[R]` | |
| 1513 | 3-C | `[D, R]` | |
| 1514 | 3-D | `[D, R1, R2, a1, a2]` | |
| 1515 | 3-E | `[D]` | |
| 1516 | 3-F | `[D, R1, R2, L1, L2]` | |
| 1517 | 3-G | `[C, R1, R2, B1, B2]` | |
| 1518 | 3-H | `[C1, C2, R1, R2, B1, B2]` | |
| 1519 | 3-I | `[C1, C2, C3, R1, R2, B1, B2]` | |
| 1520 | 3-J | `[C, R1, R2, B1, B2]` | |
| 1521 | 3-K | `[C, R1, R2, B1, B2]` | |

> **通常使用するのは 1505（Plate×Profile）と 1501（Profile×Profile）。**
> 3面ブラケットは Surfaces3 が必要になる（現在の自動生成パイプライン非対応）。

---

### Sf1/Sf2 DimensionType（辺寸法基準型）

Sf1DimensionType / Sf2DimensionType に使用する型番とそのパラメータ：

| Type | 名称 | Sf*DimensonParams のパラメータ | 備考 |
|------|------|-------------------------------|------|
| **1531** | A | `[D, L]` | デフォルト `["200", "15"]` |
| 1546 | AL | `[D, L1, L2]` | |
| 1532 | B | `[D, L]` | |
| 1547 | BL | `[D, L1, L2]` | |
| 1533 | C | `[D, B, L1, L2]` | |
| 1542 | CL | `[D, B, L, L1, L2]` | |
| 1539 | C2 | `[D, B, L1, L2]` | |
| 1543 | C2L | `[D, B, L, L1, L2]` | |
| 1534 | D | `[D, B, R, L1, L2]` | |
| 1544 | DL | `[D, B, R, L, L1, L2]` | |
| 1540 | D2 | `[D, B, R, L1, L2]` | |
| 1545 | D2L | `[D, B, R, L, L1, L2]` | |
| 1535 | E | `[G, L]` | |
| **1541** | E2 | `[G, L]` | デフォルト `["0", "100"]`（Sf1 の BracketType 1505 用） |
| 1536 | F | `[G, L1, L2, a]` | |
| 1537 | G | `[G]` | |
| 1538 | H | `[G, L, a]` | |

**パラメータの意味:**
- `D`: 寸法基準面からのオフセット距離
- `L`, `L1`, `L2`: エッジ方向の長さ
- `B`: 切り欠き幅
- `R`: 切り欠き半径
- `G`: ギャップ（端部からの距離）
- `a`: 角度

---

### Scallop1Type / Scallop2Type（本体スカラップ型）

ブラケット本体エッジのスカラップ設定：

| Type | 名称 | Scallop*Params のパラメータ | 備考 |
|------|------|----------------------------|------|
| **-1** | なし | — | BracketType 1505 の Scallop2 デフォルト |
| **0** | なし | — | BracketType 1501 の Scallop2 デフォルト |
| **1801** | 端部スカラップA1 | `[R]` | Scallop1 のデフォルト。`["0"]` = スカラップなし |
| 1560 | 2辺スカラップ | `[R, RoundFlag]` | RoundFlag: 0=丸、1=切り |
| 1561 | 3辺スカラップ | `[R1, RoundFlag1, R2, RoundFlag2]` | 3面ブラケット用 |

---

### 端部スカラップ型（EndScallop）

ブラケット端部（寸法基準コーナー部）のスカラップ形状：

| Type | 名称 | パラメータ | 備考 |
|------|------|-----------|------|
| 1801 | A1 | `[R]` | |
| 1802 | A2 | `[R]` | |
| 1806 | B1 | `[R, L]` | |
| 1808 | B2 | `[R, L, B]` | |
| 1807 | B3 | `[R, L, B]` | |
| 1809 | B4 | `[R, L, B]` | |
| 1810 | B5 | `[R, L]` | |
| 1811 | B6 | `[R, L]` | |
| 1803 | C1 | `[R]` | |
| 1804 | C2 | `[W, H]` | |
| 1805 | C3 | `[W, H, R]` | |

---

### FlangeType（フランジ型）

| Type | 名称 | パラメータ | 備考 |
|------|------|-----------|------|
| **null** | なし | — | デフォルト（ほとんどのケース） |
| 261 | C | `[B, G1, G2]` | |
| 262 | S | `[B, D, a, G1, G2]` | |
| 263 | CS | `[B, D, a, G1, G2, SwapFlag]` | SwapFlag: 0=そのまま、1=スワップ |

- フランジはすべてのブラケット形状に取り付けられるわけではない
- `RevSf3=True` でアングル方向を反転

---

### デフォルト値まとめ

通常スクリプト生成で使用する値（参考スクリプトがない場合のフォールバック）：

#### BracketType 1505（Plate × Profile FL）
```python
BracketParams     = ["200"]
Sf1DimensionType  = 1541   # E2: params = [G, L]
Sf1DimensonParams = ["0", "100"]
Sf2DimensionType  = 1531   # A: params = [D, L]
Sf2DimensonParams = ["200", "15"]
Scallop1Type      = 1801
Scallop1Params    = ["0"]
Scallop2Type      = -1
```

#### BracketType 1501（Profile FL × Profile FL）
```python
# BracketParamsは設定しない
Sf1DimensionType  = 1531   # A: params = [D, L]
Sf1DimensonParams = ["200", "15"]
Sf2DimensionType  = 1531   # A: params = [D, L]
Sf2DimensonParams = ["200", "15"]
Scallop1Type      = 1801
Scallop1Params    = ["0"]
Scallop2Type      = 0
```
