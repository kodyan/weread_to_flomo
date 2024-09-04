import requests
import json

DEBUG = False  # True 时只本地打印 log，不发请求；False 时会向 flomo 进行同步


def read_paragraphs(file_path):
    """
    微信读书笔记导出格式是按章分隔，章之间两个空格，章内每条笔记以◆开头
    """
    with open(file_path, "r", encoding="utf-8") as file:
        txt = file.read().strip()
        nums, content = process_text(txt)
        # 删掉末尾的"-- 来自微信读书"
        if content.endswith("-- 来自微信读书"):
            content = content[: -len("-- 来自微信读书")]
    # 使用恰好两个换行符分割文本
    paragraphs = content.split("\n\n\n")
    # 去除段落开头和结尾的空白字符，并保留段落内的格式
    return (nums, [p.strip("\n") for p in paragraphs if p.strip()])


def send_post_request(api_url, tag, content):
    """
    按条发送笔记到 flomo
    """
    headers = {"Content-Type": "application/json"}
    data = {"content": f"{tag}\n{content}"}
    print(f"正在发送:\n{tag}\n{content}")

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # 如果响应状态码不是 200，将引发异常
        print(
            f"POST request successful for content. Status code: {response.status_code}"
        )
        print(f"Response: {response.text}\n")
    except requests.RequestException as e:
        print(f"Error sending POST request: {e}\n")


def split_paragraphs(paragraph):
    """
    解析每个段落中的每条笔记
    """
    lines = [line for line in paragraph.split("\n") if line.strip()]  # 去除空行
    if lines and not lines[0].startswith("◆"):
        title = lines[0]
        lines = lines[1:]
    else:
        title = "未命名段落"  # 若第一段就是以◆开头的内容，设置默认标题

    contents = []
    current_content = ""
    for line in lines:
        if line and line.startswith("◆"):
            if current_content:
                contents.append(current_content.strip())
            current_content = line[1:]
        else:
            current_content += "\n" + line
    if current_content:
        contents.append(current_content.strip())
    return contents


def main(file_path, api_url, tag):
    targetTotal, paragraphs = read_paragraphs(file_path)

    # 书评不记录
    if len(paragraphs) > 0 and paragraphs[0].startswith("点评"):
        paragraphs = paragraphs[1:]
        targetTotal -= 1

    # 打印每个段落
    contents = []
    for i, paragraph in enumerate(paragraphs, 1):
        print(f"正在处理段落 {i}:")
        print(paragraph + "\n")

        contents.extend(split_paragraphs(paragraph))

        print("-" * 50)

        print("=" * 50 + "\n")
    if targetTotal != len(contents):
        raise Exception(
            f"导出{targetTotal}个笔记，实际解析{len(contents)}个笔记，解析出错"
        )
    else:
        print(f"导出{targetTotal}个笔记，实际解析{len(contents)}个笔记，解析正确")
        for content in contents:
            if not DEBUG:
                send_post_request(api_url, tag, content)


def process_text(text):
    start_index = text.find("个笔记")
    if start_index == -1:
        return text
    number_str = ""
    for char in reversed(text[:start_index]):
        if char.isdigit():
            number_str = char + number_str
        else:
            break
    nums = int(number_str) if number_str else 0
    return (nums, text[start_index + len("个笔记") + len(number_str) :])


if __name__ == "__main__":
    api_url = input("输入flomo api: ")
    print(api_url)

    tag = input("输入标签名称(例：#读书/悉达多): ")
    print(tag)

    file_path = input("导出笔记的文件路径: ")

    main(file_path=file_path, api_url=api_url, tag=tag)
