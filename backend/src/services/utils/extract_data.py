from langchain_community.document_loaders import (
    WebBaseLoader,
    TextLoader,
    PyPDFLoader,
    CSVLoader,
    Docx2txtLoader,
    UnstructuredEPubLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredMarkdownLoader,
    UnstructuredXMLLoader,
    UnstructuredRSTLoader,
    UnstructuredExcelLoader,
)

class ExtratData():
    
    def __init__(self):
        pass

    def file_loader(self,file_path: str):
        if '/' in file_path:
            filename = file_path.split('/')[-1]
        elif '\\' in file_path:
            filename = file_path.split('\\')[-1]
        
        file_content_type = filename.split('.')[-1]

        file_ext = filename.split(".")[-1].lower()
        known_type = True
        

        known_source_ext = [
            "go",
            "py",
            "java",
            "sh",
            "bat",
            "ps1",
            "cmd",
            "js",
            "ts",
            "css",
            "cpp",
            "hpp",
            "h",
            "c",
            "cs",
            "sql",
            "log",
            "ini",
            "pl",
            "pm",
            "r",
            "dart",
            "dockerfile",
            "env",
            "php",
            "hs",
            "hsc",
            "lua",
            "nginxconf",
            "conf",
            "m",
            "mm",
            "plsql",
            "perl",
            "rb",
            "rs",
            "db2",
            "scala",
            "bash",
            "swift",
            "vue",
            "svelte",
        ]

        if file_ext == "pdf":
            loader = PyPDFLoader(file_path)
        elif file_ext == "csv":
            loader = CSVLoader(file_path)
        elif file_ext == "rst":
            loader = UnstructuredRSTLoader(file_path, mode="elements")
        elif file_ext == "xml":
            loader = UnstructuredXMLLoader(file_path)
        elif file_ext == "md":
            loader = UnstructuredMarkdownLoader(file_path)
        elif file_content_type == "application/epub+zip":
            loader = UnstructuredEPubLoader(file_path)
        elif (
            file_content_type
            == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            or file_ext in ["doc", "docx"]
        ):
            loader = Docx2txtLoader(file_path)
        elif file_content_type in [
            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ] or file_ext in ["xls", "xlsx"]:
            loader = UnstructuredExcelLoader(file_path)
        elif file_ext in known_source_ext or (
            file_content_type and file_content_type.find("text/") >= 0
        ):
            loader = TextLoader(file_path, autodetect_encoding=True)
        else:
            loader = TextLoader(file_path, autodetect_encoding=True)
            known_type = False

        return loader, known_type


    def web_loader(self,link):
        known_type = 'link'
        loader = WebBaseLoader(link)
        return loader, known_type
