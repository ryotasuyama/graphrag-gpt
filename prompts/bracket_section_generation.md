## タスク
以下の【ブラケット配置分析】に基づいて、ブラケットセクションのPythonコードのみを生成してください。

**重要な制約:**
- `bracketPram1 = part.CreateBracketParam()` から始めること
- ブラケットの色設定 `part.SetElementColor(bracketN, ...)` で終わること
- import文、solid作成、profile作成など、ブラケット以外のコードは一切含めないこと
- スクリプト全体を出力しないこと
- **全候補生成**: 【ブラケット配置分析】の配置リストに記載された**すべてのブラケット**を生成すること。1つだけの例示や省略は禁止。bracketPram1, bracketPram2, ..., bracketPramN のように全件を出力すること

{reference_bracket_examples}

{error_context_section}

【ブラケット配置分析】

{analysis_document}

-----

## 出力フォーマット

```python
# ブラケットセクション（bracketPram1 から始まり、最後のSetElementColorで終わる）
bracketPram1 = part.CreateBracketParam()
# ... (ブラケット配置コードのみ)
part.SetElementColor(bracket_last, ...)
```
