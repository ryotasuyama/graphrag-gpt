# query1227.py 修正計画書（ブラケット網羅性改善）

## 1. 背景・課題整理

### 1.1 現象
- `query1228.py` を以下で実行し生成された `1228-2.py` は、`samplename.py` に存在するブラケット（主に `...Deck.DP` 系）を中心に生成できている。
- しかし、正解データ `sample.py` と比べると **ブラケット数・配置系列が大幅に不足**している。

### 1.2 事実（差分の要点）
- `CreateBracket(` の個数  
  - `1228-2.py`: 20  
  - `sample.py`: 85  
  - **不足: 65（総数ベース）**
- `BracketName` の不足傾向（ユニーク名ベース）
  - `Deck.DP` 系は概ねあるが、`HK.Casing.Wall.Side.FR13.Deck.DP` が欠落
  - `Deck.AP/BP/CP` 系が **ほぼ全滅（系列展開できていない）**
  - `DL00` の `Deck.A/B/C/D` 系が欠落
  - **同名が2個必要（左右/鏡像）**なものが 1 個しか生成されていないケースがある  
    - 例: `HK.Casing.Deck.D.FR09P`, `HK.Casing.Deck.D.FR13P` など

### 1.3 根本原因（推定）
- 現在のプロンプトは「reference にある例の踏襲」寄りで安全側に倒れやすく、
  - **DPだけ**の再現に留まり、`AP/BP/CP` や `DL00`、左右対称の増殖（MirrorCopy/対称側生成）が発想として出にくい。
- `process_generation_loop` の自己修正は主に **COM例外（CreateBracket失敗）対応**であり、  
  **“不足（網羅性）” はエラーにならないため自動改善が走らない。**

---

## 2. 目的・ゴール

### 2.1 目的
`query1228.py` の生成プロンプトと自己修正戦略を拡張し、**ブラケットの網羅性（系列展開・対称・重複）を強制**して `sample.py` に近い出力を得る。

### 2.2 成功条件（Acceptance Criteria）
最低限、以下を満たすこと：

1. **系列網羅**
   - `...Deck.DP` が生成される箇所について、対応する `...Deck.AP/BP/CP` が生成されていること（同一FR/DLの系列展開）
2. **DL00 系列**
   - `HK.Casing.Wall.Fore.DL00.Deck.A/B/C/D` と `HK.Casing.Wall.Aft.DL00.Deck.A/B/C/D` が生成されること
3. **対称・重複**
   - reference で同名が複数存在する `BracketName` は、出力も同数を再現できていること  
     （例: `HK.Casing.Deck.D.FR09P`・`FR13P` が2個）
4. **量的指標**
   - `CreateBracket(` が **reference（samplename.py）程度で頭打ちにならない**  
   - 目標目安：`CreateBracket(` が **70以上**（理想は `sample.py` の 85 に近づく）

---

## 3. 対象範囲・非対象

### 3.1 対象
- `query1228.py` の以下の領域
  - `ask()` 内の `final_question`（referenceあり分岐）
  - `QA_TEMPLATE`（生成規約・ドメインルール）
  - （任意）網羅性セルフチェックによる自己修正ループの追加

### 3.2 非対象
- ナレッジグラフの内容更新
- EvoShip API 実装や外部環境の変更
- CADモデルの幾何検証（生成モデルを実際に解析して一致判定する、等）

---

## 4. 実装方針（優先度順）

## P0: プロンプト強化（最小改修で効果最大）

### 4.1 `ask()` の【ブラケット追加の前提ルール】拡張
- 現状のルール（Surfaces1/2, BaseElement, 候補探索, BracketType踏襲）に加えて、以下を明文化する：

追加要件（例）
- `Deck.DP` だけで終えない。**AP/BP/CP/DP を同一FR/DLで系列展開して網羅する**
- **DL00 の Deck.A/B/C/D** も生成対象とする（KG/既存実績に基づく）
- **同名ブラケットが複数必要なケースを再現**する（referenceや文脈に同名複数があるなら同数生成）
- 左右対称が成立する場合、以下いずれかで対称側を埋める
  - 対称側部材を参照してもう1個生成
  - `MirrorCopy([bracketX], "PL,Y", "")` で複製（利用可能なら推奨）
- 出力前セルフチェック（プロンプト内指示）：  
  `AP/BP/CP` / `DL00` / 同名複数 が欠けていないかを自己確認し、欠けていれば追加してから出力

※ 変更箇所目安：`ask()` の `final_question`（referenceあり分岐）内  
（現状は `【ブラケット追加の前提ルール】` が短い）

---

### 4.2 `QA_TEMPLATE` の「配置の完全性」セクション増強
- 現在の「漏れなく配置」「初期化継承」に加え、以下の思想を文章化する：

追加要件（例）
- “参考スクリプトは最小例” とみなし、**命名規則の系列（AP/BP/CP/DP, DL00 A/B/C/D）を文脈から展開**して網羅
- “同名の複数出現” を仕様として扱い、**個数も再現**する

---

## P1: 質問文の自動拡張（retrieval/発想の偏りを補正）

### 4.3 instruction（question）の自動補強
- CLI の編集指示が短い（例: 「ブラケットをつけてください。」）場合に、
  `ask()` 内で **ブラケット網羅要件を追記した instruction を LLM に渡す**。

実装案（方針）
- `question` に `"ブラケット"` などが含まれる場合のみ発動
- 追記内容に以下を含める
  - AP/BP/CP/DP の網羅
  - DL00 A/B/C/D
  - 同名複数・対称（MirrorCopy可）

注意
- ブラケット以外の編集タスクへの副作用を避けるため、**条件付きで拡張**する

---

## P2: “網羅性不足” をトリガにした自己修正ループ（任意だが強い）

### 4.4 静的セルフチェック（コード解析）を追加
- スクリプト実行エラーが無い場合でも、生成コードを解析して **ブラケット不足を検出**し再生成に回す。

実装要素
- 生成コードから `BracketName="..."` を正規表現で抽出
- 以下をチェックして不足理由をテキスト化
  1) `.Deck.DP` があるのに `.Deck.AP/BP/CP` が少ない/無い
  2) `DL00 Deck.A/B/C/D` が無い
  3) reference 内で同名複数の `BracketName` が、出力では1個しかない
  4) `FR13` など明らかな穴（FR系列が連続なのに欠番）がある

自己修正の呼び出し先
- 既存の `fix_bracket_code` は「最小変更ポリシー」で網羅性追加に不向きなため、
  - 新規に `BRACKET_COVERAGE_FIX_TEMPLATE` を追加し、
  - “不足の追加” に特化した修正を依頼する（**既存のブラケットは維持し、追加のみ**）

ループ統合案
- `process_generation_loop` の attempt>0 分岐に “網羅性不足” を追加トリガとして組み込む  
  - エラー修正（COM例外）: 既存フローのまま  
  - 網羅性不足: coverage fix プロンプトで再生成

---

## 5. 変更点一覧（作業タスク）

### Task A（P0）: `ask()` のルール拡張
- ファイル: `query1227.py`
- 対象: `ask()` 内 `final_question`（referenceあり分岐）の `【ブラケット追加の前提ルール】`
- 作業:
  - AP/BP/CP の系列展開
  - DL00 A/B/C/D
  - 同名複数再現
  - 対称生成（MirrorCopy可）
  - 出力前セルフチェックの明文化

### Task B（P0）: `QA_TEMPLATE` の配置完全性ルール強化
- `QA_TEMPLATE` の 3) に “系列展開・同名複数” の規約を追加

### Task C（P1）: question 自動拡張（条件付き）
- `if "ブラケット" in question:` のような判定で拡張
- 拡張文言は `ask()` のルールと整合

### Task D（P2 / 任意）: 網羅性セルフチェックと再生成
- `extract_bracket_names(code)` の追加
- `evaluate_bracket_coverage(names, reference_names)` の追加
- 新規テンプレ `BRACKET_COVERAGE_FIX_TEMPLATE` の追加
- `process_generation_loop` に coverage 判定→再生成を統合

---

## 7. リスクと対策

### 7.1 過剰生成によるCOM例外増加
- 対策
  - 既存の `fix_bracket_code` で例外補正できる設計を維持
  - coverage fix は “追加のみ/既存維持” を徹底して破壊的変更を避ける
  - 追加時は候補面（Surfaces1/2）を “End1/End2 + AddAttachSurfaces” から探索するルールを強制

### 7.2 ブラケット以外タスクへの副作用
- 対策
  - question 自動拡張は `"ブラケット"` 含有時のみ
  - coverageループも `"ブラケット"` タスク時のみ有効化（必要ならフラグ化）

---

## 9. 実施順序（推奨）
1) Task A（askのルール拡張）  
2) Task B（QA_TEMPLATE強化）  
3) Task C（question条件付き拡張）  

---
