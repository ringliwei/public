import fitz

# pip install fitz
# pip install PyMuPDF


def pdf_image(pdfPath, imgPath, zoom_x, zoom_y, rotation_angle):
    """按页生成每页的图片

    Args:
        pdfPath (str): pdf路经
        imgPath (str): 图片存放路经
        zoom_x (int): 控制分辨率
        zoom_y (int): 控制分辨率
        rotation_angle (int): _description_
    """

    pdf = fitz.open(pdfPath)
    for pg in range(0, pdf.pageCount):
        page = pdf[pg]
        trans = fitz.Matrix(zoom_x, zoom_y).prerotate(rotation_angle)
        pm = page.get_pixmap(matrix=trans, alpha=False)
        pm.save(imgPath + str(pg) + ".png")
        print(f"page {pg}")
    pdf.close()


pdf_image(r"xxx.pdf", r"images/", 5, 5, 0)
