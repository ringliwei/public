import argparse
import os
from PyPDF2 import PdfReader, PdfWriter


def extract_pages(input_path, pages, output_path="output.pdf"):
    """
    从PDF文件中提取指定页面并保存为新文件

    参数:
        input_path (str): 输入PDF文件路径
        pages (list): 要提取的页面索引列表(从0开始)
        output_path (str): 输出文件路径
    """
    # 验证输入文件是否存在
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"输入文件 '{input_path}' 不存在")

    # 创建输出目录(如果不存在)
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 读取PDF文件
    with open(input_path, "rb") as in_file:
        reader = PdfReader(in_file)
        total_pages = len(reader.pages)

        # 验证页面索引是否有效
        invalid_pages = [p for p in pages if p < 0 or p >= total_pages]
        if invalid_pages:
            raise ValueError(f"无效的页面索引: {invalid_pages}. "
                             f"文档共有 {total_pages} 页 (索引范围 0-{total_pages-1})")

        # 提取指定页面
        writer = PdfWriter()
        extracted_count = 0

        for page_num in pages:
            writer.add_page(reader.pages[page_num])
            extracted_count += 1

        # 写入输出文件
        with open(output_path, "wb") as out_file:
            writer.write(out_file)

    return extracted_count, total_pages


def parse_page_range(range_str):
    """
    解析页面范围字符串(如 "1,3,5-8")为页面索引列表

    参数:
        range_str (str): 页面范围字符串

    返回:
        list: 页面索引列表(从0开始)
    """
    pages = []
    parts = range_str.split(',')

    for part in parts:
        if '-' in part:
            # 处理范围 (如 "5-8")
            start_end = part.split('-')
            if len(start_end) != 2:
                raise ValueError(f"无效的范围格式: '{part}'. 请使用 '起始页-结束页' 格式")

            try:
                start = int(start_end[0].strip()) - 1  # 转换为0-based索引
                end = int(start_end[1].strip())  # 结束页是1-based
            except ValueError:
                raise ValueError(f"无效的数字格式: '{part}'")

            if start < 0 or end <= 0:
                raise ValueError(f"页码必须为正数: '{part}'")
            if start >= end:
                raise ValueError(f"起始页必须小于结束页: '{part}'")

            pages.extend(range(start, end))
        else:
            # 处理单个页码
            try:
                page_num = int(part.strip()) - 1  # 转换为0-based索引
            except ValueError:
                raise ValueError(f"无效的页码: '{part}'")

            if page_num < 0:
                raise ValueError(f"页码必须为正数: '{part}'")

            pages.append(page_num)

    # 去重并排序
    return sorted(set(pages))


def main():
    '''
    支持单个页码（如 1,3,5）
    支持页面范围（如 5-8）
    支持混合格式（如 1,3,5-8,10）


    注意：
    1. 页码从1开始计数。
    2. 范围包含起始页和结束页。
    3. 输入文件必须是PDF格式。
    4. 输出文件将自动创建在当前目录下。
    5. 输出文件名默认是 output.pdf。

    示例：
    1. 提取第1、3、5页：
    python pdf_pick_up.py document.pdf -p "1,3,5"

    2. 提取第5页到第8页：
    python pdf_pick_up.py document.pdf -p "5-8"

    3. 提取第1页、第3页、第5页到第8页、第10页：
    python pdf_pick_up.py document.pdf -p "1,3,5-8,10"

    '''
    parser = argparse.ArgumentParser(
        description="PDF页面提取工具 - 从PDF文件中提取指定页面",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("input", help="输入的PDF文件路径")
    parser.add_argument("-p", "--pages", required=True,
                        help="要提取的页面，支持范围和单个页码 (例如: '1,3,5-8')")
    parser.add_argument("-o", "--output", default="output.pdf",
                        help="输出文件路径")

    args = parser.parse_args()

    try:
        # 解析页面范围
        page_indices = parse_page_range(args.pages)

        # 提取页面
        extracted_count, total_pages = extract_pages(
            args.input,
            page_indices,
            args.output
        )

        print(f"成功提取 {extracted_count} 页 (从 {total_pages} 页文档中)")
        print(f"输出文件已保存到: {os.path.abspath(args.output)}")

    except Exception as e:
        print(f"错误: {str(e)}")
        exit(1)


if __name__ == '__main__':
    main()
