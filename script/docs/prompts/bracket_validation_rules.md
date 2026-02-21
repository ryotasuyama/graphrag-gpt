## COM例外のデバッグガイド

`pywintypes.com_error` が `CreateBracket` で発生した場合、以下の原因を順にチェックしてください。

### 原因1: Surfaces の参照先が存在しないか型が不正
- Surfaces1/Surfaces2 で参照している変数（solidN, extrude_sheetN, profileN[0]）がスクリプト内で生成済みか確認
- PLS形式の場合、**必ず7要素**: `["PLS","False","False", nx, ny, nz, sheetOrSolidVar]`
- 法線ベクトル (nx,ny,nz) が全て0でないか確認
- FL形式の場合: `[profileN[0]+",FL"]`

### 原因2: BaseElement が不正
- BaseElement には必ず `profileN[0]` を使う
- `solidN`, `extrude_sheetN` は不可
- `profileN[0]` がスクリプト内で `CreateProfile()` により生成されているか確認

### 原因3: Sf1EndElements の参照先が不正
- PLS形式で参照する要素が、実際に存在するシート/プロファイルか確認
- 法線ベクトルが **AttachSurface ではなく EndElement のシート法線** を使っているか確認

### 原因4: BracketType と Surfaces の組み合わせが不整合
- **1505**: Surfaces1 は必ず PLS形式、Surfaces2 は FL形式
- **1501**: Surfaces1, Surfaces2 ともに FL形式
- BracketType に存在しないフィールドを設定していないか確認

### 原因5: 寸法パラメータの不備
- Sf1DimensonParams/Sf2DimensonParams が必ず2要素のリスト
- Thickness が正の数値文字列であること

### 対処: 最初の1つだけ生成して検証する
COM例外が修正できない場合は、**ブラケットを1つだけ生成**してください。
最も単純なケース（ProfileType=1003 の End1側、BracketType=1505）を1つだけ出力し、
それが成功すれば残りを追加する段階的アプローチを取ります。
