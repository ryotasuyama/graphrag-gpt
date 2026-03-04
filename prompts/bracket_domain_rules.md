## ブラケット生成の絶対ルール（必ず守る）

1. **`part.CreateBracket(bracketParam, False)`** — 第2引数は **必ず False**（True は非表示になるため禁止）
2. **`part.BlankElement(bracketX, True)` を入れない** — ブラケットが見えなくなる。`False` のみ許可
3. **BaseElement は `profileXX[0]`（Profile本体）** — solid を渡してはいけない
4. **ブラケットコードは、参照する solid・profile が定義済みであれば任意の位置に配置できる**（末尾集約は不要）
5. **参考スクリプトの BracketType / フィールドをそのまま踏襲し、未知のフィールドを創作しない**

## 接続ペアの種類

ブラケットは「2つの面（Surfaces1 / Surfaces2）」を結ぶ要素として定義する。
代表的なペアは下記の通り（具体的な書式は後述のコード例を参照）:

- **(A) Plate × Profile**: Surfaces1=PLS面（solidX参照）、Surfaces2=Profile FL面 → BracketType 1505
- **(B) Profile × Profile**: Surfaces1=Profile FL面、Surfaces2=Profile FL面 → BracketType 1501
- **(C) Profile板要素 × Plate**: Surfaces1=PLS面（profileXX[1]参照）、Surfaces2=PLS面（solidX参照）→ BracketType 1505 ※Sf1EndElements 不要

## BracketType 選択ルール

BracketType の選択基準は `bracket_analysis_guide_noref.md` を参照すること。

## ブラケット候補の探索基準

BaseElement となる Profile は以下の特徴を持つものを優先:
- `AddAttachSurfaces(...)` で板に取り付いている（板付きスティフナ）
- `AddEnd1Elements(...)` / `AddEnd2Elements(...)` が存在する
- ProfileType がスティフナ系（1002 / 1003）

## 配置位置

- 各スティフナの End1 / End2 付近にブラケットを配置
- `Sf1EndElements` / `Sf2EndElements` が参考スクリプトにある場合は必ず模倣
- 座標系・方向ベクトル・オフセットの定義は元スクリプトから変えない