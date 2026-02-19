## タスク
以下の【ブラケット候補グループ】について、各ブラケットのパラメータを**JSON形式のみ**で出力してください。
**Pythonコードは一切出力しないこと。** JSONのみ出力してください。

{error_context_section}

{reference_bracket_examples}

---

### 事前計算済みデータ（変更不要）

以下の値は静的解析により確定しています。コード変数名として使用するため、引用符なしで参照してください。

{prefilled_table}

---

### LLMが決定すべきパラメータ

各候補について以下のパラメータのみ決定してください:

- `bracket_name`: 命名規則に従ったブラケット名（例: `"HK.Casing.Wall.Side.FR12.Deck.DP"`）
- `thickness`: プロファイルのProfileParamsの板厚値（文字列、例: `"9.9999999999999982"`）
- `bracket_type`: 1505（PLS×FL）または 1501（FL×FL）を確認・必要に応じて変更
- `bracket_params`: BracketType 1505の場合 `["200"]`（BracketType 1501には含めない）
- `sf1_dimension_type`: Sf1 寸法タイプ（例: 1541）
- `sf1_dimension_params`: Sf1 寸法パラメータ（例: `["0", "100"]`）
- `sf2_dimension_type`: Sf2 寸法タイプ（例: 1531）
- `sf2_dimension_params`: Sf2 寸法パラメータ（例: `["200", "15"]`）
- `flange_type`: DL02プロファイルの場合のみ設定（通常 `null`）
- `rev_sf1` / `rev_sf2` / `rev_sf3`: 通常 `false`
- `surfaces2_ref`: BracketType 1501の場合のみ必要（第2プロファイルの変数名、例: `"profile5[0]"`）

---

【ブラケット候補グループ: {group_name}】

{group_candidates_detail}

---

## 出力フォーマット

全候補分（{num_candidates}件）を省略せず出力してください。

```json
{{
  "brackets": [
    {{
      "candidate_id": 1,
      "bracket_name": "...",
      "thickness": "9.9999999999999982",
      "bracket_type": 1505,
      "bracket_params": ["200"],
      "sf1_dimension_type": 1541,
      "sf1_dimension_params": ["0", "100"],
      "sf2_dimension_type": 1531,
      "sf2_dimension_params": ["200", "15"],
      "flange_type": null,
      "rev_sf1": false,
      "rev_sf2": false,
      "rev_sf3": false
    }}
  ]
}}
```
