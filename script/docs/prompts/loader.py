import os
import functools

PROMPTS_DIR = os.path.dirname(os.path.abspath(__file__))

BRACKET_KEYWORDS = ["ブラケット", "bracket", "createbracket", "bracketparam"]


@functools.lru_cache(maxsize=None)
def load_prompt(name: str) -> str:
    """プロンプトファイルを名前で読込（キャッシュ付き）"""
    path = os.path.join(PROMPTS_DIR, f"{name}.md")
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


@functools.lru_cache(maxsize=None)
def load_example(name: str) -> str:
    """examples/ からコード例を読込（キャッシュ付き）"""
    path = os.path.join(PROMPTS_DIR, "examples", f"{name}.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def is_bracket_task(instruction: str, reference_code: str = None) -> bool:
    """ブラケット関連タスクかどうか判定"""
    instruction_lower = instruction.lower()
    if any(kw in instruction_lower for kw in BRACKET_KEYWORDS):
        return True
    if reference_code and "CreateBracket" in reference_code:
        return True
    return False


def extract_bracket_section_from_code(code: str) -> str:
    """参考スクリプトからブラケットセクションのみを抽出する"""
    import re
    marker = "bracketPram1 = part.CreateBracketParam()"
    idx = code.find(marker)
    if idx != -1:
        return code[idx:].strip()
    # フォールバック: bracketParam variant
    alt_match = re.search(r'bracketP(?:ram|aram)\w*\s*=\s*part\.CreateBracketParam\(\)', code)
    if alt_match:
        return code[alt_match.start():].strip()
    return ""


def build_analysis_prompt(
    instruction: str,
    original_code: str,
    reference_code: str = None,
    structure_summary: str = "",
    candidates_summary: str = "",
) -> str:
    """Agent 1: ブラケット配置分析プロンプトを構築"""
    parts = [load_prompt("base_system")]

    # 参考スクリプトの有無で分析ガイドを切替
    if reference_code:
        parts.append(load_prompt("bracket_analysis_guide"))
    else:
        parts.append(load_prompt("bracket_analysis_guide_noref"))

    reference_section = ""
    if reference_code:
        reference_section = f"【参考スクリプト】\n\n```python\n{reference_code}\n```\n"

    # 構造解析結果の組み立て
    structure_section = ""
    if structure_summary or candidates_summary:
        parts_struct = []
        if structure_summary:
            parts_struct.append("## 自動解析: スクリプト構造\n\n" + structure_summary)
        if candidates_summary:
            parts_struct.append("## 自動解析: ブラケット候補\n\n" + candidates_summary)
        structure_section = "\n\n".join(parts_struct)

    template = load_prompt("bracket_placement_analysis")
    question = template.format(
        instruction=instruction,
        original_code=original_code,
        reference_section=reference_section,
        structure_section=structure_section,
    )

    parts.append(question)
    return "\n\n".join(parts)


def build_bracket_section_prompt(
    analysis_document: str,
    reference_code: str = None,
    structure_summary: str = "",
) -> str:
    """Agent 2: ブラケットセクション生成プロンプトを構築"""
    parts = [load_prompt("base_system")]
    parts.append(load_prompt("bracket_domain_rules"))
    parts.append("## 参考コード例（BracketType 1505: PLS × Profile FL）")
    parts.append("```python\n" + load_example("bracket_1505") + "\n```")
    parts.append("## 参考コード例（BracketType 1501: Profile FL × Profile FL）")
    parts.append("```python\n" + load_example("bracket_1501") + "\n```")

    reference_bracket_examples = ""
    if reference_code:
        bracket_section = extract_bracket_section_from_code(reference_code)
        if bracket_section:
            reference_bracket_examples = f"【参考スクリプトのブラケットセクション】\n\n```python\n{bracket_section}\n```\n"

    # 構造情報をAgent 2にも提供
    if structure_summary:
        parts.append("## スクリプト構造情報\n\n" + structure_summary)

    template = load_prompt("bracket_section_generation")
    question = template.format(
        analysis_document=analysis_document,
        reference_bracket_examples=reference_bracket_examples,
        error_context_section="",
    )

    parts.append(question)
    return "\n\n".join(parts)


def _build_error_context_block(error_context: dict) -> str:
    """エラーコンテキストブロックを文字列として組み立てる"""
    stderr = error_context.get("stderr", "")
    line_number = error_context.get("line_number", "unknown")
    error_line = error_context.get("error_line", "")
    bracket_param_section = error_context.get("bracket_param_section", "")

    block = (
        "## エラー修正モード\n\n"
        "前回生成したブラケットセクションを実行したところ、以下のエラーが発生しました。\n"
        "**同じ分析ドキュメントに基づいて、このエラーを修正したブラケットセクションを再生成してください。**\n\n"
        f"### エラートレースバック\n```\n{stderr}\n```\n\n"
        f"### 失敗行（行{line_number}）\n```python\n{error_line}\n```\n\n"
        f"### 失敗したブラケットパラメータ定義\n```python\n{bracket_param_section}\n```\n\n"
        "### ブラケット修正チェックリスト（以下を順に確認して修正）\n"
        "0. **表示状態（Blank）**: `CreateBracket(bracketParam, True)` → 必ず False に。`BlankElement(bracketX, True)` は削除。\n"
        "1. **Surfaces1/Surfaces2**: 面が None/未生成/型不一致でないか。面ペア順序（PLS↔FL等）が正しいか。\n"
        "2. **BaseElement**: 原則 `profileXX[0]` を使う。solid を渡していないか。\n"
        "3. **End1/End2 と EndElements**: 対応する要素が欠けていないか。\n"
        "4. **BracketType とフィールドの整合**: 参考スクリプトの同型を優先。\n"
        "5. **寸法の符号・範囲**: Height/Width/Thickness が 0 以下でないか。\n"
        "6. **向き（Orientation/Vector）**: 参照面の法線に対して不正でないか。\n"
    )

    # COM例外の場合、追加のデバッグガイドを付与
    if "com_error" in stderr.lower() or "com" in stderr.lower():
        try:
            block += "\n\n" + load_prompt("bracket_validation_rules")
        except FileNotFoundError:
            pass
        block += (
            "\n\n### 代替アプローチの提案\n"
            "上記チェックリストで解決しない場合、以下を試してください:\n"
            "- **Surfaces1 のシート→ソリッド変換**: `extrude_sheetN` をSurfaces1に使用している場合、"
            "そのシートが `CreateThicken` でソリッド化されていれば `solidN` に置き換えてください。"
            "スクリプト構造情報のThickenセクションまたは候補テーブルの「Solid代替」列で対応を確認できます。\n"
            "- **Sf1EndElements の法線方向を反転**: `RevSf1=True` を試すか、法線の符号を全て反転してください。\n"
            "- **BracketName の重複回避**: 各ブラケットに一意の BracketName を付けてください。\n"
        )

    # 単一ブラケットモード
    if error_context.get("single_bracket_mode"):
        block += (
            "\n\n## 重要: 単一ブラケットモード\n\n"
            "COM例外が繰り返し発生しています。\n"
            "**ブラケットを1つだけ（bracketPram1のみ）生成してください。**\n"
            "最も単純なケース（ProfileType=1003のEnd1側、BracketType=1505）を選んでください。\n"
        )

    return block


def build_bracket_section_prompt_with_error(
    analysis_document: str,
    reference_code: str = None,
    error_context: dict = None,
    structure_summary: str = "",
) -> str:
    """Agent 2 (リトライ版): エラーコンテキスト付きでブラケットセクション生成プロンプトを構築"""
    parts = [load_prompt("base_system")]
    parts.append(load_prompt("bracket_domain_rules"))
    parts.append("## 参考コード例（BracketType 1505: PLS × Profile FL）")
    parts.append("```python\n" + load_example("bracket_1505") + "\n```")
    parts.append("## 参考コード例（BracketType 1501: Profile FL × Profile FL）")
    parts.append("```python\n" + load_example("bracket_1501") + "\n```")

    reference_bracket_examples = ""
    if reference_code:
        bracket_section = extract_bracket_section_from_code(reference_code)
        if bracket_section:
            reference_bracket_examples = f"【参考スクリプトのブラケットセクション】\n\n```python\n{bracket_section}\n```\n"

    # 構造情報をAgent 2にも提供
    if structure_summary:
        parts.append("## スクリプト構造情報\n\n" + structure_summary)

    error_context_section = ""
    if error_context:
        error_context_section = _build_error_context_block(error_context)

    template = load_prompt("bracket_section_generation")
    question = template.format(
        analysis_document=analysis_document,
        reference_bracket_examples=reference_bracket_examples,
        error_context_section=error_context_section,
    )

    parts.append(question)
    return "\n\n".join(parts)


def format_group_candidates_for_prompt(group: dict) -> str:
    """
    グループの候補を Markdown テーブルとして整形する（Agent 2 JSON プロンプト向け）。
    事前計算済みデータ（変数名・法線・Solid参照）を表示する。
    """
    lines = []
    lines.append(
        "| # | candidate_id | profile_var | End | base_element | mold | "
        "PLS法線(n0,n1,n2) | surfaces1_ref | sf1_end_normal | sf1_end_element | "
        "ProfileParams | profile_name |"
    )
    lines.append(
        "|---|--------------|-------------|-----|--------------|------|"
        "------------------|---------------|----------------|-----------------|"
        "---------------|--------------|"
    )
    for i, c in enumerate(group["candidates"], 1):
        pls = ",".join(c.get("surfaces1_pls_normal", [])) or "-"
        end_n = ",".join(c.get("sf1_end_normal", [])) or "-"
        surf1_ref = c.get("attach_surface_solid") or c.get("attach_surface", "-")
        lines.append(
            f"| {i} | {c['id']} | {c['profile_var']} | {c['end_side']} "
            f"| {c['base_element']} | {c.get('mold', '+')} "
            f"| {pls} | {surf1_ref} | {end_n} | {c.get('sf1_end_element', '-')} "
            f"| [{c.get('profile_params', '')}] | {c.get('profile_name', '')} |"
        )
    return "\n".join(lines)


def extract_json_from_llm_response(content: str) -> dict | None:
    """
    LLM レスポンスから JSON ブロックを抽出してパースする。
    ```json ... ``` ブロックを優先し、なければ裸の { } を試みる。
    """
    import json
    import re

    # ```json ... ``` ブロックを探す
    match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # ``` ... ``` ブロック（言語指定なし）を試みる
    match = re.search(r'```\s*([\{\[].*?)\s*```', content, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # 裸の JSON を試みる（最初の { から最後の } まで）
    brace_match = re.search(r'\{.*\}', content, re.DOTALL)
    if brace_match:
        try:
            return json.loads(brace_match.group(0))
        except json.JSONDecodeError:
            pass

    return None


def _build_group_json_error_context_block(error_ctx: dict) -> str:
    """JSON モードのエラーコンテキストブロックを組み立てる"""
    block = (
        "## エラー修正モード\n\n"
        "前回生成した JSON に基づいてブラケットコードを実行したところ、以下のエラーが発生しました。\n"
        "**同じグループの候補について、このエラーを修正した JSON を再出力してください。**\n\n"
    )
    stderr = error_ctx.get("stderr", "")
    if stderr:
        block += f"### エラートレースバック\n```\n{stderr}\n```\n\n"
    json_used = error_ctx.get("json_used", "")
    if json_used:
        block += f"### 前回使用した JSON\n```json\n{json_used}\n```\n\n"
    generated_code = error_ctx.get("generated_code", "")
    if generated_code:
        block += f"### テンプレートが生成したコード（参考）\n```python\n{generated_code}\n```\n\n"
    block += (
        "### 修正チェックリスト\n"
        "- `thickness` が 0 以下でないか確認してください\n"
        "- `sf1_dimension_params` / `sf2_dimension_params` の値が有効な範囲か確認してください\n"
        "- `bracket_type` が候補の接続形式（PLS×FL = 1505、FL×FL = 1501）と一致しているか確認してください\n"
        "- BracketType 1501 の場合は `surfaces2_ref` が設定されているか確認してください\n"
        "- `bracket_name` が他のブラケットと重複していないか確認してください\n"
    )
    return block


def build_bracket_group_json_prompt(
    group: dict,
    analysis_document: str,
    reference_code: str = None,
    structure_summary: str = "",
) -> str:
    """
    Agent 2 (batch JSON モード): グループ単位のブラケット JSON 生成プロンプトを構築する。
    """
    parts = [load_prompt("base_system")]
    parts.append(load_prompt("bracket_domain_rules"))
    parts.append("## 参考コード例（BracketType 1505: PLS × Profile FL）")
    parts.append("```python\n" + load_example("bracket_1505") + "\n```")
    parts.append("## 参考コード例（BracketType 1501: Profile FL × Profile FL）")
    parts.append("```python\n" + load_example("bracket_1501") + "\n```")

    reference_bracket_examples = ""
    if reference_code:
        bracket_section = extract_bracket_section_from_code(reference_code)
        if bracket_section:
            reference_bracket_examples = (
                f"【参考スクリプトのブラケットセクション】\n\n```python\n{bracket_section}\n```\n"
            )

    if structure_summary:
        parts.append("## スクリプト構造情報\n\n" + structure_summary)

    if analysis_document:
        parts.append("## ブラケット配置分析（Agent 1 の出力）\n\n" + analysis_document)

    prefilled_table = format_group_candidates_for_prompt(group)
    group_name = f"{group['attach_surface']} ({group.get('attach_surface_name', '')})"
    group_candidates_detail = _build_group_candidates_detail(group)
    num_candidates = len(group["candidates"])

    template = load_prompt("bracket_section_generation_json")
    question = template.format(
        error_context_section="",
        reference_bracket_examples=reference_bracket_examples,
        prefilled_table=prefilled_table,
        group_name=group_name,
        group_candidates_detail=group_candidates_detail,
        num_candidates=num_candidates,
    )
    parts.append(question)
    return "\n\n".join(parts)


def build_bracket_group_json_prompt_with_error(
    group: dict,
    analysis_document: str,
    reference_code: str = None,
    structure_summary: str = "",
    error_ctx: dict = None,
) -> str:
    """
    Agent 2 (batch JSON モード、エラーリトライ): エラーコンテキスト付きプロンプトを構築する。
    """
    parts = [load_prompt("base_system")]
    parts.append(load_prompt("bracket_domain_rules"))
    parts.append("## 参考コード例（BracketType 1505: PLS × Profile FL）")
    parts.append("```python\n" + load_example("bracket_1505") + "\n```")
    parts.append("## 参考コード例（BracketType 1501: Profile FL × Profile FL）")
    parts.append("```python\n" + load_example("bracket_1501") + "\n```")

    reference_bracket_examples = ""
    if reference_code:
        bracket_section = extract_bracket_section_from_code(reference_code)
        if bracket_section:
            reference_bracket_examples = (
                f"【参考スクリプトのブラケットセクション】\n\n```python\n{bracket_section}\n```\n"
            )

    if structure_summary:
        parts.append("## スクリプト構造情報\n\n" + structure_summary)

    if analysis_document:
        parts.append("## ブラケット配置分析（Agent 1 の出力）\n\n" + analysis_document)

    error_context_section = ""
    if error_ctx:
        error_context_section = _build_group_json_error_context_block(error_ctx)

    prefilled_table = format_group_candidates_for_prompt(group)
    group_name = f"{group['attach_surface']} ({group.get('attach_surface_name', '')})"
    group_candidates_detail = _build_group_candidates_detail(group)
    num_candidates = len(group["candidates"])

    template = load_prompt("bracket_section_generation_json")
    question = template.format(
        error_context_section=error_context_section,
        reference_bracket_examples=reference_bracket_examples,
        prefilled_table=prefilled_table,
        group_name=group_name,
        group_candidates_detail=group_candidates_detail,
        num_candidates=num_candidates,
    )
    parts.append(question)
    return "\n\n".join(parts)


def _build_group_candidates_detail(group: dict) -> str:
    """グループの各候補の詳細を箇条書き形式で整形する"""
    lines = []
    for i, c in enumerate(group["candidates"], 1):
        pls = ", ".join(c.get("surfaces1_pls_normal", [])) or "-"
        end_n = ", ".join(c.get("sf1_end_normal", [])) or "-"
        surf1_ref = c.get("attach_surface_solid") or c.get("attach_surface", "-")
        lines.append(
            f"**候補 {i}** (candidate_id={c['id']})\n"
            f"  - profile_var: `{c['profile_var']}`, End: {c['end_side']}\n"
            f"  - base_element: `{c['base_element']}`, mold: `{c.get('mold', '+')}`\n"
            f"  - surfaces1_ref (Surfaces1 solid): `{surf1_ref}`\n"
            f"  - surfaces1_pls_normal: `{pls}`\n"
            f"  - sf1_end_element: `{c.get('sf1_end_element', '-')}`\n"
            f"  - sf1_end_normal: `{end_n}`\n"
            f"  - profile_name: {c.get('profile_name', '-')}\n"
            f"  - profile_params (ProfileParams): [{c.get('profile_params', '')}]\n"
            f"  - 推定 bracket_type: {c.get('bracket_type', 1505)}"
        )
    return "\n\n".join(lines)


def build_generation_prompt(question: str, is_bracket: bool) -> str:
    """レイヤーを組み立ててプロンプトを構築"""
    parts = [load_prompt("base_system")]

    if is_bracket:
        parts.append(load_prompt("bracket_analysis_guide"))
        parts.append(load_prompt("bracket_domain_rules"))
        parts.append("## 参考コード例（BracketType 1505: PLS × Profile FL）")
        parts.append("```python\n" + load_example("bracket_1505") + "\n```")
        parts.append("## 参考コード例（BracketType 1501: Profile FL × Profile FL）")
        parts.append("```python\n" + load_example("bracket_1501") + "\n```")

    parts.append(load_prompt("output_format"))

    template = "\n\n".join(parts)
    return template.format(question=question)
