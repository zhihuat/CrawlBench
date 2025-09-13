import sys
from bs4 import BeautifulSoup
import os

def print_tree(element, indent=0):
    """
    递归打印 DOM 树，显示标签名、属性和文本。
    """
    for child in element.children:
        if child.name:  # 标签节点
            # 格式化标签名和属性
            attrs = " ".join([f'{k}="{v}"' for k, v in child.attrs.items()])
            if attrs:
                print("  " * indent + f"<{child.name} {attrs}>")
            else:
                print("  " * indent + f"<{child.name}>")
            print_tree(child, indent + 1)
        elif child.string and child.string.strip():  # 文本节点
            text = child.string.strip().replace("\n", " ")
            print("  " * indent + f"\"{text}\"")

def main():
    # if len(sys.argv) < 2:
    #     print("用法: python print_dom.py <html文件路径>")
    #     sys.exit(1)

    file_path = "/Users/zhihua/Projects/AgentScope/toscrape/a-light-in-the-attic"
    file_path = os.path.join(file_path, "index.html")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            html_str = f.read()
    except Exception as e:
        print(f"读取文件失败: {e}")
        sys.exit(1)

    # 解析 HTML
    soup = BeautifulSoup(html_str, "html.parser")

    # 打印 DOM 树
    print_tree(soup)

if __name__ == "__main__":
    main()