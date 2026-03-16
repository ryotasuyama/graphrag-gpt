あなたは、CADアプリケーション「EvoShip」のブラケット生成コードを修正するエキスパートです。
以下のPythonスクリプトを実行したところ、CreateBracket呼び出しでCOM例外が発生しました。
エラー情報を分析し、失敗候補とその近縁候補を中心にブラケットパラメータを修正した完全なPythonスクリプトを生成してください。

## 重要：修正ポリシー（必ず守る）
- **変更対象は、失敗した CreateBracket 候補と、その近縁の危険候補です。**
- 成功済みのブラケット候補と、それ以外のコード（生成された形状、部材生成順序）は **原則そのまま**にしてください。
- `NameError: bracketX is not defined` の場合は、未定義変数の使用行ではなく、対応する `bracketX = part.CreateBracket(...)` 候補を修正してください。
- 同一署名または近縁署名の候補を、別名や別候補番号で再生成しないでください。
- 出力は **完成した全スクリプト**（省略なし、` ```python ... ``` ` で囲む）のみです。

## エラー情報（Traceback）
{error_traceback}

## 失敗行とその周辺コンテキスト
失敗行（行{error_line_number}）:
```python
{error_line}
```

前後のコンテキスト（前{context_lines}行）:
```python
{context_before}
{error_line}
{context_after}
```

## 対象ブラケットパラメータの定義
{bracket_param_section}

## 構造化された失敗候補
- failed_signature: {failed_signature}
- normalization_note: {normalization_note}

## ブラケット修正のチェックリスト（以下を順に確認して修正）
以下の観点を順に確認し、問題があれば修正してください：

0. **表示状態（Blank）の確認（例外がなくても重要）**
- `part.CreateBracket(bracketParam, True)` になっている場合は **必ず False に修正**する。
- ブラケット作成直後（または近傍）に `part.BlankElement(bracketX, True)` がある場合は **削除**する（または `False` に変更）。
- 参考スクリプトの規約：ブラケットは作成時に表示が基本（CreateBracket第2引数 False）。

1. **Surfaces1 / Surfaces2 の妥当性**
- 参照している面が None/未生成/型不一致になっていないか
- 面ペア順序（PLS↔FL 等）が参考スクリプトと整合するか
- 面の参照形式が正しいか（例: `profileXX[0]+",FL"` または `["PLS", ..., solidX]`）

2. **BaseElement の妥当性**
- 原則 `profileXX[0]`（Profile本体）を使う、solid を渡していないか
- BaseElement が正しく定義されているか

3. **End1/End2 と EndElements**
- `AddEnd1Elements/AddEnd2Elements` に対応する要素が欠けていないか
- Sf1EndElements / Sf2EndElements が必要な型で設定されているか

4. **BracketType とフィールドの整合**
- 参考スクリプトに存在する `BracketType` / `Sf1EndElements` / `Sf2EndElements` を勝手に増減しない
- 型により必須フィールドが違う可能性があるため、参考スクリプトで同型を優先
- Side 系の未実績 `1501 / FL-FL` を避ける。必要なら `1505 / PLS-FL + Sf1EndElements` に置換する

5. **寸法の符号・範囲**
- Height/Width/Thickness が 0 以下になっていないか
- 板厚に対して極端に大きすぎ/小さすぎの値になっていないか（可能なら参照部材寸法から再計算）

6. **向き（Orientation/Vector）が必要な型の場合**
- 参照面の法線に対して不正な向きになっていないか
- 参考スクリプトに合わせた規約（例えば FL を基準にする等）を踏襲

## 参考スクリプト（該当する CreateBracket 例）
{reference_snippet}

## 元のスクリプト全体
```python
{full_code}
```

## 出力形式
修正後の完全なPythonスクリプトのみを以下の形式で出力してください。説明やコメントは不要です。

```python
# 修正後の完全なスクリプト（省略なし）
```
