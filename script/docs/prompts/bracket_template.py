"""
ブラケットコードテンプレートエンジン

LLM が出力した JSON 仕様から Python コードを決定論的に生成する。
構文エラーはゼロ保証。変数名の連番管理は呼び出し元 (start_index) が担う。

対応 BracketType:
  - 1505: Plate (PLS面) × Profile (FL面)
  - 1501: Profile (FL面) × Profile (FL面)
"""

from __future__ import annotations
from typing import List, Dict, Any, Tuple


def render_bracket_code(brackets: List[Dict[str, Any]], start_index: int = 1) -> str:
    """
    ブラケット仕様リストから Python コード文字列を生成する。

    Args:
        brackets: merge_candidate_with_llm_params() の出力リスト
        start_index: bracketPram の開始番号（グループ間の連番管理に使用）

    Returns:
        ブラケットセクションの Python コード文字列
    """
    blocks = []
    for i, spec in enumerate(brackets):
        n = start_index + i
        blocks.append(_render_single_bracket(n, spec))
    return "\n".join(blocks).rstrip()


def validate_bracket_json(json_data: Any) -> List[str]:
    """
    Agent 2 が出力した JSON 構造をスキーマ検証する。

    Returns:
        エラーメッセージのリスト（空リストは検証成功）
    """
    errors: List[str] = []

    if not isinstance(json_data, dict):
        return ["JSONデータが dict ではありません"]

    brackets = json_data.get("brackets")
    if not isinstance(brackets, list):
        return ['"brackets" キーがリストではありません']
    if len(brackets) == 0:
        return ['"brackets" リストが空です']

    required_fields = [
        "bracket_name",
        "thickness",
        "sf1_dimension_type",
        "sf1_dimension_params",
        "sf2_dimension_type",
        "sf2_dimension_params",
    ]

    for i, b in enumerate(brackets):
        if not isinstance(b, dict):
            errors.append(f"brackets[{i}] が dict ではありません")
            continue
        for field in required_fields:
            if field not in b:
                errors.append(f"brackets[{i}] に必須フィールド '{field}' がありません")

    return errors


# ========== プライベートヘルパー ==========

def _render_single_bracket(n: int, spec: Dict[str, Any]) -> str:
    """1 個分のブラケットコードブロックを生成する"""
    lines: List[str] = []
    bracket_type = spec.get("bracket_type", 1505)
    color = spec.get("color", ["0", "255", "255", "0.19999998807907104"])

    lines.append(f"bracketPram{n} = part.CreateBracketParam()")
    lines.append(f"bracketPram{n}.DefinitionType=1")
    lines.append(f'bracketPram{n}.BracketName="{spec["bracket_name"]}"')
    lines.append(f'bracketPram{n}.MaterialName="{spec.get("material_name", "SS400")}"')
    lines.append(f"bracketPram{n}.BaseElement={spec['base_element']}")
    lines.append(f"bracketPram{n}.UseSideSheetForPlane=False")
    lines.append(f'bracketPram{n}.Mold="{spec["mold"]}"')
    lines.append(f'bracketPram{n}.Thickness="{spec["thickness"]}"')
    lines.append(f"bracketPram{n}.BracketType={bracket_type}")

    if bracket_type == 1505:
        _render_1505(n, spec, lines)
    elif bracket_type == 1501:
        _render_1501(n, spec, lines)
    else:
        _render_1505(n, spec, lines)

    if spec.get("flange_type") is not None:
        lines.append(f"bracketPram{n}.FlangeType={spec['flange_type']}")

    lines.append(f"bracket{n} = part.CreateBracket(bracketPram{n},False)")
    color_args = ",".join(f'"{c}"' for c in color)
    lines.append(f"part.SetElementColor(bracket{n},{color_args})")
    lines.append("")

    return "\n".join(lines)


def _render_1505(n: int, spec: Dict[str, Any], lines: List[str]) -> None:
    bracket_params = spec.get("bracket_params", ["200"])
    lines.append(f"bracketPram{n}.BracketParams={_format_list(bracket_params)}")
    lines.append(f"bracketPram{n}.Scallop1Type=1801")
    lines.append(f'bracketPram{n}.Scallop1Params=["0"]')
    lines.append(f"bracketPram{n}.Scallop2Type=-1")

    n0, n1, n2 = _format_normals(spec.get("surfaces1_pls_normal", ["0", "0", "0"]))
    surfaces1_ref = spec.get("surfaces1_ref", "")
    lines.append(
        f'bracketPram{n}.Surfaces1=["PLS","False","False","{n0}","{n1}","{n2}",{surfaces1_ref}]'
    )
    lines.append(f"bracketPram{n}.RevSf1={_bool_str(spec.get('rev_sf1', False))}")

    surfaces2_ref = spec.get("surfaces2_ref", "")
    lines.append(f'bracketPram{n}.Surfaces2=[{surfaces2_ref}+",FL"]')
    lines.append(f"bracketPram{n}.RevSf2={_bool_str(spec.get('rev_sf2', False))}")
    lines.append(f"bracketPram{n}.RevSf3={_bool_str(spec.get('rev_sf3', False))}")

    lines.append(f"bracketPram{n}.Sf1DimensionType={spec.get('sf1_dimension_type', 1541)}")
    lines.append(
        f"bracketPram{n}.Sf1DimensonParams={_format_list(spec.get('sf1_dimension_params', ['0', '100']))}"
    )

    en0, en1, en2 = _format_normals(spec.get("sf1_end_elements_normal", ["0", "0", "0"]))
    sf1_end_ref = spec.get("sf1_end_elements_ref", "")
    lines.append(
        f'bracketPram{n}.Sf1EndElements=["PLS","False","False","{en0}","{en1}","{en2}",{sf1_end_ref}]'
    )

    lines.append(f"bracketPram{n}.Sf2DimensionType={spec.get('sf2_dimension_type', 1531)}")
    lines.append(
        f"bracketPram{n}.Sf2DimensonParams={_format_list(spec.get('sf2_dimension_params', ['200', '15']))}"
    )


def _render_1501(n: int, spec: Dict[str, Any], lines: List[str]) -> None:
    lines.append(f"bracketPram{n}.Scallop1Type=1801")
    lines.append(f'bracketPram{n}.Scallop1Params=["0"]')
    lines.append(f"bracketPram{n}.Scallop2Type=0")

    surfaces1_ref = spec.get("surfaces1_ref", "")
    lines.append(f'bracketPram{n}.Surfaces1=[{surfaces1_ref}+",FL"]')
    lines.append(f"bracketPram{n}.RevSf1={_bool_str(spec.get('rev_sf1', False))}")

    surfaces2_ref = spec.get("surfaces2_ref", "")
    lines.append(f'bracketPram{n}.Surfaces2=[{surfaces2_ref}+",FL"]')
    lines.append(f"bracketPram{n}.RevSf2={_bool_str(spec.get('rev_sf2', False))}")
    lines.append(f"bracketPram{n}.RevSf3={_bool_str(spec.get('rev_sf3', False))}")

    lines.append(f"bracketPram{n}.Sf1DimensionType={spec.get('sf1_dimension_type', 1531)}")
    lines.append(
        f"bracketPram{n}.Sf1DimensonParams={_format_list(spec.get('sf1_dimension_params', ['200', '15']))}"
    )

    lines.append(f"bracketPram{n}.Sf2DimensionType={spec.get('sf2_dimension_type', 1531)}")
    lines.append(
        f"bracketPram{n}.Sf2DimensonParams={_format_list(spec.get('sf2_dimension_params', ['200', '15']))}"
    )


def _format_list(params: list) -> str:
    quoted = [f'"{p}"' for p in params]
    return "[" + ",".join(quoted) + "]"


def _format_normals(normals: list) -> Tuple[str, str, str]:
    if len(normals) >= 3:
        return str(normals[0]), str(normals[1]), str(normals[2])
    return "0", "0", "0"


def _bool_str(val: bool) -> str:
    return "True" if val else "False"
