"""
EvoShip スクリプト構造解析モジュール

元スクリプトを正規表現で解析し、LLMに渡す構造メタデータを生成する。
参考スクリプトなしでもブラケット候補を自動検出するために使用。
"""
import re
from typing import Optional


# ========== 正規表現パターン ==========

# シート生成: extrude_sheetN = part.CreateLinearSweepSheet(...)
RE_SHEET = re.compile(
    r'(extrude_sheet\d+)\s*=\s*part\.CreateLinearSweepSheet\((\w+),\s*(?:True|False)\)'
)
# シートの法線: part.SheetAlignNormal(extrude_sheetN, nx, ny, nz)
RE_SHEET_NORMAL = re.compile(
    r'part\.SheetAlignNormal\((\w+),\s*([^,]+),\s*([^,]+),\s*([^)]+)\)'
)
# SweepParam の Name: extrudePramN.Name="..."
RE_SWEEP_NAME = re.compile(
    r'(extrudePram\d+)\.Name\s*=\s*"([^"]*)"'
)
# SweepParam の SweepDirection: extrudePramN.SweepDirection="..."
RE_SWEEP_DIR = re.compile(
    r'(extrudePram\d+)\.SweepDirection\s*=\s*"([^"]*)"'
)

# ソリッド生成: solidN = part.CreateSolid("name","","material")
RE_SOLID = re.compile(
    r'(solid\d+)\s*=\s*part\.CreateSolid\(\s*"([^"]*)"'
)
# Thicken: thickenN = part.CreateThicken("name", solidN, "dir", [extrude_sheetN])
RE_THICKEN = re.compile(
    r'(thicken\d+)\s*=\s*part\.CreateThicken\(\s*"[^"]*"\s*,\s*(\w+)\s*,\s*"[^"]*"\s*,\s*\[(\w+)\]'
)
# Thicken フォールバック（sheet変数なし）
RE_THICKEN_FALLBACK = re.compile(
    r'(thicken\d+)\s*=\s*part\.CreateThicken\(\s*"[^"]*"\s*,\s*(\w+)\s*,'
)

# ProfileParam 生成: ProfilePramN = part.CreateProfileParam()
RE_PROFILE_PARAM = re.compile(
    r'(ProfilePram\d+)\s*=\s*part\.CreateProfileParam\(\)'
)
# Profile 生成: profileN = part.CreateProfile(ProfilePramN, ...)
RE_PROFILE = re.compile(
    r'(profile\d+)\s*=\s*part\.CreateProfile\((\w+),\s*(?:True|False)\)'
)

# Profile属性パターン
RE_ATTACH_SURF = re.compile(r'(\w+)\.AddAttachSurfaces\((\w+)\)')
RE_PROFILE_TYPE = re.compile(r'(\w+)\.ProfileType\s*=\s*(\d+)')
RE_PROFILE_PARAMS = re.compile(r'(\w+)\.ProfileParams\s*=\s*\[([^\]]*)\]')
RE_PROFILE_NAME = re.compile(r'(\w+)\.ProfileName\s*=\s*"([^"]*)"')
RE_MOLD = re.compile(r'(\w+)\.Mold\s*=\s*"([^"]*)"')
RE_END1_ELEMENTS = re.compile(r'(\w+)\.AddEnd1Elements\((\w+)\)')
RE_END2_ELEMENTS = re.compile(r'(\w+)\.AddEnd2Elements\((\w+)\)')
RE_END1_TYPE = re.compile(r'(\w+)\.End1Type\s*=\s*(\d+)')
RE_END2_TYPE = re.compile(r'(\w+)\.End2Type\s*=\s*(\d+)')
RE_FLANGE_NAME = re.compile(r'(\w+)\.FlangeName\s*=\s*"([^"]*)"')

# MirrorCopy: mirror_copiedN = part.MirrorCopy([profileN[0]], "PL,Y", "")
# ソースにprofileN[0]のような[]を含む場合があるため、最後の]までマッチ
RE_MIRROR = re.compile(
    r'(mirror_copied\d+)\s*=\s*part\.MirrorCopy\(\[(.+?)\]\s*,\s*"([^"]*)"'
)

# Variable: var_elmN = part.CreateVariable("name","value","unit","")
RE_VARIABLE = re.compile(
    r'(var_elm\d+)\s*=\s*part\.CreateVariable\(\s*"([^"]*)"\s*,\s*"([^"]*)"\s*,'
)


def extract_script_structure(code: str) -> dict:
    """
    EvoShipスクリプトを正規表現で解析し、構造メタデータを返す。
    """
    # --- SweepParam の Name / Direction マッピング ---
    sweep_names = {}
    for m in RE_SWEEP_NAME.finditer(code):
        sweep_names[m.group(1)] = m.group(2)

    sweep_dirs = {}
    for m in RE_SWEEP_DIR.finditer(code):
        sweep_dirs[m.group(1)] = m.group(2)

    # SweepParam → Sheet の対応
    sweep_to_sheet = {}
    for m in RE_SHEET.finditer(code):
        sweep_to_sheet[m.group(2)] = m.group(1)

    # --- シート ---
    sheet_normals = {}
    for m in RE_SHEET_NORMAL.finditer(code):
        sheet_normals[m.group(1)] = [m.group(2).strip(), m.group(3).strip(), m.group(4).strip()]

    sheets = []
    for m in RE_SHEET.finditer(code):
        sheet_var = m.group(1)
        param_var = m.group(2)
        sheets.append({
            "var": sheet_var,
            "name": sweep_names.get(param_var, ""),
            "sweep_direction": sweep_dirs.get(param_var, ""),
            "normal": sheet_normals.get(sheet_var, []),
        })

    # --- ソリッド ---
    solids = []
    for m in RE_SOLID.finditer(code):
        solids.append({
            "var": m.group(1),
            "name": m.group(2),
        })

    # --- Thicken ---
    thickens = []
    thicken_matched_vars = set()
    for m in RE_THICKEN.finditer(code):
        thickens.append({
            "var": m.group(1),
            "solid_var": m.group(2),
            "sheet_var": m.group(3),
        })
        thicken_matched_vars.add(m.group(1))
    # フォールバック: sheet変数をキャプチャできなかったThicken
    for m in RE_THICKEN_FALLBACK.finditer(code):
        if m.group(1) not in thicken_matched_vars:
            thickens.append({
                "var": m.group(1),
                "solid_var": m.group(2),
                "sheet_var": "",
            })

    # --- Profile属性の収集 ---
    # まずProfileParam変数ごとに属性をまとめる
    param_attrs = {}
    for m in RE_PROFILE_PARAM.finditer(code):
        param_attrs[m.group(1)] = {}

    def _set_attr(regex, attr_name, converter=None):
        for m in regex.finditer(code):
            pvar = m.group(1)
            val = m.group(2)
            if pvar in param_attrs:
                param_attrs[pvar][attr_name] = converter(val) if converter else val

    _set_attr(RE_ATTACH_SURF, "attach_surface")
    _set_attr(RE_PROFILE_TYPE, "profile_type", int)
    _set_attr(RE_PROFILE_PARAMS, "profile_params")
    _set_attr(RE_PROFILE_NAME, "profile_name")
    _set_attr(RE_MOLD, "mold")
    _set_attr(RE_END1_ELEMENTS, "end1_elements")
    _set_attr(RE_END2_ELEMENTS, "end2_elements")
    _set_attr(RE_END1_TYPE, "end1_type", int)
    _set_attr(RE_END2_TYPE, "end2_type", int)
    _set_attr(RE_FLANGE_NAME, "flange_name")

    # ProfileParam → profile変数 の対応
    profiles = []
    for m in RE_PROFILE.finditer(code):
        profile_var = m.group(1)
        param_var = m.group(2)
        attrs = param_attrs.get(param_var, {})
        profiles.append({
            "var": profile_var,
            "param_var": param_var,
            "profile_type": attrs.get("profile_type"),
            "profile_params": attrs.get("profile_params", ""),
            "profile_name": attrs.get("profile_name", ""),
            "attach_surface": attrs.get("attach_surface", ""),
            "end1_elements": attrs.get("end1_elements", ""),
            "end2_elements": attrs.get("end2_elements", ""),
            "end1_type": attrs.get("end1_type"),
            "end2_type": attrs.get("end2_type"),
            "mold": attrs.get("mold", ""),
            "has_flange": bool(attrs.get("flange_name")),
        })

    # --- MirrorCopy ---
    mirrors = []
    for m in RE_MIRROR.finditer(code):
        mirrors.append({
            "var": m.group(1),
            "source": m.group(2).strip(),
            "mirror_plane": m.group(3),
        })

    # --- Variable ---
    variables = []
    for m in RE_VARIABLE.finditer(code):
        variables.append({
            "var": m.group(1),
            "name": m.group(2),
            "value": m.group(3),
        })

    return {
        "sheets": sheets,
        "solids": solids,
        "thickens": thickens,
        "profiles": profiles,
        "mirrors": mirrors,
        "variables": variables,
    }


def detect_bracket_candidates(structure: dict) -> list:
    """
    構造情報からブラケット候補を自動検出する。

    判定ロジック:
    - ProfileType 1002/1003/1201/1007 のプロファイルが対象
    - 各End1/End2接続先ごとに1つのブラケット候補
    - AttachSurface(板) × Profile(FL) → BracketType 1505
    - ミラーコピーされたプロファイルはスキップ（オリジナル側のみ）
    """
    # シート法線のルックアップ
    sheet_normals = {}
    sheet_names = {}
    for s in structure["sheets"]:
        sheet_normals[s["var"]] = s.get("normal", [])
        sheet_names[s["var"]] = s.get("name", "")

    # Sheet → Solid マッピング（Thicken経由）
    sheet_to_solid = {}
    for t in structure["thickens"]:
        sheet_var = t.get("sheet_var", "")
        if sheet_var:
            sheet_to_solid[sheet_var] = t["solid_var"]

    # ミラーコピーのソース一覧（ミラーされたprofileは除外しない、ソースのみ対象）
    mirrored_sources = set()
    for m in structure["mirrors"]:
        mirrored_sources.add(m["source"])

    candidates = []
    candidate_id = 1

    for prof in structure["profiles"]:
        ptype = prof.get("profile_type")
        if ptype not in (1002, 1003, 1201, 1007):
            continue

        attach_surf = prof.get("attach_surface", "")
        attach_normal = sheet_normals.get(attach_surf, [])

        for end_side, end_elem_key in [("End1", "end1_elements"), ("End2", "end2_elements")]:
            end_elem = prof.get(end_elem_key, "")
            if not end_elem:
                continue

            end_normal = sheet_normals.get(end_elem, [])

            # PLS法線ベクトルの符号反転（Surfaces1用）
            # 通常 "0","-0","-1" のような形式
            pls_normal = _invert_normal(attach_normal) if attach_normal else []

            # Sf1EndElements 用の法線
            sf1_end_normal = _invert_normal(end_normal) if end_normal else []

            # BracketType の判定
            # End要素がシートなら 1505 (Plate x Profile)
            bracket_type = 1505  # デフォルト

            candidates.append({
                "id": candidate_id,
                "profile_var": prof["var"],
                "profile_type": ptype,
                "profile_name": prof.get("profile_name", ""),
                "end_side": end_side,
                "attach_surface": attach_surf,
                "attach_surface_name": sheet_names.get(attach_surf, ""),
                "attach_surface_solid": sheet_to_solid.get(attach_surf, ""),
                "end_element": end_elem,
                "end_element_name": sheet_names.get(end_elem, ""),
                "bracket_type": bracket_type,
                "base_element": f"{prof['var']}[0]",
                "surfaces1_pls_normal": pls_normal,
                "sf1_end_element": end_elem,
                "sf1_end_normal": sf1_end_normal,
                "mold": prof.get("mold", "+"),
                "profile_params": prof.get("profile_params", ""),
            })
            candidate_id += 1

    return candidates


def _invert_normal(normal: list) -> list:
    """法線ベクトルの符号を反転する（文字列リスト）"""
    result = []
    for v in normal:
        v = v.strip()
        try:
            fval = float(v)
            if fval == 0:
                result.append("0")
            else:
                result.append(str(-fval).rstrip('0').rstrip('.') if -fval != int(-fval) else str(int(-fval)))
        except ValueError:
            result.append(v)
    return result


def format_structure_for_prompt(structure: dict) -> str:
    """構造情報をMarkdownテーブルに整形"""
    lines = []

    # Sheets
    lines.append("### シート/板（Sheets）")
    lines.append("| 変数 | 名前 | SweepDirection | 法線 (nx,ny,nz) |")
    lines.append("|------|------|----------------|-----------------|")
    for s in structure["sheets"]:
        normal_str = ",".join(s.get("normal", [])) if s.get("normal") else "-"
        lines.append(f"| {s['var']} | {s['name']} | {s['sweep_direction']} | {normal_str} |")

    lines.append("")

    # Solids
    if structure["solids"]:
        lines.append("### ソリッド（Solids）")
        lines.append("| 変数 | 名前 |")
        lines.append("|------|------|")
        for s in structure["solids"]:
            lines.append(f"| {s['var']} | {s['name']} |")
        lines.append("")

    # Profiles
    lines.append("### プロファイル（Profiles）")
    lines.append("| 変数 | ProfileType | AttachSurface | End1Elements | End2Elements | Mold | ProfileParams | Flange |")
    lines.append("|------|-------------|---------------|--------------|--------------|------|---------------|--------|")
    for p in structure["profiles"]:
        pparams = p.get("profile_params", "")
        flange = "Yes" if p.get("has_flange") else "-"
        lines.append(
            f"| {p['var']} | {p.get('profile_type', '-')} | {p.get('attach_surface', '-')} "
            f"| {p.get('end1_elements', '-')} | {p.get('end2_elements', '-')} "
            f"| {p.get('mold', '-')} | [{pparams}] | {flange} |"
        )

    lines.append("")

    # Mirrors
    if structure["mirrors"]:
        lines.append("### ミラーコピー（MirrorCopy）")
        lines.append("| 変数 | ソース | ミラー面 |")
        lines.append("|------|--------|----------|")
        for m in structure["mirrors"]:
            lines.append(f"| {m['var']} | {m['source']} | {m['mirror_plane']} |")
        lines.append("")

    return "\n".join(lines)


def format_candidates_for_prompt(candidates: list) -> str:
    """ブラケット候補をMarkdownテーブルに整形"""
    if not candidates:
        return "ブラケット候補が自動検出されませんでした。"

    lines = []
    lines.append("| # | Profile | End | AttachSurface | EndElement | BracketType | BaseElement | PLS法線 | EndElement法線 | Solid代替 | 備考 |")
    lines.append("|---|---------|-----|---------------|------------|-------------|-------------|---------|----------------|-----------|------|")
    for c in candidates:
        pls_n = ",".join(c.get("surfaces1_pls_normal", [])) if c.get("surfaces1_pls_normal") else "-"
        end_n = ",".join(c.get("sf1_end_normal", [])) if c.get("sf1_end_normal") else "-"
        solid_alt = c.get("attach_surface_solid", "") or "-"
        note = f"{c.get('attach_surface_name', '')} × {c.get('end_element_name', '')}"
        lines.append(
            f"| {c['id']} | {c['profile_var']} (Type {c['profile_type']}) "
            f"| {c['end_side']} | {c['attach_surface']} | {c['end_element']} "
            f"| {c['bracket_type']} | {c['base_element']} | {pls_n} | {end_n} | {solid_alt} | {note} |"
        )

    return "\n".join(lines)


def validate_bracket_section(bracket_code: str, structure: dict) -> list:
    """
    生成されたブラケットコードを静的に検証する。

    Returns:
        [{"level": "error"|"warning", "message": str, "line": int|None, "auto_fix": str|None}]
    """
    issues = []
    lines = bracket_code.split("\n")

    # 既知の変数セットを構築
    known_vars = set()
    for s in structure["sheets"]:
        known_vars.add(s["var"])
    for s in structure["solids"]:
        known_vars.add(s["var"])
    for p in structure["profiles"]:
        known_vars.add(p["var"])
        known_vars.add(f"{p['var']}[0]")
        known_vars.add(f"{p['var']}[1]")
    for m in structure["mirrors"]:
        known_vars.add(m["var"])
    for t in structure.get("thickens", []):
        known_vars.add(t["var"])

    for i, line in enumerate(lines, 1):
        # Check 1: CreateBracket second arg must be False
        cb_match = re.search(r'part\.CreateBracket\(\s*\w+\s*,\s*(True|False)\)', line)
        if cb_match and cb_match.group(1) == "True":
            issues.append({
                "level": "error",
                "message": f"行{i}: CreateBracket の第2引数が True です（Falseにする必要あり）",
                "line": i,
                "auto_fix": "CreateBracket_True_to_False",
            })

        # Check 2: BlankElement with True on bracket
        blank_match = re.search(r'part\.BlankElement\(\s*(bracket\w*)\s*,\s*True\)', line)
        if blank_match:
            issues.append({
                "level": "error",
                "message": f"行{i}: BlankElement(bracket, True) はブラケットを非表示にします。削除してください",
                "line": i,
                "auto_fix": "remove_blank_true",
            })

        # Check 3: BaseElement should be profileN[0], not solid or sheet
        base_match = re.search(r'\.BaseElement\s*=\s*(\w+)', line)
        if base_match:
            base_val = base_match.group(1)
            if base_val.startswith("solid") or base_val.startswith("extrude_sheet"):
                issues.append({
                    "level": "error",
                    "message": f"行{i}: BaseElement に {base_val} が指定されています。profileN[0] を使用してください",
                    "line": i,
                    "auto_fix": None,
                })

        # Check 4: BracketType と Surfaces の整合性
        bt_match = re.search(r'\.BracketType\s*=\s*(\d+)', line)
        if bt_match:
            # このブラケットのSurfaces形式を後続行で確認するため、
            # bracket_type をメモしておく（簡易チェック）
            pass

        # Check 5: Surfaces の変数参照チェック
        surf_match = re.search(r'\.Surfaces[12]\s*=\s*\[(.+)\]', line)
        if surf_match:
            surf_content = surf_match.group(1)
            # solidN, extrude_sheetN, profileN[0] の参照を抽出
            var_refs = re.findall(r'(solid\d+|extrude_sheet\d+|profile\d+\[\d+\]|profile\d+)', surf_content)
            for var_ref in var_refs:
                if var_ref not in known_vars:
                    issues.append({
                        "level": "error",
                        "message": f"行{i}: Surfaces で参照されている変数 '{var_ref}' がスクリプト内に存在しません",
                        "line": i,
                        "auto_fix": None,
                    })

        # Check 6: Sf1EndElements/Sf2EndElements の変数参照チェック
        end_elem_match = re.search(r'\.Sf[12]EndElements\s*=\s*\[(.+)\]', line)
        if end_elem_match:
            elem_content = end_elem_match.group(1)
            var_refs = re.findall(r'(solid\d+|extrude_sheet\d+|profile\d+\[\d+\]|profile\d+)', elem_content)
            for var_ref in var_refs:
                if var_ref not in known_vars:
                    issues.append({
                        "level": "warning",
                        "message": f"行{i}: EndElements で参照されている変数 '{var_ref}' がスクリプト内に存在しません",
                        "line": i,
                        "auto_fix": None,
                    })

    # Check 7: ブラケット生成数と候補数の比較
    create_bracket_count = len(re.findall(r'part\.CreateBracket\(', bracket_code))
    if create_bracket_count == 0:
        issues.append({
            "level": "error",
            "message": "CreateBracket の呼び出しが見つかりません",
            "line": None,
            "auto_fix": None,
        })
    elif create_bracket_count == 1:
        expected = sum(
            1 for p in structure.get("profiles", [])
            if p.get("profile_type") in (1002, 1003, 1201, 1007)
            for k in ("end1_elements", "end2_elements") if p.get(k)
        )
        if expected > 5:
            issues.append({
                "level": "warning",
                "message": f"CreateBracket が1つだけですが、候補は{expected}件あります。全候補のブラケットを生成してください",
                "line": None,
                "auto_fix": None,
            })

    return issues


def auto_fix_bracket_section(bracket_code: str, issues: list) -> str:
    """
    自動修正可能な問題を修正する。
    """
    fixed = bracket_code

    for issue in issues:
        fix_type = issue.get("auto_fix")
        if fix_type == "CreateBracket_True_to_False":
            fixed = re.sub(
                r'(part\.CreateBracket\(\s*\w+\s*,\s*)True(\))',
                r'\1False\2',
                fixed,
            )
        elif fix_type == "remove_blank_true":
            # BlankElement(bracketXXX, True) の行を削除
            fixed = re.sub(
                r'^.*part\.BlankElement\(\s*bracket\w*\s*,\s*True\).*\n?',
                '',
                fixed,
                flags=re.MULTILINE,
            )

    return fixed


# ========== バッチ処理: グループ分けと仕様マージ ==========

def group_bracket_candidates(candidates: list, max_per_group: int = 8) -> list:
    """
    ブラケット候補を attach_surface 別にグループ化する。
    max_per_group を超えるグループは自動分割する。

    Returns:
        [
            {
                "group_id": int,
                "attach_surface": str,
                "attach_surface_name": str,
                "candidates": [candidate_dict, ...]
            },
            ...
        ]
    """
    from collections import OrderedDict

    groups_by_surface: "OrderedDict[str, list]" = OrderedDict()
    for c in candidates:
        key = c.get("attach_surface", "")
        if key not in groups_by_surface:
            groups_by_surface[key] = []
        groups_by_surface[key].append(c)

    result = []
    group_id = 1
    for surf, cands in groups_by_surface.items():
        surf_name = cands[0].get("attach_surface_name", "") if cands else ""
        if len(cands) <= max_per_group:
            result.append({
                "group_id": group_id,
                "attach_surface": surf,
                "attach_surface_name": surf_name,
                "candidates": cands,
            })
            group_id += 1
        else:
            for i in range(0, len(cands), max_per_group):
                chunk = cands[i:i + max_per_group]
                result.append({
                    "group_id": group_id,
                    "attach_surface": surf,
                    "attach_surface_name": surf_name,
                    "candidates": chunk,
                })
                group_id += 1

    return result


def merge_candidate_with_llm_params(candidate: dict, llm_params: dict) -> dict:
    """
    静的解析の候補データと LLM が決定したパラメータをマージして
    テンプレートエンジンに渡す完全なブラケット仕様 dict を生成する。

    candidate: detect_bracket_candidates() の出力要素
    llm_params: Agent 2 が JSON で出力した brackets[i] の要素
    """
    bracket_type = llm_params.get("bracket_type", candidate.get("bracket_type", 1505))

    spec: dict = {
        "candidate_id": candidate["id"],
        "bracket_name": llm_params["bracket_name"],
        "material_name": "SS400",
        "thickness": str(llm_params["thickness"]),
        "bracket_type": bracket_type,
        "bracket_params": llm_params.get("bracket_params", ["200"]),
        "mold": candidate.get("mold", "+"),
        "base_element": candidate["base_element"],
        "rev_sf1": llm_params.get("rev_sf1", False),
        "rev_sf2": llm_params.get("rev_sf2", False),
        "rev_sf3": llm_params.get("rev_sf3", False),
        "sf1_dimension_type": llm_params.get("sf1_dimension_type", 1541),
        "sf1_dimension_params": llm_params.get("sf1_dimension_params", ["0", "100"]),
        "sf2_dimension_type": llm_params.get("sf2_dimension_type", 1531),
        "sf2_dimension_params": llm_params.get("sf2_dimension_params", ["200", "15"]),
        "flange_type": llm_params.get("flange_type"),
        "color": ["0", "255", "255", "0.19999998807907104"],
    }

    if bracket_type == 1505:
        # Surfaces1: PLS 法線 + solid 参照
        spec["surfaces1_pls_normal"] = candidate.get("surfaces1_pls_normal", ["0", "0", "0"])
        spec["surfaces1_ref"] = (
            candidate.get("attach_surface_solid") or candidate.get("attach_surface", "")
        )
        # Surfaces2: profileN[0] の FL 面
        spec["surfaces2_ref"] = candidate["base_element"]
        # Sf1EndElements: PLS 法線 + end_element 参照
        spec["sf1_end_elements_normal"] = candidate.get("sf1_end_normal", ["0", "0", "0"])
        spec["sf1_end_elements_ref"] = candidate.get("sf1_end_element", "")
    else:
        # BracketType 1501: Profile FL × Profile FL
        # surfaces1_ref = base_element (自身の FL 面)
        spec["surfaces1_ref"] = candidate["base_element"]
        # surfaces2_ref = LLM が指定した第2プロファイル
        spec["surfaces2_ref"] = llm_params.get("surfaces2_ref", "")

    return spec
