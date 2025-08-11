import os
import math
import argparse
from PyPDF2 import PdfReader, PdfWriter
from tqdm import tqdm


def split_pdf_by_pages(input_path, output_dir, pages_per_split, prefix):
    """
    按页数分割PDF文件

    参数:
        input_path (str): 输入PDF文件路径
        output_dir (str): 输出目录
        pages_per_split (int): 每个分片的页数
        prefix (str): 输出文件名前缀
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 打开PDF文件
    pdf = PdfReader(input_path)
    total_pages = len(pdf.pages)

    # 计算分片数量
    num_splits = math.ceil(total_pages / pages_per_split)

    print(f"开始分割: {os.path.basename(input_path)}")
    print(f"总页数: {total_pages}, 每个分片页数: {pages_per_split}, 将生成 {num_splits} 个分片")

    # 使用进度条
    with tqdm(total=num_splits, desc="处理进度") as pbar:
        for i in range(num_splits):
            # 创建PDF写入对象
            writer = PdfWriter()

            # 计算当前分片的起始页和结束页
            start_page = i * pages_per_split
            end_page = min((i + 1) * pages_per_split, total_pages)

            # 添加页面到当前分片
            for page_num in range(start_page, end_page):
                writer.add_page(pdf.pages[page_num])

            # 生成输出文件名
            output_filename = f"{prefix}_{i+1:03d}.pdf"
            output_path = os.path.join(output_dir, output_filename)

            # 写入分片文件
            with open(output_path, "wb") as out_file:
                writer.write(out_file)

            pbar.update(1)
            pbar.set_postfix(file=output_filename)

    print(f"\n分割完成! 分片文件已保存到: {output_dir}")


def split_pdf_by_size(input_path, output_dir, max_size_mb, prefix):
    """
    按文件大小分割PDF文件

    参数:
        input_path (str): 输入PDF文件路径
        output_dir (str): 输出目录
        max_size_mb (float): 每个分片的最大大小(MB)
        prefix (str): 输出文件名前缀
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 打开PDF文件
    pdf = PdfReader(input_path)
    total_pages = len(pdf.pages)

    # 计算目标大小（字节）
    max_size_bytes = max_size_mb * 1024 * 1024

    print(f"开始分割: {os.path.basename(input_path)}")
    print(f"总页数: {total_pages}, 每个分片最大大小: {max_size_mb:.2f} MB")

    # 初始化变量
    current_writer = PdfWriter()
    current_size = 0
    split_index = 1
    current_pages = 0

    # 使用进度条
    with tqdm(total=total_pages, desc="处理进度") as pbar:
        for page_num in range(total_pages):
            # 添加当前页到临时写入器以估算大小
            temp_writer = PdfWriter()
            for p in current_writer.pages:
                temp_writer.add_page(p)
            temp_writer.add_page(pdf.pages[page_num])

            # 计算临时文件大小
            temp_size = len(temp_writer.write_to_bytes())

            # 如果添加当前页会超过大小限制，保存当前分片
            if temp_size > max_size_bytes and current_size > 0:
                output_filename = f"{prefix}_{split_index:03d}.pdf"
                output_path = os.path.join(output_dir, output_filename)

                with open(output_path, "wb") as out_file:
                    current_writer.write(out_file)

                pbar.set_postfix(file=output_filename, pages=current_pages, size=f"{current_size/1024/1024:.2f}MB")

                # 重置写入器和计数器
                current_writer = PdfWriter()
                current_writer.add_page(pdf.pages[page_num])
                current_size = len(current_writer.write_to_bytes())
                current_pages = 1
                split_index += 1
            else:
                # 添加当前页到分片
                current_writer.add_page(pdf.pages[page_num])
                current_size = temp_size
                current_pages += 1

            pbar.update(1)

        # 保存最后一个分片
        if current_pages > 0:
            output_filename = f"{prefix}_{split_index:03d}.pdf"
            output_path = os.path.join(output_dir, output_filename)

            with open(output_path, "wb") as out_file:
                current_writer.write(out_file)

            pbar.set_postfix(file=output_filename, pages=current_pages, size=f"{current_size/1024/1024:.2f}MB")

    print(f"\n分割完成! 共生成 {split_index} 个分片文件，已保存到: {output_dir}")


def main():
    '''
    示例:
    1. 按页数分割:
    python pdf_splitter.py input.pdf --pages 10

    2. 按文件大小分割(每个分片不超过5MB)
    python pdf_splitter.py input.pdf --size 5

    3. 自定义输出目录和文件名前缀：
    python pdf_splitter.py input.pdf --pages 10 --output my_output --prefix my_split

    4. 按文件大小分割(每个分片不超过5MB)，自定义输出目录和文件名前缀：
    python pdf_splitter.py input.pdf --size 5 --output my_output --prefix my_split
    '''

    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(
        description="PDF文件分片处理工具",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("input", help="输入的PDF文件路径")
    parser.add_argument("-o", "--output", default="output",
                        help="输出目录")
    parser.add_argument("-p", "--prefix", default="split",
                        help="输出文件名的前缀")
    parser.add_argument("--pages", type=int,
                        help="按页数分割，指定每个分片的页数")
    parser.add_argument("--size", type=float,
                        help="按文件大小分割，指定每个分片的最大大小(MB)")

    args = parser.parse_args()

    # 检查输入文件是否存在
    if not os.path.isfile(args.input):
        print(f"错误: 输入文件 '{args.input}' 不存在!")
        return

    # 确保至少指定了一种分割方式
    if args.pages is None and args.size is None:
        print("错误: 必须指定 --pages 或 --size 参数来选择分割方式!")
        return

    # 执行分割操作
    try:
        if args.pages:
            split_pdf_by_pages(args.input, args.output, args.pages, args.prefix)
        else:
            split_pdf_by_size(args.input, args.output, args.size, args.prefix)
    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")


if __name__ == "__main__":
    main()
