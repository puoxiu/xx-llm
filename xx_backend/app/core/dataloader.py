from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, ToMarkdownLoader


class DataLoaderModule:
    def __init__(self, dir_path: str, chunk_size = 500, chunk_overlap = 100):
        """
        初始化数据加载器模块
        Args:
            dir_path (str): 包含所有文档的目录路径
            chunk_size (int, optional): 每个文档块的大小. Defaults to 500.
            chunk_overlap (int, optional): 文档块之间的重叠大小. Defaults to 100.
        """
        self.dir_path = dir_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.documents = []
        self.text_splitter = CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def load_text_documents(self):
        """加载文本文件"""
        loader = DirectoryLoader(
            self.dir_path,
            glob="**/*.txt",
            show_progress=True
        )
        # 加载文本文件
        raw_documents = loader.load()
        # 文本文件切分
        self.documents.extend(self.text_splitter.split_documents(raw_documents))

    def load_json_documents(self):
        """加载json文件"""
        loader = DirectoryLoader(
            self.dir_path,
            glob="**/*.json",
            show_progress=True
        )
        # 加载json文件
        raw_documents = loader.load()
        # json文件切分
        self.documents.extend(self.text_splitter.split_documents(raw_documents))

    def load_md_documents(self):
        """加载markdown文件"""
        loader = DirectoryLoader(
            self.dir_path,
            glob="**/*.md",
            show_progress=True
        )
        # 加载markdown文件
        raw_documents = loader.load()
        # markdown文件切分
        self.documents.extend(self.text_splitter.split_documents(raw_documents))


    def validate_and_clean_data(self):
        """数据验证与清洗"""
        raw_documents = self.documents
        # 去除空内容
        self.documents = [doc for doc in self.documents if doc.page_content.strip()]

        # 去重
        self.documents = list(set(self.documents))
        # 打印处理前和后的文档数量
        print(f"处理前文档数量: {len(raw_documents)}")
        print(f"处理后文档数量: {len(self.documents)}")

    def load_all_documents(self, json_path, md_path):
        """加载所有文档并进行验证和清洗"""
        self.load_text_documents()
        self.load_json_documents()
        self.load_md_documents()
        self.validate_and_clean_data()

    def display_summary(self):
        """数据加载和处理的结果统计"""
        print(f"加载的文档总数: {len(self.documents)}")

if __name__ == "__main__":
    data_loader = DataLoaderModule("./data")

    data_loader.load_all_documents("./data/json", "./data/md")
    data_loader.display_summary()