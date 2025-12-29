from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Union

# --- ▼▼▼ インポート修正 ▼▼▼ ---
# import os # config.py を使うため os.environ は不要
import time
import functools
# from dotenv import load_dotenv # config.py を使うため dotenv は不要
import config # ★ config.py をインポート
try:
    import openai
except ImportError:
    print("OpenAIライブラリが必要です。 'pip install openai' を実行してください。", file=sys.stderr)
    sys.exit(1)
# --- ▲▲▲ インポート修正 ▲▲▲ ---


# .envファイルから環境変数を読み込む
# load_dotenv() # config.py を使うため不要


# --- ▼▼▼ 修正 (OpenAI クライアントのセットアップ) ▼▼▼ ---
# config.py からキーを読み込む
OPENAI_API_KEY = getattr(config, "OPENAI_API_KEY", None)

if not OPENAI_API_KEY:
    print("警告: config.py に OPENAI_API_KEY が設定されていません。LLMによる文脈一致評価はスキップされます。", file=sys.stderr)
    OPENAI_CLIENT = None
else:
    # APIキーを明示的に渡してクライアントを初期化
    OPENAI_CLIENT = openai.OpenAI(api_key=OPENAI_API_KEY)

LLM_SYSTEM_PROMPT = """あなたは、APIドキュメントの記述を比較する専門家です。
以下の2つの説明文が、文脈的に同じ意味を表しているかどうかを判定してください。

完全に同じである必要はありませんが、エンジニアが読んだときに同じ機能や制約、意味を持つと解釈できる場合は「はい」と答えてください。
意味が異なる場合や、一方が情報を含んでいるがもう一方が全く含んでいない場合は「いいえ」と答えてください。

回答は「はい」または「いいえ」のいずれか一言のみでお願いします。
"""

LLM_RATE_LIMIT_DELAY = 1  # API呼び出し間の待機時間（秒）

@functools.lru_cache(maxsize=None)
def llm_check_contextual_match(desc1: str, desc2: str) -> bool:
    """LLMを使用して2つのdescriptionの文脈一致を評価する"""
    if not OPENAI_CLIENT:
        return False # APIキーがない場合は常に False

    # 正規化してから比較（キャッシュ効率化のため）
    norm_desc1 = normalize_whitespace(desc1) or ""
    norm_desc2 = normalize_whitespace(desc2) or ""

    if not norm_desc1 or not norm_desc2:
        return False # どちらかが空なら不一致

    if norm_desc1 == norm_desc2:
        return True # 完全に一致する場合はAPIを呼ばない

    user_prompt = f"説明1: {norm_desc1}\n説明2: {norm_desc2}"

    try:
        time.sleep(LLM_RATE_LIMIT_DELAY) # レートリミット対策
        
        completion = OPENAI_CLIENT.chat.completions.create(
            model="gpt-4o-mini", # コストと速度に応じて "gpt-3.5-turbo" などに変更可能
            messages=[
                {"role": "system", "content": LLM_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0,
            max_tokens=5,
        )
        
        response_text = completion.choices[0].message.content or ""
        
        # 応答が "はい" を含んでいれば True
        if "はい" in response_text:
            return True
        else:
            return False
            
    except Exception as e:
        print(f"LLM呼び出しエラー (比較中: '{norm_desc1[:20]}...' vs '{norm_desc2[:20]}...'): {e}", file=sys.stderr)
        return False # エラー時は False (不一致) として扱う
# --- ▲▲▲ 修正 (OpenAI クライアントのセットアップ) ▲▲▲ ---


# --- XML用データクラス ---
@dataclass
class XmlParameter:
    key: str
    name: str
    type_name: str
    description: str

@dataclass
class XmlEntry:
    entry_type: str
    name: str
    category: Optional[str]
    title_jp: Optional[str]
    raw_return: Optional[str]
    return_description: Optional[str]
    params: List[XmlParameter]
    object_name: Optional[str]


# --- JSON用データクラス (既存) ---
@dataclass
class JsonParameter:
    key: str
    name: str
    type_name: str
    description: str
    order: int

@dataclass
class JsonEntry:
    entry_type: str
    name: str
    category: Optional[str] = None
    title_jp: Optional[str] = None
    raw_return: Optional[str] = None
    return_description: Optional[str] = None
    params: List[JsonParameter] = field(default_factory=list)
    object_name: Optional[str] = None


ENTRY_TYPE_MAP: Dict[str, str] = {
    "method": "function",
    "parameterObject": "parameter_object",
}


def sanitize_template_xml(text: str) -> str:
    """Fixes known formatting issues in api_template.xml before parsing."""
    def fix_block(tag: str, source: str) -> str:
        pattern = re.compile(rf"<{tag}>(?P<body>[\s\S]*?)<{tag}\s*/>")
        while True:
            match = pattern.search(source)
            if not match:
                break
            body = match.group("body")
            replacement = f"<{tag}>{body}</{tag}>"
            source = source[: match.start()] + replacement + source[match.end() :]
        return source

    text = fix_block("parameters", text)
    text = fix_block("attributes", text)
    text = re.sub(r"<parameters>\s*<parameters\s*/>", "<parameters/>", text)
    text = re.sub(r"<parameters>\s*</parameters>", "<parameters/>", text)
    text = re.sub(r"<attributes>\s*<attributes\s*/>", "<attributes/>", text)
    text = re.sub(r"<attributes>\s*</attributes>", "<attributes/>", text)
    return text


def normalize_whitespace(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = value.replace("\u3000", " ")
    normalized = re.sub(r"\s+", " ", normalized.strip())
    return normalized or None


def normalize_category(section: Optional[str]) -> Optional[str]:
    section = normalize_whitespace(section)
    if not section:
        return None
    suffixes = ["のメソッド", "のプロパティ", "のイベント", "の属性", "のパラメータ"]
    for suffix in suffixes:
        if section.endswith(suffix):
            section = section[: -len(suffix)]
            break
    return section or None


def extract_return_fields(text: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    text = normalize_whitespace(text)
    if not text:
        return None, None
    cleaned = re.sub(r"^返り値[:：]\s*", "", text)
    return cleaned or None, cleaned or None


def split_type_and_description(text: Optional[str]) -> Tuple[str, str]:
    normalized = normalize_whitespace(text) or ""
    if not normalized:
        return "", ""
    parts = re.split(r"[:：]", normalized, maxsplit=1)
    if len(parts) == 1:
        return parts[0].strip(), ""
    type_name, description = parts[0].strip(), parts[1].strip()
    return type_name, description


def build_parameter_key(name: str, index: int) -> str:
    name = name.strip()
    return name or f"__index_{index}"


# --- ▼▼▼ 修正箇所 1 (既存の修正) ▼▼▼ ---
def parse_xml_template(path: Path) -> Dict[str, XmlEntry]:
    """
    api_template.xmlを解析し、検証可能な形式に再構成する。
    """
    raw = path.read_text(encoding="utf-8")
    sanitized = sanitize_template_xml(raw)
    try:
        root = ET.fromstring(sanitized)
    except ET.ParseError as exc:
        raise ValueError(f"XMLの解析に失敗しました: {exc}") from exc

    entries: Dict[str, XmlEntry] = {}
    for element in root:
        entry_type_raw = element.tag
        entry_type = ENTRY_TYPE_MAP.get(entry_type_raw, entry_type_raw)
        name_attr = element.get("name") # XMLのname属性 (e.g., LinearSweepParam)
        if not name_attr:
            continue
        
        category = normalize_category(element.get("section"))
        object_name = category

        # title, return, params を先に読み込む
        title_jp_val, raw_return_val, return_desc_val = None, None, None
        params_list: List[XmlParameter] = []

        for child in element:
            if child.tag == "title":
                title_jp_val = normalize_whitespace(child.text)
            elif child.tag == "return":
                raw_return_val, return_desc_val = extract_return_fields(child.text)
            elif child.tag in {"parameters", "attributes"}:
                for param in child:
                    if param.tag != "parameter":
                        continue
                    param_name = normalize_whitespace(param.get("name") or "") or ""
                    type_name, description = split_type_and_description(param.text)
                    key = build_parameter_key(param_name, len(params_list))
                    params_list.append(
                        XmlParameter(key=key, name=param_name, type_name=type_name, description=description)
                    )

        # (★修正★) parameterObjectの場合、キーをname属性からtitleに変更
        entry_key = name_attr
        entry_name = name_attr # デフォルトはname属性
        if entry_type == "parameter_object" and title_jp_val:
            entry_key = title_jp_val  # 辞書のキー
            entry_name = title_jp_val # エントリ自体の名前
        
        entries[entry_key] = XmlEntry(
            entry_type=entry_type, name=entry_name, category=category, title_jp=title_jp_val,
            raw_return=raw_return_val, return_description=return_desc_val,
            params=params_list, object_name=object_name,
        )
    return entries
# --- ▲▲▲ 修正箇所 1 (既存の修正) ▲▲▲ ---


# --- ▼▼▼ 修正箇所 2 (既存の修正) ▼▼▼ ---
def parse_neo4j_json(path: Path) -> Dict[str, JsonEntry]:
    """
    neo4j_data.jsonのグラフ構造を解析し、検証可能な形式に再構成する。
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    nodes = {node['id']: node for node in data.get('nodes', [])}
    
    # 探索を効率化するため、リレーションシップをソースIDで索引付け
    source_to_rels: Dict[str, List[Dict]] = {}
    for rel in data.get('relationships', []):
        source_id = rel.get('source')
        if source_id:
            source_to_rels.setdefault(source_id, []).append(rel)

    json_entries: Dict[str, JsonEntry] = {}
    
    # --- 1. Methodノードの解析 (既存のコード) ---
    method_nodes = [n for n in nodes.values() if n.get('type') == 'Method']

    for method_node in method_nodes:
        method_props = method_node.get('properties', {})
        method_name = method_props.get('name')
        if not method_name or not method_props:
            continue

        entry = JsonEntry(
            name=method_name,
            entry_type='function',
            title_jp=method_props.get('description')
        )

        method_rels = source_to_rels.get(method_node['id'], [])
        for rel in method_rels:
            target_id = rel.get('target')
            target_node = nodes.get(target_id)
            if not target_node:
                continue
            
            rel_type = rel.get('type')
            target_props = target_node.get('properties', {})

            if rel_type == 'BELONGS_TO':
                entry.object_name = target_props.get('name')
                entry.category = entry.object_name
            
            elif rel_type == 'HAS_RETURNS':
                entry.return_description = normalize_whitespace(target_props.get('description'))
                entry.raw_return = entry.return_description

            elif rel_type == 'HAS_PARAMETER':
                param_name = target_props.get('name', '')
                param_desc = target_props.get('description', '')
                param_order = target_props.get('order', 999)
                param_type = "不明"

                param_rels = source_to_rels.get(target_id, [])
                for param_rel in param_rels:
                    if param_rel.get('type') == 'HAS_TYPE':
                        type_node = nodes.get(param_rel.get('target'))
                        if type_node:
                            param_type = type_node.get('properties', {}).get('name', "不明")
                        break
                
                entry.params.append(JsonParameter(
                    key=build_parameter_key(param_name, len(entry.params)),
                    name=param_name, type_name=param_type,
                    description=param_desc, order=param_order,
                ))

        entry.params.sort(key=lambda p: p.order)
        json_entries[method_name] = entry
        
    # --- 2. ParameterObject (DataType) ノードの解析 (★新規追加★) ---
    datatype_nodes = [n for n in nodes.values() if n.get('type') == 'DataType']
    for dt_node in datatype_nodes:
        dt_id = dt_node['id']
        dt_props = dt_node.get('properties', {})
        dt_name = dt_props.get('name')
        if not dt_name:
            continue

        # このDataTypeノードから出ている HAS_ATTRIBUTE リレーションを探す
        attributes_rels = [
            rel for rel in source_to_rels.get(dt_id, []) 
            if rel.get('type') == 'HAS_ATTRIBUTE'
        ]

        # HAS_ATTRIBUTE リレーションがなければパラメータオブジェクトではない
        if not attributes_rels:
            continue
        
        # パラメータオブジェクト用の JsonEntry を作成
        entry = JsonEntry(
            name=dt_name,
            entry_type='parameter_object',
            title_jp=dt_name, # XMLのtitleとJSONのnameが一致すると仮定
            params=[]
        )
        
        # 属性 (Attribute) をパースして params に追加
        for attr_rel in attributes_rels:
            attr_id = attr_rel.get('target')
            attr_node = nodes.get(attr_id)
            if not attr_node or attr_node.get('type') != 'Attribute':
                continue
                
            attr_props = attr_node.get('properties', {})
            attr_name = attr_props.get('name', '')
            attr_desc = attr_props.get('description', '')
            attr_type = "不明"

            # 属性の型 (HAS_TYPE) を探す
            attr_type_rels = source_to_rels.get(attr_id, [])
            for type_rel in attr_type_rels:
                if type_rel.get('type') == 'HAS_TYPE':
                    type_node = nodes.get(type_rel.get('target'))
                    if type_node:
                        attr_type = type_node.get('properties', {}).get('name', "不明")
                    break
            
            entry.params.append(JsonParameter(
                key=build_parameter_key(attr_name, len(entry.params)),
                name=attr_name, type_name=attr_type,
                description=attr_desc, order=999, # order はJSON側にないため固定値
            ))
        
        json_entries[dt_name] = entry

    return json_entries
# --- ▲▲▲ 修正箇所 2 (既存の修正) ▲▲▲ ---


@dataclass
class Difference:
    name: str
    entry_type: str
    field: str
    expected: object
    actual: object


# --- ▼▼▼ 修正 (AccuracyMetrics の ⑺ コメント修正) ▼▼▼ ---
@dataclass
class AccuracyMetrics:
    """正答率計算用のメトリクス"""
    # ⑴関数名の正答率
    function_names_total: int
    function_names_correct: int
    function_names_accuracy: float

    # ⑵パラメータオブジェクトの正答率
    parameter_objects_total: int
    parameter_objects_correct: int
    parameter_objects_accuracy: float

    # ⑶型定義の正答率
    type_definitions_total: int
    type_definitions_correct: int
    type_definitions_accuracy: float

    # ⑷引数定義名の正答率
    parameter_names_total: int
    parameter_names_correct: int
    parameter_names_accuracy: float

    # ⑸引数タイプの正答率
    parameter_types_total: int
    parameter_types_correct: int
    parameter_types_accuracy: float

    # ⑹descriptionの正答率（完全一致）
    descriptions_total: int
    descriptions_correct: int
    descriptions_accuracy: float

    # ⑺descriptionの正答率（文脈一致）
    contextual_descriptions_total: int
    contextual_descriptions_correct: int
    contextual_descriptions_accuracy: float


def calculate_denominators(
    xml_entries: Dict[str, XmlEntry]
) -> Tuple[int, int, int, int, int, int, int]: # 戻り値を7つに変更
    """
    各評価指標の分母を計算する (XMLを正解とする)

    Returns:
        Tuple[int, int, int, int, int, int, int]: (関数名総数, ..., description総数(完全), description総数(文脈))
    """
    # ⑴関数名の総数（XMLのmethod総数）
    function_names_total = sum(1 for entry in xml_entries.values() if entry.entry_type == "function")

    # ⑵パラメータオブジェクトの総数（XMLのparameterObject総数）
    parameter_objects_total = sum(1 for entry in xml_entries.values() if entry.entry_type == "parameter_object")

    # ⑶型定義の総数（XMLのtypeDefinition総数）- test1021.pyでは対象外
    type_definitions_total = sum(1 for entry in xml_entries.values() if entry.entry_type == "type_definition")

    # ⑷引数定義名の総数（XMLの全パラメータ名数）
    parameter_names_total = sum(len(entry.params) for entry in xml_entries.values())

    # ⑸引数タイプの総数（XMLの全パラメータタイプ数）
    parameter_types_total = sum(len(entry.params) for entry in xml_entries.values())

    # ⑹descriptionの総数（完全一致）
    descriptions_total = 0
    # ⑺ description (文脈一致) の総数 (★修正: params と return を対象)
    contextual_descriptions_total = 0

    for entry in xml_entries.values():
        # パラメータのdescription
        for param in entry.params:
            if param.description:
                descriptions_total += 1 # (6) 完全一致の対象
                contextual_descriptions_total += 1 # (7) 文脈一致の対象
        
        # 戻り値のdescription
        if entry.return_description:
            descriptions_total += 1 # (6) 完全一致の対象
            contextual_descriptions_total += 1 # (7) 文脈一致の対象 (★追加)
        
        # 型定義のdescription
        if entry.entry_type == "type_definition" and entry.title_jp:
            descriptions_total += 1 # (6) 完全一致の対象
            # (7) は対象外 (JSONパーサーが未対応のため)

    return (function_names_total, parameter_objects_total, type_definitions_total, 
            parameter_names_total, parameter_types_total, descriptions_total,
            contextual_descriptions_total) # 戻り値を7つに変更

def calculate_numerators(
    xml_entries: Dict[str, XmlEntry], json_entries: Dict[str, JsonEntry]
) -> Tuple[int, int, int, int, int, int, int]: # 戻り値を7つに変更
    """
    各評価指標の分子（正解数）を計算する (JSONの値を評価)

    Returns:
        Tuple[int, int, int, int, int, int, int]: (関数名正解数, ..., description正解数(完全), description正解数(文脈))
    """
    # ⑴関数名の正解数（JSONで正しく抽出された関数数）
    function_names_correct = sum(
        1 for entry in json_entries.values() 
        if entry.entry_type == "function"
    )

    # ⑵パラメータオブジェクトの正解数（JSONで正しく抽出されたパラメータオブジェクト数）
    parameter_objects_correct = sum(
        1 for entry in json_entries.values() 
        if entry.entry_type == "parameter_object"
    )

    # ⑶型定義の正解数（JSONで正しく抽出された型定義数）
    type_definitions_correct = sum(
        1 for entry in json_entries.values() 
        if entry.entry_type == "type_definition"
    )

    # ⑷引数定義名の正解数（XMLとJSONで同じパラメータの名前が一致しているものの数）
    parameter_names_correct = 0
    parameter_types_correct = 0
    descriptions_correct = 0 # (6) 完全一致
    contextual_descriptions_correct = 0 # (7) 文脈一致

    print("LLMによる文脈一致評価を開始します... (config.py の OPENAI_API_KEY が必要です)", file=sys.stderr)
    llm_call_count = 0

    for name in xml_entries.keys():
        if name in json_entries:
            xml_entry = xml_entries[name]
            json_entry = json_entries[name]
            
            # パラメータのマッピングを作成
            xml_params = {param.key: param for param in xml_entry.params}
            json_params = {param.key: param for param in json_entry.params}
            
            # 共通のパラメータで名前、タイプ、Descriptionが一致するものをカウント
            common_params = set(xml_params.keys()) & set(json_params.keys())
            for key in common_params:
                xml_param = xml_params[key]
                json_param = json_params[key]
                
                # (4) 名前
                if xml_param.name == json_param.name:
                    parameter_names_correct += 1

                # (5) タイプ
                if xml_param.type_name == json_param.type_name:
                    parameter_types_correct += 1
                
                xml_desc = xml_param.description
                json_desc = json_param.description

                # (6) パラメータDescription (完全一致)
                if (xml_desc and 
                    json_desc and
                    normalize_whitespace(xml_desc) == normalize_whitespace(json_desc)):
                    descriptions_correct += 1
                
                # (7) パラメータDescription (文脈一致)
                if (xml_desc and json_desc):
                    llm_call_count += 1
                    if llm_call_count % 10 == 0:
                        print(f"  ...LLM評価 {llm_call_count} 件目 (param)", file=sys.stderr)

                    # LLMで評価
                    if llm_check_contextual_match(xml_desc, json_desc):
                        contextual_descriptions_correct += 1
            
            # (6) 戻り値のdescription (完全一致)
            if (xml_entry.return_description and 
                json_entry.return_description and
                normalize_whitespace(xml_entry.return_description) == normalize_whitespace(json_entry.return_description)):
                descriptions_correct += 1
            
            # (7) 戻り値のdescription (文脈一致) (★追加★)
            if (xml_entry.return_description and json_entry.return_description):
                llm_call_count += 1
                if llm_call_count % 10 == 0:
                    print(f"  ...LLM評価 {llm_call_count} 件目 (return)", file=sys.stderr)
                
                if llm_check_contextual_match(xml_entry.return_description, json_entry.return_description):
                    contextual_descriptions_correct += 1

    if llm_call_count > 0:
        print(f"LLMによる文脈一致評価が完了しました。 (合計 {llm_call_count} ペアを評価)", file=sys.stderr)
    elif OPENAI_CLIENT:
        print("LLM評価対象のdescription (XMLとJSON双方に存在する) がありませんでした。", file=sys.stderr)

    return (function_names_correct, parameter_objects_correct, type_definitions_correct, 
            parameter_names_correct, parameter_types_correct, descriptions_correct,
            contextual_descriptions_correct) # 戻り値を7つに変更
# --- ▲▲▲ 修正 (calculate_numerators で ⑺ の分子に return を追加) ▲▲▲ ---


# --- ▼▼▼ 修正 (calculate_accuracy_metrics で ⑺ のコメント修正) ▼▼▼ ---
def calculate_accuracy_metrics(
    xml_entries: Dict[str, XmlEntry], json_entries: Dict[str, JsonEntry]
) -> AccuracyMetrics:
    """
    正答率メトリクスを計算する

    Returns:
        AccuracyMetrics: 各評価指標の総数、正解数、正答率
    """
    # 分母を計算 (7つの値を受け取る)
    (function_names_total, parameter_objects_total, type_definitions_total, parameter_names_total, 
     parameter_types_total, descriptions_total, 
     contextual_descriptions_total) = calculate_denominators(xml_entries)

    # 分子を計算 (7つの値を受け取る)
    (function_names_correct, parameter_objects_correct, type_definitions_correct, parameter_names_correct,
     parameter_types_correct, descriptions_correct,
     contextual_descriptions_correct) = calculate_numerators(xml_entries, json_entries)

    # 正答率を計算（ゼロ除算を避ける）
    function_names_accuracy = (function_names_correct / function_names_total
                               if function_names_total > 0 else 0.0)
    parameter_objects_accuracy = (parameter_objects_correct / parameter_objects_total
                                  if parameter_objects_total > 0 else 0.0)
    type_definitions_accuracy = (type_definitions_correct / type_definitions_total
                                 if type_definitions_total > 0 else 0.0)
    parameter_names_accuracy = (parameter_names_correct / parameter_names_total
                                if parameter_names_total > 0 else 0.0)
    parameter_types_accuracy = (parameter_types_correct / parameter_types_total
                                if parameter_types_total > 0 else 0.0)
    descriptions_accuracy = (descriptions_correct / descriptions_total
                             if descriptions_total > 0 else 0.0)
    
    # (7) 文脈一致の正答率を計算
    contextual_descriptions_accuracy = (contextual_descriptions_correct / contextual_descriptions_total
                                        if contextual_descriptions_total > 0 else 0.0)

    return AccuracyMetrics(
        function_names_total=function_names_total,
        function_names_correct=function_names_correct,
        function_names_accuracy=function_names_accuracy,
        parameter_objects_total=parameter_objects_total,
        parameter_objects_correct=parameter_objects_correct,
        parameter_objects_accuracy=parameter_objects_accuracy,
        type_definitions_total=type_definitions_total,
        type_definitions_correct=type_definitions_correct,
        type_definitions_accuracy=type_definitions_accuracy,
        parameter_names_total=parameter_names_total,
        parameter_names_correct=parameter_names_correct,
        parameter_names_accuracy=parameter_names_accuracy,
        parameter_types_total=parameter_types_total,
        parameter_types_correct=parameter_types_correct,
        parameter_types_accuracy=parameter_types_accuracy,
        descriptions_total=descriptions_total,
        descriptions_correct=descriptions_correct,
        descriptions_accuracy=descriptions_accuracy,
        # (7) を追加
        contextual_descriptions_total=contextual_descriptions_total,
        contextual_descriptions_correct=contextual_descriptions_correct,
        contextual_descriptions_accuracy=contextual_descriptions_accuracy,
    )
# --- ▲▲▲ 修正 (calculate_accuracy_metrics で ⑺ のコメント修正) ▲▲▲ ---


def compare_entries(xml_entry: XmlEntry, json_entry: JsonEntry) -> List[Difference]:
    differences: List[Difference] = []

    def record(field: str, expected: object, actual: object) -> None:
        # ホワイトスペースを正規化して比較
        norm_expected = normalize_whitespace(str(expected)) if isinstance(expected, str) else expected
        norm_actual = normalize_whitespace(str(actual)) if isinstance(actual, str) else actual
        
        # None と "" を同一視する (JSON側がNone、XML側が""になるケースを許容)
        if (norm_expected is None or norm_expected == "") and (norm_actual is None or norm_actual == ""):
             pass # 差分なしとみなす
        elif norm_expected != norm_actual:
            differences.append(
                Difference(name=xml_entry.name, entry_type=xml_entry.entry_type, field=field, expected=expected, actual=actual)
            )

    record("title_jp", xml_entry.title_jp, json_entry.title_jp)
    
    # ParameterObject の場合、return と object_name は比較しない (JSON側に情報がないため)
    if xml_entry.entry_type == 'function':
        record("return_description", xml_entry.return_description, json_entry.return_description)
        record("object_name", xml_entry.object_name, json_entry.object_name)

    xml_params: Dict[str, Union[XmlParameter, JsonParameter]] = {p.key: p for p in xml_entry.params}
    json_params: Dict[str, Union[XmlParameter, JsonParameter]] = {p.key: p for p in json_entry.params}

    for key in sorted(set(xml_params) - set(json_params)):
        param = xml_params[key]
        differences.append(
            Difference(name=xml_entry.name, entry_type=xml_entry.entry_type, field=f"params[{param.name or key}]",
                       expected={"type": param.type_name, "description": param.description}, actual="(JSONに無し)")
        )
    for key in sorted(set(json_params) - set(xml_params)):
        param = json_params[key]
        differences.append(
            Difference(name=xml_entry.name, entry_type=xml_entry.entry_type, field=f"params[{param.name or key}]",
                       expected="(XMLに無し)", actual={"type": param.type_name, "description": param.description})
        )
    for key in sorted(set(xml_params) & set(json_params)):
        xml_param = xml_params[key]
        json_param = json_params[key]
        record(f"params[{xml_param.name or key}].type", xml_param.type_name, json_param.type_name)
        record(f"params[{xml_param.name or key}].description", xml_param.description, json_param.description)

    return differences


def compare_collections(
    xml_entries: Dict[str, XmlEntry], json_entries: Dict[str, JsonEntry]
) -> Tuple[List[str], List[str], List[Difference]]:
    xml_keys = set(xml_entries.keys())
    json_keys = set(json_entries.keys())
    
    xml_only = sorted(xml_keys - json_keys)
    json_only = sorted(json_keys - xml_keys)

    diffs: List[Difference] = []
    for name in sorted(xml_keys & json_keys):
        # XMLとJSONでエントリタイプが異なる場合は差分として記録
        if xml_entries[name].entry_type != json_entries[name].entry_type:
            diffs.append(Difference(
                name=name, entry_type=xml_entries[name].entry_type, field="entry_type",
                expected=xml_entries[name].entry_type, actual=json_entries[name].entry_type
            ))
            continue
            
        diffs.extend(compare_entries(xml_entries[name], json_entries[name]))

    return xml_only, json_only, diffs


def format_differences(
    xml_only: Iterable[str], json_only: Iterable[str], diffs: Iterable[Difference], limit: Optional[int] = 20
) -> str:
    lines: List[str] = []
    xml_only_list, json_only_list, diff_list = list(xml_only), list(json_only), list(diffs)

    def trim(items: List) -> Tuple[List, bool]:
        if limit is None or len(items) <= limit:
            return items, False
        return items[:limit], True

    if xml_only_list:
        subset, more = trim(xml_only_list)
        lines.append(f"[XMLのみ] {', '.join(subset)}")
        if more: lines.append(f"  ...他 {len(xml_only_list) - len(subset)} 件")
    if json_only_list:
        subset, more = trim(json_only_list)
        lines.append(f"[JSONのみ] {', '.join(subset)}")
        if more: lines.append(f"  ...他 {len(json_only_list) - len(subset)} 件")
    if diff_list:
        lines.append("[差分あり]")
        subset, more = trim(diff_list)
        for diff in subset:
            expected = f'"{diff.expected}"' if diff.expected is not None else "(None/空)"
            actual = f'"{diff.actual}"' if diff.actual is not None else "(None/空)"
            lines.append(f"- {diff.name} | {diff.field:<30} | 期待値: {expected:<40} | 実際値: {actual}")
        if more: lines.append(f"  ...他 {len(diff_list) - len(subset)} 件の差分")

    return "\n".join(lines) if lines else "差分は検出されませんでした。"


# --- ▼▼▼ 修正 (write_report_document で ⑺ のコメント修正) ▼▼▼ ---
def write_report_document(
    report_path: Path, xml_path: Path, json_path: Path, xml_only: List[str],
    json_only: List[str], diffs: List[Difference], report_text: str, exit_code: int,
    accuracy_metrics: Optional[AccuracyMetrics] = None
) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    outcome = "差分なし (exit 0)" if exit_code == 0 else "差分あり (exit 1)"
    
    # カウントを正確にする
    xml_keys = set([d.name for d in diffs]) | set(xml_only)
    json_keys = set([d.name for d in diffs]) | set(json_only)
    common_keys = xml_keys & json_keys
    xml_count = len(xml_only) + len(common_keys)
    json_count = len(json_only) + len(common_keys)


    summary_lines = [
        f"# structured_api 検証ログ ({timestamp})", "",
        f"- XML: `{xml_path.name}`",
        f"- JSON: `{json_path.name}`",
        f"- 結果: {outcome}",
        f"- XMLエントリ数 (比較対象): {xml_count}",
        f"- JSONエントリ数 (比較対象): {json_count}",
        f"- XMLのみ: {len(xml_only)}件 / JSONのみ: {len(json_only)}件 / 共通キーの差分: {len(diffs)}件",
    ]

    # --- ▼▼▼ (AccuracyMetricsのレポート) ⑺ コメント修正 ▼▼▼ ---
    if accuracy_metrics:
        summary_lines.extend([
            "", "## 正答率メトリクス",
            "",
            "### ⑴関数名の正答率",
            f"- 総数: {accuracy_metrics.function_names_total}",
            f"- 正解数: {accuracy_metrics.function_names_correct}",
            f"- 正答率: {accuracy_metrics.function_names_accuracy:.2%}",
            "",
            "### ⑵パラメータオブジェクトの正答率",
            f"- 総数: {accuracy_metrics.parameter_objects_total}",
            f"- 正解数: {accuracy_metrics.parameter_objects_correct}",
            f"- 正答率: {accuracy_metrics.parameter_objects_accuracy:.2%}",
            "",
            "### ⑶型定義の正答率",
            f"- 総数: {accuracy_metrics.type_definitions_total}",
            f"- 正解数: {accuracy_metrics.type_definitions_correct}",
            f"- 正答率: {accuracy_metrics.type_definitions_accuracy:.2%}",
            "",
            "### ⑷引数定義名の正答率",
            f"- 総数: {accuracy_metrics.parameter_names_total}",
            f"- 正解数: {accuracy_metrics.parameter_names_correct}",
            f"- 正答率: {accuracy_metrics.parameter_names_accuracy:.2%}",
            "",
            "### ⑸引数タイプの正答率",
            f"- 総数: {accuracy_metrics.parameter_types_total}",
            f"- 正解数: {accuracy_metrics.parameter_types_correct}",
            f"- 正答率: {accuracy_metrics.parameter_types_accuracy:.2%}",
            "",
            "### ⑹descriptionの正答率（完全一致）",
            f"- 総数: {accuracy_metrics.descriptions_total}",
            f"- 正解数: {accuracy_metrics.descriptions_correct}",
            f"- 正答率: {accuracy_metrics.descriptions_accuracy:.2%}",
            "",
            "### ⑺descriptionの正答率（文脈一致）",
            f"- 総数: {accuracy_metrics.contextual_descriptions_total}",
            f"- 正解数: {accuracy_metrics.contextual_descriptions_correct}",
            f"- 正答率: {accuracy_metrics.contextual_descriptions_accuracy:.2%}",
        ])
    # --- ▲▲▲ (AccuracyMetricsのレポート) ⑺ コメント修正 ▲▲▲ ---

    summary_lines.extend([
        "", "## レポート", "```", report_text, "```",
    ])
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
# --- ▲▲▲ 修正 (write_report_document で ⑺ のコメント修正) ▲▲▲ ---


# --- ▼▼▼ 修正 (run_validation で ⑺ のコメント修正) ▼▼▼ ---
def run_validation(xml_path: Path, json_path: Path, report_path: Path) -> int:
    try:
        xml_entries = parse_xml_template(xml_path)
        json_entries = parse_neo4j_json(json_path)
    except (ValueError, FileNotFoundError, json.JSONDecodeError) as e:
        print(f"エラー: ファイルの読み込みまたは解析に失敗しました。\n{e}", file=sys.stderr)
        return 2

    xml_only, json_only, diffs = compare_collections(xml_entries, json_entries)
    report = format_differences(xml_only, json_only, diffs)
    print(report)

    # --- ▼▼▼ (AccuracyMetricsの計算と表示) ⑺ コメント修正 ▼▼▼ ---
    accuracy_metrics = calculate_accuracy_metrics(xml_entries, json_entries)
    print("\n=== 正答率メトリクス ===")
    print(f"⑴関数名の正答率: {accuracy_metrics.function_names_correct}/{accuracy_metrics.function_names_total} ({accuracy_metrics.function_names_accuracy:.2%})")
    print(f"⑵パラメータオブジェクトの正答率: {accuracy_metrics.parameter_objects_correct}/{accuracy_metrics.parameter_objects_total} ({accuracy_metrics.parameter_objects_accuracy:.2%})")
    print(f"⑶型定義の正答率: {accuracy_metrics.type_definitions_correct}/{accuracy_metrics.type_definitions_total} ({accuracy_metrics.type_definitions_accuracy:.2%})")
    print(f"⑷引数定義名の正答率: {accuracy_metrics.parameter_names_correct}/{accuracy_metrics.parameter_names_total} ({accuracy_metrics.parameter_names_accuracy:.2%})")
    print(f"⑸引数タイプの正答率: {accuracy_metrics.parameter_types_correct}/{accuracy_metrics.parameter_types_total} ({accuracy_metrics.parameter_types_accuracy:.2%})")
    print(f"⑹descriptionの正答率（完全一致）: {accuracy_metrics.descriptions_correct}/{accuracy_metrics.descriptions_total} ({accuracy_metrics.descriptions_accuracy:.2%})")
    print(f"⑺descriptionの正答率（文脈一致）: {accuracy_metrics.contextual_descriptions_correct}/{accuracy_metrics.contextual_descriptions_total} ({accuracy_metrics.contextual_descriptions_accuracy:.2%})")
    # --- ▲▲▲ (AccuracyMetricsの計算と表示) ⑺ コメント修正 ▲▲▲ ---

    full_report = format_differences(xml_only, json_only, diffs, limit=None)
    exit_code = 1 if xml_only or json_only or diffs else 0
    
    # accuracy_metrics をレポート書き出し関数に渡す
    write_report_document(
        report_path, xml_path, json_path, xml_only, json_only, diffs, full_report, exit_code,
        accuracy_metrics
    )

    return exit_code
# --- ▲▲▲ 修正 (run_validation で ⑺ のコメント修正) ▲▲▲ ---


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="api_template.xml と neo4j_data.json の整合性検証")
    parser.add_argument(
        "--xml", type=Path, default=Path("api_template.xml"), help="APIテンプレートXMLのパス"
    )
    parser.add_argument(
        "--json", type=Path, default=Path("neo4j_data.json"), help="Neo4jグラフ構造JSONのパス"
    )
    parser.add_argument(
        "--report", type=Path, default=Path("validation_report.md"), help="検証結果を書き出すMarkdownファイルのパス"
    )
    return parser


# --- ▼▼▼ 修正 (main で APIキーの警告) ▼▼▼ ---
def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not OPENAI_CLIENT:
        print("=" * 50, file=sys.stderr)
        # ★ 警告メッセージを config.py を参照するように修正
        print("警告: config.py に OPENAI_API_KEY が設定されていません。", file=sys.stderr)
        print("LLMによる文脈一致評価 (⑺) は実行されず、正答率は 0% になります。", file=sys.stderr)
        print("=" * 50, file=sys.stderr)

    if not args.xml.exists():
        print(f"XMLファイルが見つかりません: {args.xml}", file=sys.stderr)
        return 2
    if not args.json.exists():
        print(f"JSONファイルが見つかりません: {args.json}", file=sys.stderr)
        return 2

    return run_validation(args.xml, args.json, args.report)
# --- ▲▲▲ 修正 (main で APIキーの警告) ▲▲▲ ---


if __name__ == "__main__":
    sys.exit(main())