'''
pip install fitz
pip install PyMuPDF
'''

import fitz

def pdf_image(pdf_path, img_save_dir, zoom_x, zoom_y, rotation_angle):
    """按页生成每页的图片

    Args:
        pdf_path (str): pdf全路经
        img_save_dir (str): 图片存放路经
        zoom_x (int): 控制分辨率
        zoom_y (int): 控制分辨率
        rotation_angle (int): _description_
    """

    pdf = fitz.open(pdf_path)
    for pg in range(0, pdf.pageCount):
        page = pdf[pg]
        trans = fitz.Matrix(zoom_x, zoom_y).prerotate(rotation_angle)
        pm = page.get_pixmap(matrix=trans, alpha=False)
        pm.save(img_save_dir + str(pg) + ".png")
        print(f"page {pg}")
    pdf.close()


pdf_image(r"xxx.pdf", r"images/", 5, 5, 0)
