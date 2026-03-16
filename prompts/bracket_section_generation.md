## タスク
以下の【ブラケット配置分析】に基づいて、ブラケットセクションのPythonコードのみを生成してください。

**重要な制約:**
- `bracketPram1 = part.CreateBracketParam()` から始めること
- ブラケットの色設定 `part.SetElementColor(bracketN, ...)` で終わること
- import文、solid作成、profile作成など、ブラケット以外のコードは一切含めないこと
- スクリプト全体を出力しないこと
- **全候補生成**: 【ブラケット配置分析】の配置リストに記載された**すべてのブラケット**を生成すること。1つだけの例示や省略は禁止。bracketPram1, bracketPram2, ..., bracketPramN のように全件を出力すること
- エラー修正モードでは、失敗候補とその近縁候補を除外・置換してよい
- blacklist 済みの署名・近縁署名の候補は再生成しないこと
- `NameError` の場合でも、未定義変数の色設定行ではなく、対応する `CreateBracket` 候補を修正すること
- Side 系の未実績 `1501 / FL-FL` は避け、必要なら `1505 / PLS-FL + Sf1EndElements` を使うこと
- `BracketType=1505` では `Sf1EndElements` を省略しないこと

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
