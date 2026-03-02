## ブラケット配置分析ガイド（参考スクリプトなし）

参考スクリプトが提供されていないため、元のスクリプトの構造のみからブラケット配置を決定します。
以下の自動解析結果と判断基準を活用してください。

### 1. ブラケット配置箇所の特定

- 各 Profile の End1/End2 接続先がブラケット候補です
- Profile が板（extrude_sheet）に `AddAttachSurfaces` で取り付き、End1/End2 で別の板に接続している場合、その交差コーナーにブラケットが必要
- 下記の「自動検出されたブラケット候補」テーブルを基にしてください
- **配置漏れ防止**: ProfileType 1002/1003（山形鋼）、1201（T形鋼）のすべてのEnd接続にブラケットが必要

### 2. BracketType の決定

| 接続パターン | BracketType | Surfaces1 | Surfaces2 |
|-------------|-------------|-----------|-----------|
| (A) Plate(PLS面) × Profile(FL面) | **1505** | `["PLS","False","False",nx,ny,nz,solidX]` | `[profileN[0]+",FL"]` |
| (B) Profile(FL面) × Profile(FL面) | **1501** | `[profileA[0]+",FL"]` | `[profileB[0]+",FL"]` |
| (C) Profile板要素(PLS面) × Plate(PLS面) | **1505** | `["PLS","False","False",nx,ny,nz,profileXX[1]]` | `["PLS","False","False",nx2,ny2,nz2,solidY]` |

- ProfileType 1002/1003 → 通常 **1505**（板に取り付くスティフナの端部）
- 2つのプロファイルが交差する箇所 → **1501**
- タイプ(C): AttachSurface が存在せず profileXX[1] が板要素として使われる場合（Sf1EndElements は **不要**）

> 型番・パラメータの完全一覧は `bracket_type_reference.md` を参照してください。

### 3. Surfaces の構成方法

#### Surfaces1（PLS面の場合 — BracketType 1505）
```
["PLS", "False", "False", nx, ny, nz, solidX_or_sheetX]
```
- `nx, ny, nz` は **AttachSurface の SheetAlignNormal の符号反転値**
  - 自動解析結果の「PLS法線」列の値をそのまま使用してください
- 最後の要素（面参照変数）:
  - AttachSurface のシートが `CreateThicken` でソリッド化されている場合 → **対応する `solidN` を使用（推奨）**
  - ソリッド化されていない場合 → `extrude_sheetN` を使用
  - 自動解析結果の「Solid代替」列に対応するsolid変数が表示されている場合はそちらを優先

#### Surfaces2（FL面の場合）
```
[profileN[0] + ",FL"]
```

#### BaseElement
- **必ず `profileN[0]`**（Profile本体）を使用。solid や extrude_sheet は不可

### 4. 寸法パラメータのデフォルト値

#### BracketType 1505 の場合
| パラメータ | 値 |
|-----------|-----|
| BracketParams | `["200"]` |
| Sf1DimensionType | 1541 |
| Sf1DimensonParams | `["0","100"]` |
| Sf2DimensionType | 1531 |
| Sf2DimensonParams | `["200","15"]` |
| Scallop1Type | 1801 |
| Scallop1Params | `["0"]` |
| Scallop2Type | -1 |

#### BracketType 1501 の場合
| パラメータ | 値 |
|-----------|-----|
| Sf1DimensionType | 1531 |
| Sf1DimensonParams | `["200","15"]` |
| Sf2DimensionType | 1531 |
| Sf2DimensonParams | `["200","15"]` |
| Scallop1Type | 1801 |
| Scallop1Params | `["0"]` |
| Scallop2Type | 0 |

### 5. Sf1EndElements（BracketType 1505 の場合に**必須**）

**省略するとCOM例外が発生します。必ず設定してください。**

```
["PLS", "False", "False", nx, ny, nz, endElementVar]
```
- `endElementVar` は **Surfaces1（PLS板）の面上に存在するスティフナまたはデッキ材プロファイル**
  - 例: Side FR を Deck.D（solid2）に接続する場合 → Deck.D 上の DLxx/FRxx プロファイル（`profile17[0]` 等）
  - **FR profile 自身の End1/End2 に指定した板要素（`extrude_sheetN` 等）ではない**
  - 参考スクリプトが利用可能な場合は、同型ブラケット（1505）の `Sf1EndElements` をそのまま流用すること
- `nx, ny, nz` は **自動解析結果の「EndElement法線」列の値をそのまま使用**してください
  - この値は EndElement のシート法線（SheetAlignNormal）の符号反転値として事前計算されています

### 6. その他の共通パラメータ
- `DefinitionType=1`（固定）
- `UseSideSheetForPlane=False`（固定）
- `RevSf1=False`, `RevSf2=False`, `RevSf3=False`（デフォルト）
- `Thickness`: ProfileParams の板厚値を参考に `"8"` ～ `"12"` 程度
- `Mold`: Profile と同じ値を使用
- `MaterialName`: `"SS400"`（元スクリプトと同じ）

### 7. 注意事項
- ミラーコピーされた部材はオリジナル側のみブラケットを作成（後でミラー可能）
- `part.CreateBracket(bracketParam, False)` — 第2引数は必ず False
- `part.BlankElement(bracketX, True)` は使わない
- ブラケットコードは全 solid/profile 生成の後に配置する
