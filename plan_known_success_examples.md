# 実装計画: アイデア2「既知成功例の徹底収集」

## 背景と課題

`analysis_llm_script_iteration.md` の分析により、ブラケット生成精度が低い根本原因は「フィードバックの質」ではなく **「提供される例の質」** にあると判明。

現状の問題：
- `prompts/examples/bracket_1501.txt` / `bracket_1505.txt` は `DefinitionType`, `BracketName`, `MaterialName`, `Mold`, `Thickness` などの必須フィールドが欠落した**最小例**
- 参照スクリプトが明示されない場合（`-r` フラグなし）、LLMはこの最小例しか参照できない
- 結果として LLM は「実例の模倣」ではなく「理解してから生成」せざるを得ず、Non-Recoverable な値（法線ベクトル等）を創作してしまう

**追加で判明した問題（0301-1 vs 0301-2 の比較分析より）：**
- Agent 1（analysis.md 生成）の出力テーブルに `Sf1EndElements` 列がなく、Agent 2 が推測する構造になっている
- `bracket_analysis_guide_noref.md` の EndElement 説明が「FR profile自身のEnd1/End2要素」と誤読できる記述になっており、LLMが誤った参照先（`profile1[0]`等）を選び続ける原因になっている
- エラー修正プロンプトのCOM例外チェックリストが汎用的すぎ、Sf1EndElements の正しい修正方向を示せていない

**目的：完全な実績例を自動的に LLM に提供し、「実例の模倣」で生成させる**

---

## 素材の確認

以下のスクリプトから完全な実績例を抽出する。

| ソース | 行 | 内容 | 状態 |
|--------|-----|------|------|
| `script/samplename.py` | L339–362 | BracketType 1501（Profile FL × Profile FL）| `BlankElement(True)` あり → その行のみ除外 |
| `script/sample.py` | L395–418 | BracketType 1505（Plate PLS × Profile FL）1件目 | クリーン |
| `script/sample.py` | L474–497 | BracketType 1505（Plate PLS × Profile FL）2件目 | クリーン・命名パターンの確認用 |

---

## 変更ファイル一覧

| ファイル | 操作 | 優先度 |
|---------|------|--------|
| `prompts/bracket_placement_analysis.md` | 分析テーブルに `Sf1EndElements` 列を追加（ステップ A） | **最優先** |
| `prompts/bracket_analysis_guide_noref.md` | Section 5 の EndElement 説明を修正（ステップ B） | **最優先** |
| `prompts/examples/bracket_1501.txt` | 完全フィールドセットに**置き換え** | 最優先 |
| `prompts/examples/bracket_1505.txt` | 完全フィールドセットに**置き換え** | 最優先 |
| `prompts/examples/bracket_1505_with_sf1end.txt` | **新規作成**（2件目の 1505 例） | 最優先 |
| `prompts/loader.py` | COM例外チェックリストに Sf1EndElements 診断を追加（ステップ C）＋例選択ロジック改善 | 高 |
| `query.py` | デフォルト参照スクリプトの自動ロードを追加 | 高 |

---

## ステップ A: `bracket_placement_analysis.md` の分析テーブルに `Sf1EndElements` 列を追加

**問題**: Agent 1 の出力フォーマット指示（`bracket_placement_analysis.md`）のテーブルに `Sf1EndElements` 列がない。
そのため Agent 1 は Sf1EndElements をテーブルで明示する必要がなく、Agent 2 は備考の読み取りまたは推測に頼ってしまう。

**変更箇所**: `bracket_placement_analysis.md` の `## 出力フォーマット` 内テーブル定義

```markdown
# 変更前
| # | Surfaces1 | Surfaces2 | BracketType | BaseElement | 備考 |
|---|-----------|-----------|-------------|-------------|------|
| 1 | （例: solid1,PL） | （例: profile1[0],FL） | （例: 1505） | （例: profile1[0]） | （注意事項など） |

# 変更後
| # | Surfaces1 | Surfaces2 | BracketType | BaseElement | Sf1EndElements | 備考 |
|---|-----------|-----------|-------------|-------------|----------------|------|
| 1 | （例: ["PLS","False","False","0","-0","-1",solid1]） | （例: profile1[0]+",FL"） | （例: 1505） | （例: profile1[0]） | （例: profile8[0]） | （注意事項など） |
```

**効果**: Agent 1 がどのプロファイルを Sf1EndElements に使うかをテーブルで確定させるため、Agent 2 は推測なしに正しい値を使える。参照スクリプトありの場合（`bracket_analysis_guide.md` 使用時）にも同じテーブル形式が使われるため、両方のケースで一貫して機能する。

---

## ステップ B: `bracket_analysis_guide_noref.md` Section 5 の EndElement 説明を修正

**問題**: 現在の記述（Section 5, L80-81）：
```
- `endElementVar` は End1/End2 で指定されている要素（`extrude_sheetN` や `profileN[0]`）
```
これは「FR profile 自身の End1/End2 要素（＝接続先の板）」を使うように読める。
しかし正解は「Surfaces1 の板面（PLS）の**上に存在するスティフナ/デッキ材**」を使うことであり（例: Deck.D に接続するFRに対し、Deck.D 上の DLxx プロファイルを指定）、End1/End2 要素とは別物である。

**変更箇所**: `bracket_analysis_guide_noref.md` Section 5「Sf1EndElements」の説明文

```markdown
# 変更前
- `endElementVar` は End1/End2 で指定されている要素（`extrude_sheetN` や `profileN[0]`）
- `nx, ny, nz` は **自動解析結果の「EndElement法線」列の値をそのまま使用**してください
  - この値は EndElement のシート法線（SheetAlignNormal）の符号反転値として事前計算されています
- EndElementがシートの場合でも `CreateThicken` でソリッド化されていれば `solidN` を推奨

# 変更後
- `endElementVar` は **Surfaces1（PLS板）の面上に存在するスティフナまたはデッキ材プロファイル**
  - 例: Side FR を Deck.D（solid2）に接続する場合 → Deck.D 上の DLxx/FRxx プロファイル（`profile17[0]` 等）
  - **FR profile 自身の End1/End2 要素（`extrude_sheetN` 等）ではない**
  - 参考スクリプトが利用可能な場合は、同型ブラケット（1505）の `Sf1EndElements` をそのまま流用すること
- `nx, ny, nz` は **自動解析結果の「EndElement法線」列の値をそのまま使用**してください
  - この値は EndElement のシート法線（SheetAlignNormal）の符号反転値として事前計算されています
```

**効果**: `-r` なし実行時でも、LLM が「板のEnd要素」ではなく「板面上の隣接スティフナ」という正しい参照先を選べるようになる。0301-2 で繰り返された `profile1[0]`（Wall系部材）の誤指定を防ぐ。

---

## ステップ C: `loader.py` の COM 例外チェックリストに Sf1EndElements 診断を追加

**問題**: `_build_error_context_block()` のチェックリスト項目3は汎用的すぎ、1505 で Sf1EndElements の参照先が誤っているという最頻発ケースへの具体的な修正方向を示せていない。

**変更箇所**: `prompts/loader.py` の `_build_error_context_block()` 内 COM 例外時の追加ブロック（現在の `"- **Sf1EndElements の法線方向を反転**..."` の前に追加）

```python
# 変更後（COM例外時の「代替アプローチの提案」に追加）
"- **Sf1EndElements の参照先を確認**: `endElementVar` に指定したプロファイルが "
"Surfaces1 の板（solidX）の面上に存在するプロファイルかを確認してください。\n"
"  - Side FR → Deck 接続（1505）の場合: Deck 板上の DLxx/FRxx プロファイル（`profileN[0]`）を使います。\n"
"  - FR プロファイル自身の End1/End2 に指定した板要素（`extrude_sheetN`）ではありません。\n"
"  - 参考スクリプトに同型ブラケットがある場合は、その `Sf1EndElements` の値をそのまま使用してください。\n"
```

**効果**: エラー修正ループで「同じ誤った参照を繰り返す」ランダムウォークを止め、正しい修正方向（板面上の隣接スティフナへの切り替え）を LLM に示す。

---

## ステップ 1: `bracket_1501.txt` を完全例に置き換え

**欠落している現状フィールド**: `DefinitionType`, `BracketName`, `MaterialName`, `BaseElement`, `UseSideSheetForPlane`, `Mold`, `Thickness`

`script/samplename.py` L339–362 を素材に（`BlankElement(bracket1,True)` の行のみ除外）：

```python
# BracketType 1501: Profile(FL面) × Profile(FL面)
# BaseElement は Profile 本体 (profileXX[0])
# Surfaces1/Surfaces2 はどちらも Profile の FL 面
# 命名規則: "HK.<構造>.<部材名>.<位置>"
bracketPram1 = part.CreateBracketParam()
bracketPram1.DefinitionType=1
bracketPram1.BracketName="HK.Casing.Wall.Fore.DL01.Deck.DP"
bracketPram1.MaterialName="SS400"
bracketPram1.BaseElement=profile7[0]
bracketPram1.UseSideSheetForPlane=False
bracketPram1.Mold="+"
bracketPram1.Thickness="7.9999999999999964"
bracketPram1.BracketType=1501
bracketPram1.Scallop1Type=1801
bracketPram1.Scallop1Params=["0"]
bracketPram1.Scallop2Type=0
bracketPram1.Surfaces1=[profile7[0]+",FL"]
bracketPram1.RevSf1=False
bracketPram1.Surfaces2=[profile6[0]+",FL"]
bracketPram1.RevSf2=False
bracketPram1.RevSf3=False
bracketPram1.Sf1DimensionType=1531
bracketPram1.Sf1DimensonParams=["200","15"]
bracketPram1.Sf2DimensionType=1531
bracketPram1.Sf2DimensonParams=["200","15"]
bracket1 = part.CreateBracket(bracketPram1,False)
part.SetElementColor(bracket1,"0","255","255","0.19999998807907104")
```

---

## ステップ 2: `bracket_1505.txt` を完全例に置き換え

`script/sample.py` L395–418（bracketPram1、BracketType 1505）を素材に：

```python
# BracketType 1505: Plate(PLS面) × Profile(FL面)
# BaseElement は Profile 本体 (profileXX[0])
# Surfaces1: ["PLS","False","False", nx, ny, nz, solidX]   ← PLS 法線は solid の法線方向
# Sf1EndElements: ["PLS","False","False", nx, ny, nz, profileXX[0]]  ← 端部接続要素
bracketPram1 = part.CreateBracketParam()
bracketPram1.DefinitionType=1
bracketPram1.BracketName="HK.Casing.Wall.Side.FR08.Deck.CP"
bracketPram1.MaterialName="SS400"
bracketPram1.BaseElement=profile5[0]
bracketPram1.UseSideSheetForPlane=False
bracketPram1.Mold="+"
bracketPram1.Thickness="9.9999999999999982"
bracketPram1.BracketType=1505
bracketPram1.BracketParams=["200"]
bracketPram1.Scallop1Type=1801
bracketPram1.Scallop1Params=["0"]
bracketPram1.Scallop2Type=0
bracketPram1.Surfaces1=["PLS","False","False","0","-0","-1",solid1]
bracketPram1.RevSf1=False
bracketPram1.Surfaces2=[profile5[0]+",FL"]
bracketPram1.RevSf2=False
bracketPram1.RevSf3=False
bracketPram1.Sf1DimensionType=1541
bracketPram1.Sf1DimensonParams=["0","100"]
bracketPram1.Sf1EndElements=["PLS","False","False","-0","-1","-0",profile8[0]]
bracketPram1.Sf2DimensionType=1531
bracketPram1.Sf2DimensonParams=["200","15"]
bracket1 = part.CreateBracket(bracketPram1,False)
part.SetElementColor(bracket1,"0","255","255","0.19999998807907104")
```

---

## ステップ 3: `bracket_1505_with_sf1end.txt` を新規作成

`script/sample.py` L474–498（bracketPram2）を素材に。

**目的**: 複数ブラケットを生成する際の **変数命名パターン**（`bracketPram2`, `bracket2`）と、同一 `solid` への2件目 1505 ブラケットの書き方を示す。

```python
# BracketType 1505 (2件目の例): Plate(PLS面) × Profile(FL面)
# 変数番号は連番にする (bracketPram2, bracket2, ...)
bracketPram2 = part.CreateBracketParam()
bracketPram2.DefinitionType=1
bracketPram2.BracketName="HK.Casing.Wall.Side.FR11.Deck.CP"
bracketPram2.MaterialName="SS400"
bracketPram2.BaseElement=profile10[0]
bracketPram2.UseSideSheetForPlane=False
bracketPram2.Mold="+"
bracketPram2.Thickness="9.9999999999999982"
bracketPram2.BracketType=1505
bracketPram2.BracketParams=["200"]
bracketPram2.Scallop1Type=1801
bracketPram2.Scallop1Params=["0"]
bracketPram2.Scallop2Type=0
bracketPram2.Surfaces1=["PLS","False","False","0","-0","-1",solid1]
bracketPram2.RevSf1=False
bracketPram2.Surfaces2=[profile10[0]+",FL"]
bracketPram2.RevSf2=False
bracketPram2.RevSf3=False
bracketPram2.Sf1DimensionType=1541
bracketPram2.Sf1DimensonParams=["0","100"]
bracketPram2.Sf1EndElements=["PLS","False","False","-0","-1","-0",profile8[0]]
bracketPram2.Sf2DimensionType=1531
bracketPram2.Sf2DimensonParams=["200","15"]
bracket2 = part.CreateBracket(bracketPram2,False)
part.SetElementColor(bracket2,"0","255","255","0.19999998807907104")
```

---

## ステップ 4: `loader.py` の例選択ロジックを改善

### 追加関数: `select_bracket_examples(candidates) -> list[str]`

ブラケット候補の `bracket_type` に基づいて、使用するコード例ファイル名リストを返す。

```python
def select_bracket_examples(candidates: list = None) -> list[str]:
    """
    ブラケット候補リストに基づいて使用するコード例ファイル名を返す。
    candidates が None または空の場合はデフォルト（両方）を返す。
    """
    if not candidates:
        return ["bracket_1505", "bracket_1505_with_sf1end", "bracket_1501"]

    types = {c.get("bracket_type", 1505) for c in candidates}
    result = []
    if 1505 in types:
        result.extend(["bracket_1505", "bracket_1505_with_sf1end"])
    if 1501 in types:
        result.append("bracket_1501")
    return result or ["bracket_1505", "bracket_1505_with_sf1end", "bracket_1501"]
```

### `build_bracket_section_prompt()` と各変種の修正

関数シグネチャに `candidates: list = None` を追加し、ハードコードされた 2例 の選択を `select_bracket_examples(candidates)` に置き換える。

**変更対象関数（4箇所）**:
- `build_bracket_section_prompt()`
- `build_bracket_section_prompt_with_error()`
- `build_bracket_group_json_prompt()`（`group["candidates"]` を渡す）
- `build_bracket_group_json_prompt_with_error()`（同上）

**変更前**:
```python
parts.append("## 参考コード例（BracketType 1505: PLS × Profile FL）")
parts.append("```python\n" + load_example("bracket_1505") + "\n```")
parts.append("## 参考コード例（BracketType 1501: Profile FL × Profile FL）")
parts.append("```python\n" + load_example("bracket_1501") + "\n```")
```

**変更後**:
```python
for example_name in select_bracket_examples(candidates):
    example_code = load_example(example_name)
    # ヘッダはファイル先頭の # コメントから自動取得
    header_line = next((l.lstrip("# ").strip() for l in example_code.splitlines() if l.startswith("#")), example_name)
    parts.append(f"## 参考コード例（{header_line}）")
    parts.append("```python\n" + example_code + "\n```")
```

### `query.py` 呼び出し箇所の更新

`build_bracket_section_prompt()` を呼ぶ箇所（`query.py` 内）で、`candidates` を渡すよう更新する。

---

## ステップ 5: `query.py` でデフォルト参照スクリプトを自動ロード

参照スクリプト未指定（`-r` なし）かつブラケットタスクの場合に `script/samplename.py` を自動ロードする。

**変更箇所**: `load_script_files()` 関数の末尾に追加

```python
# ブラケットタスクで参照スクリプトが未指定の場合、デフォルト参照を試みる
if reference_code is None:
    from prompts.loader import is_bracket_task
    if is_bracket_task(file_path, original_code):          # instructionが渡せない場合はoriginal_codeで代替
        default_ref = os.path.join(os.path.dirname(os.path.abspath(__file__)), "script", "samplename.py")
        if os.path.exists(default_ref) and os.path.abspath(default_ref) != os.path.abspath(file_path):
            with open(default_ref, "r", encoding="utf-8") as f:
                reference_code = f.read()
            print(f"--- [Default Reference] Auto-loaded: {default_ref} ---")
```

**注意**: `is_bracket_task()` に `instruction` を渡せるように呼び出し元から変数を取得するか、`original_code` 内の `CreateBracket` 有無で判定する（`reference_code` がある既存スクリプトに `CreateBracket` が含まれるケースに対応）。

---

## 優先順位サマリ

| ステップ | 対象ファイル | インパクト | 実装コスト | 優先度 |
|---------|------------|----------|-----------|--------|
| **A**: 分析テーブルに Sf1EndElements 列追加 | `bracket_placement_analysis.md` | **高**（Agent 1 の出力品質が直接改善） | **最低**（テキスト編集のみ） | **最優先** |
| **B**: EndElement 説明の修正 | `bracket_analysis_guide_noref.md` | **高**（-r なし時の根本的誤りを解消） | **最低**（テキスト編集のみ） | **最優先** |
| 1–3: 例ファイルの拡充 | `prompts/examples/*.txt` | **高**（Agent 2 の模倣精度が改善） | **低**（テキスト編集のみ） | **最優先** |
| 5: デフォルト参照スクリプト | `query.py` | **高**（`-r` 未指定時の品質向上） | 低〜中（条件分岐追加のみ） | 高 |
| **C**: COM例外チェックリストに診断追加 | `prompts/loader.py` | 中（エラー修正ループの方向性改善） | **低**（文言追加のみ） | 高 |
| 4: 例選択ロジック | `prompts/loader.py` | 中（候補型に応じた最適化） | 中（関数追加 + 4箇所修正） | 中 |

---

## 検証手順

```bash
# 0. ステップ A: 分析テーブルに Sf1EndElements 列が追加されているか確認
grep "Sf1EndElements" prompts/bracket_placement_analysis.md
# 期待値: 列ヘッダと例行に "Sf1EndElements" が含まれる

# 0b. ステップ B: bracket_analysis_guide_noref.md の修正確認
grep -A3 "endElementVar" prompts/bracket_analysis_guide_noref.md
# 期待値: "Surfaces1（PLS板）の面上に存在する" という説明が含まれる

# 0c. ステップ C: loader.py に Sf1EndElements 診断が追加されているか確認
grep "Sf1EndElements の参照先" prompts/loader.py
# 期待値: 1件以上ヒット

# 1. 例ファイルに BlankElement(True) が含まれていないことを確認
grep -n "BlankElement.*True" prompts/examples/bracket_1501.txt prompts/examples/bracket_1505.txt

# 2. 例ファイルに必須フィールドが含まれていることを確認
grep -c "BracketName\|MaterialName\|DefinitionType" \
  prompts/examples/bracket_1501.txt \
  prompts/examples/bracket_1505.txt

# 3. 参照スクリプトなしでブラケット生成（デフォルト参照の動作確認）
python query.py script/samplename_no_bracket.py "ブラケットをつけてください。" \
  -o script/test_out.py --no-exec

# 4. 生成スクリプトに完全フィールドが含まれているか確認
grep -c "BracketName\|MaterialName\|DefinitionType" script/test_out.py
# 期待値: ブラケット数 × 3 以上

# 5. 明示的参照スクリプトありでも動作確認（既存動作の回帰テスト）
python query.py script/sample_no_bracket.py "ブラケットをつけてください。" \
  -r script/samplename.py -o script/test_out2.py --no-exec
```

**合格基準**:
- `bracket_1501.txt` / `bracket_1505.txt` に `BlankElement.*True` が 0 件
- `test_out.py` で `BracketName=`, `MaterialName=`, `DefinitionType=1` が生成されている
- 明示的 `-r` 指定時も動作が変わらない（回帰なし）
