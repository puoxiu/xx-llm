import uuid

def generate_namespace() -> str:
    """
    生成一个唯一的命名空间 ID，用于隔离向量数据库数据
    """
    return "ns_" + uuid.uuid4().hex[:12]
