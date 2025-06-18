from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os


class EmbeddingModule:
    def __init__(self, dataloader, faiss_index_path = "faiss_index"):
        """
        初始化嵌入模块
        Args:
            dataloader (DataLoaderModule): 数据加载模块
            faiss_index_path (str, optional): FAISS 索引文件路径. Defaults to "faiss_index".
        """
        self.dataloader = dataloader
        self.faiss_index_path = faiss_index_path
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None

    def build_faiss_vector_store(self):
        """
        构建 FAISS 向量存储
        """
        self.vectorstore = FAISS.from_documents(
            self.dataloader.documents,
            self.embeddings
        )
        self.vectorstore.save_local(self.faiss_index_path)

    def load_faiss_vector_store(self):
        """
        加载 FAISS 向量存储
        """
        if os.path.exists(self.faiss_index_path):
            self.vectorstore = FAISS.load_local(self.faiss_index_path, self.embeddings)
        else:
            raise FileNotFoundError(f"FAISS 索引文件 {self.faiss_index_path} 不存在")

    def query_similar_documents(self, query: str, top_k: int = 3) -> list[str]:
        """
        查询与查询文本相似的文档
        Args:
            query (str): 查询文本
            top_k (int, optional): 返回的最相似文档数量. Defaults to 3.
        Returns:
            list: 包含最相似文档的列表
        """
        if not self.vectorstore:
            raise ValueError("FAISS 向量存储未加载")
        # 将输入文本转换为嵌入向量
        query_embedding = self.embeddings.embed_query(query)
        # 使用嵌入向量查询最相似的文档
        docs = self.vectorstore.similarity_search_by_vector(query_embedding, top_k)
        # 返回文本内容
        return [doc.page_content for doc in docs]
    
# todo
# 支持动态添加 or 删除？
# 持久化是怎么做的？可以多用户隔离？
# embedding模型是什么？

if __name__ == "__main__":
    from core.dataloader import DataLoaderModule
    from core.config import settings

    settings.OPENAI_API_KEY = "sk-xxxx"
    dataloader = DataLoaderModule("data")
    dataloader.load_text_documents()
    embedding = EmbeddingModule(dataloader)
    embedding.build_faiss_vector_store()
    embedding.load_faiss_vector_store()
    print(embedding.query_similar_documents("你好"))
    
