## タスク
以下の【元のスクリプト】と【編集指示】を分析し、ブラケット配置仕様ドキュメントを作成してください。
**Pythonコードは一切出力しないこと。** Markdownの仕様ドキュメントのみ出力してください。

{reference_section}

{structure_section}

【元のスクリプト】

```python
{original_code}
```

-----

【編集指示】
{instruction}

-----

## 出力フォーマット（以下の形式で出力してください）

## ブラケット配置分析

### 対象部材とループ変数
- （例: profile1〜5: Stiffener FL 型）

### ブラケット配置リスト
| # | Surfaces1 | Surfaces2 | BracketType | BaseElement | 備考 |
|---|-----------|-----------|-------------|-------------|------|
| 1 | （例: solid1,PL） | （例: profile1[0],FL） | （例: 1505） | （例: profile1[0]） | （注意事項など） |

### ループ構造方針
- （例: profileN[0] を順番にループする）
- （例: 各 profileN に対して bracketPramN を作成する）

### パラメータ依存関係
- Height/Width/Thickness の計算ロジック
- End1/End2 の指定が必要かどうか

### 注意事項
- （参考スクリプトから読み取った重要な注意点）
