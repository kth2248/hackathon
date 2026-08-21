# parts/nlp/command_parser.py
"""
자연어 명령 파서(규칙 기반 NLP): 문장에서 키워드/숫자/패턴을 추출해 구조화된 명령으로 변환.
순수 파이썬 — vpython 불필요, 인터넷 불필요(오프라인 안전).

사용처: F 말로 짓는 도시 ("나무 20그루랑 태양광 5개" -> {tree:20, solar:5}).

개념: 거대 AI 모델 없이도 '키워드 사전 + 정규식'으로 자연어의 핵심을 뽑아낼 수 있다.
이것이 자연어처리(NLP)의 가장 기본 원리다.
"""
import re


def extract_count(text, default=1, max_count=None):
    """문장에서 개수를 추출. "3개", "5그루", 그냥 "7" 등. 못 찾으면 default."""
    m = (re.search(r"(\d+)\s*개", text)
         or re.search(r"(\d+)\s*그루", text)
         or re.search(r"(\d+)", text))
    n = int(m.group(1)) if m else default
    if max_count is not None:
        n = min(n, max_count)
    return max(0, n)


def extract_keyword(text, keyword_map, default=None):
    """keyword_map(키워드->값)에서 문장에 처음 등장하는 키워드의 값을 반환."""
    for kw, val in keyword_map.items():
        if kw in text:
            return val
    return default


def extract_all_counts(text, keyword_map, max_count=None):
    """여러 종류를 한 문장에서: "나무 20 태양광 5" -> {값: 개수}.
    각 키워드 바로 뒤(또는 앞)의 숫자를 그 키워드의 개수로 잡는다.
    """
    result = {}
    for kw, val in keyword_map.items():
        # "나무 20" 또는 "20 나무" 형태의 숫자를 찾음
        m = (re.search(kw + r"\s*(\d+)", text)
             or re.search(r"(\d+)\s*(?:개|그루)?\s*" + kw, text))
        if kw in text:
            n = int(m.group(1)) if m else 1
            if max_count is not None:
                n = min(n, max_count)
            result[val] = result.get(val, 0) + n
    return result


def parse(text, fields):
    """여러 필드를 한 번에 추출.
    fields: {이름: (키워드맵, 기본값)}  ->  {이름: 값} 반환.
    개수는 extract_count/extract_all_counts를 따로 쓰면 된다.
    """
    return {name: extract_keyword(text, kmap, default)
            for name, (kmap, default) in fields.items()}
