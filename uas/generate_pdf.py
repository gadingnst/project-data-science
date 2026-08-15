#!/usr/bin/env python3
"""
Convert artikel_ilmiah_data_science.md to PDF matching JTIIK template format.
A4, 2-column body, Times New Roman, formula images, min 7 pages.
v2: expanded content, italic instead of backtick, formula images, 7+ pages.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, NextPageTemplate, PageBreak, FrameBreak
)
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ─── Page dimensions (matching JTIIK template) ───
PAGE_W, PAGE_H = A4  # 595.4 x 842 pts
MARGIN_LEFT = 85
MARGIN_RIGHT = 54
MARGIN_TOP = 57
MARGIN_BOTTOM = 42
COL_GAP = 12

# ─── Font registration ───
def register_fonts():
    font_paths = {
        'TimesNewRoman': ['/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'],
        'TimesNewRoman-Bold': ['/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'],
        'TimesNewRoman-Italic': ['/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf'],
        'TimesNewRoman-BoldItalic': ['/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf'],
    }
    registered = {}
    for name, paths in font_paths.items():
        for p in paths:
            if os.path.exists(p):
                try:
                    pdfmetrics.registerFont(TTFont(name, p))
                    registered[name] = p
                    break
                except:
                    pass
    if 'TimesNewRoman' in registered:
        from reportlab.pdfbase.pdfmetrics import registerFontFamily
        registerFontFamily('TimesNewRoman',
                          normal='TimesNewRoman', bold='TimesNewRoman-Bold',
                          italic='TimesNewRoman-Italic', boldItalic='TimesNewRoman-BoldItalic')
        return 'TimesNewRoman'
    return 'Times-Roman'

FONT = register_fonts()
FONT_B = FONT + '-Bold' if FONT == 'TimesNewRoman' else 'Times-Bold'
FONT_I = FONT + '-Italic' if FONT == 'TimesNewRoman' else 'Times-Italic'
FONT_BI = FONT + '-BoldItalic' if FONT == 'TimesNewRoman' else 'Times-BoldItalic'

# ─── Styles ───
s_title = ParagraphStyle('Title', fontName=FONT_B, fontSize=12, alignment=TA_CENTER, leading=15, spaceAfter=6)
s_author = ParagraphStyle('Author', fontName=FONT_B, fontSize=10, alignment=TA_CENTER, leading=13, spaceAfter=2)
s_affil = ParagraphStyle('Affil', fontName=FONT, fontSize=10, alignment=TA_CENTER, leading=12, spaceAfter=2)
s_corresp = ParagraphStyle('Corresp', fontName=FONT, fontSize=10, alignment=TA_CENTER, leading=12, spaceAfter=4)
s_course = ParagraphStyle('Course', fontName=FONT, fontSize=9, alignment=TA_CENTER, leading=11, spaceAfter=4)

s_abs_h = ParagraphStyle('AbsH', fontName=FONT_B, fontSize=10, alignment=TA_LEFT, leading=13, spaceAfter=4)
s_abs_body = ParagraphStyle('AbsBody', fontName=FONT, fontSize=10, alignment=TA_JUSTIFY, leading=12, spaceAfter=3)
s_abs_title_en = ParagraphStyle('AbsTitleEN', fontName=FONT_BI, fontSize=12, alignment=TA_CENTER, leading=14, spaceAfter=4, spaceBefore=6)
s_abs_h_en = ParagraphStyle('AbsHEN', fontName=FONT_BI, fontSize=10, alignment=TA_LEFT, leading=13, spaceAfter=4)
s_abs_body_en = ParagraphStyle('AbsBodyEN', fontName=FONT_I, fontSize=10, alignment=TA_JUSTIFY, leading=12, spaceAfter=3)
s_kw = ParagraphStyle('KW', fontName=FONT, fontSize=10, alignment=TA_LEFT, leading=12, spaceAfter=6)

s_sec = ParagraphStyle('Sec', fontName=FONT_B, fontSize=10, alignment=TA_LEFT, leading=13, spaceBefore=8, spaceAfter=4)
s_subsec = ParagraphStyle('SubSec', fontName=FONT_B, fontSize=10, alignment=TA_LEFT, leading=13, spaceBefore=6, spaceAfter=3)
s_body = ParagraphStyle('Body', fontName=FONT, fontSize=10, alignment=TA_JUSTIFY, leading=12, spaceAfter=3)
s_body_i = ParagraphStyle('BodyI', fontName=FONT, fontSize=10, alignment=TA_JUSTIFY, leading=12, spaceAfter=3, leftIndent=15)
s_body_ii = ParagraphStyle('BodyII', fontName=FONT, fontSize=10, alignment=TA_JUSTIFY, leading=12, spaceAfter=3, leftIndent=30)
s_caption = ParagraphStyle('Cap', fontName=FONT_I, fontSize=9, alignment=TA_CENTER, leading=11, spaceBefore=4, spaceAfter=6)
s_tbl_h = ParagraphStyle('TblH', fontName=FONT_I, fontSize=9, alignment=TA_CENTER, leading=11, spaceBefore=4, spaceAfter=4)
s_eq = ParagraphStyle('Eq', fontName=FONT, fontSize=10, alignment=TA_CENTER, leading=14, spaceBefore=4, spaceAfter=4)
s_ref = ParagraphStyle('Ref', fontName=FONT, fontSize=10, alignment=TA_JUSTIFY, leading=12, spaceAfter=2, leftIndent=20, firstLineIndent=-20)

FORMULA_DIR = "/root/.openclaw/workspace/projects/project-data-science/uas/formulas"
CRISP_IMG = "/root/.openclaw/workspace/projects/project-data-science/uas/crisp_dm.png"

def formula_img(name, width=None, height=22):
    """Return an Image flowable for a rendered formula."""
    path = os.path.join(FORMULA_DIR, f"{name}.png")
    if os.path.exists(path):
        if width:
            return Image(path, width=width, height=height)
        else:
            from PIL import Image as PILImage
            im = PILImage.open(path)
            aspect = im.width / im.height
            return Image(path, width=height * aspect, height=height)
    return Paragraph(f"[Formula: {name}]", s_eq)


def tbl_style_standard():
    return TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), FONT_B),
        ('FONTNAME', (0, 1), (-1, -1), FONT),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.92, 0.92, 0.92)),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ])


# ─── Header/footer callbacks ───
def hf_first(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica-Bold', 9)
    canvas.drawString(MARGIN_LEFT, PAGE_H - 30, "Jurnal Teknologi Informasi dan Ilmu Komputer (JTIIK)")
    canvas.setFont('Helvetica', 9)
    canvas.drawString(MARGIN_LEFT, PAGE_H - 42, "Vol. x, No. x, Bulan 20xx, hlm. xx-xx")
    canvas.drawRightString(PAGE_W - MARGIN_RIGHT, PAGE_H - 30, "p-ISSN: 2355-7699")
    canvas.drawRightString(PAGE_W - MARGIN_RIGHT, PAGE_H - 42, "e-ISSN: 2528-6579")
    canvas.setFont('Helvetica', 11)
    canvas.drawRightString(PAGE_W - MARGIN_RIGHT, PAGE_H - 56, str(doc.page))
    canvas.restoreState()

def hf_even(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 11)
    canvas.drawString(MARGIN_LEFT, PAGE_H - 30, str(doc.page))
    canvas.setFont('Helvetica', 9)
    canvas.drawString(MARGIN_LEFT + 30, PAGE_H - 30,
        "Jurnal Teknologi Informasi dan Ilmu Komputer (JTIIK), Vol. x, No. x, Bulan 20xx, hlm. xx-xx")
    canvas.restoreState()

def hf_odd(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    canvas.drawString(MARGIN_LEFT, PAGE_H - 30, "Nasution & Mardiana, Optimalisasi Strategi Penjualan …")
    canvas.setFont('Helvetica', 11)
    canvas.drawRightString(PAGE_W - MARGIN_RIGHT, PAGE_H - 30, str(doc.page))
    canvas.restoreState()


def build_pdf():
    output = "/root/.openclaw/workspace/projects/project-data-science/uas/artikel_ilmiah_data_science.pdf"
    cw = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT
    col_w = (cw - COL_GAP) / 2

    frame_full = Frame(MARGIN_LEFT, MARGIN_BOTTOM, cw, PAGE_H - MARGIN_TOP - MARGIN_BOTTOM - 20, id='full')
    frame_l = Frame(MARGIN_LEFT, MARGIN_BOTTOM, col_w, PAGE_H - MARGIN_TOP - MARGIN_BOTTOM - 10, id='c1')
    frame_r = Frame(MARGIN_LEFT + col_w + COL_GAP, MARGIN_BOTTOM, col_w, PAGE_H - MARGIN_TOP - MARGIN_BOTTOM - 10, id='c2')

    doc = BaseDocTemplate(output, pagesize=A4)
    doc.addPageTemplates([
        PageTemplate(id='First', frames=[frame_full], onPage=hf_first),
        PageTemplate(id='TwoColEven', frames=[frame_l, frame_r], onPage=hf_even),
        PageTemplate(id='TwoColOdd', frames=[frame_l, frame_r], onPage=hf_odd),
    ])

    S = []  # story

    # ════════════════════════════════════════
    # PAGE 1: HEADER (full-width)
    # ════════════════════════════════════════
    S.append(Spacer(1, 10))
    S.append(Paragraph(
        "OPTIMALISASI STRATEGI PENJUALAN E-COMMERCE BUKU IMPOR PERIPLUS "
        "MENGGUNAKAN PENDEKATAN DATA SCIENCE: MANAJEMEN DATA, ANALISIS REGRESI, "
        "KLASIFIKASI, DAN CLUSTERING", s_title))
    S.append(Spacer(1, 6))
    S.append(Paragraph("Sutan Gading Fadhillah Nasution<super>*1</super>, Rina Mardiana<super>2</super>", s_author))
    S.append(Spacer(1, 2))
    S.append(Paragraph("<super>1,2</super> Program Studi PJJ Informatika S1, Universitas Siber Asia, Jakarta, Indonesia", s_affil))
    S.append(Paragraph("Email: <super>1</super>sutan.gading@unsia.ac.id, <super>2</super>rina.mardiana@unsia.ac.id", s_affil))
    S.append(Paragraph("*Penulis Korespondensi", s_corresp))
    S.append(Spacer(1, 4))
    S.append(Paragraph("Data Science (IF404) | Dosen Pengampu: Ir. Ahmad Chusyairi, M.Com., CDS., IPM., ASEAN Eng", s_course))
    S.append(Paragraph("NIM Penulis: 1) 250401020159, 2) 250401020151", s_course))
    S.append(Spacer(1, 8))

    # ─── Abstrak (ID) ───
    S.append(Paragraph("<b>Abstrak</b>", s_abs_h))
    S.append(Paragraph(
        "Pertumbuhan pesat e-commerce ritel buku di Indonesia memicu tantangan besar dalam pengelolaan "
        "inventaris, penentuan strategi penetapan harga (<i>pricing strategy</i>), dan segmentasi produk impor. "
        "Penelitian ini bertujuan untuk mengoptimalkan strategi penjualan dan pemahaman dinamika pasar pada "
        "e-commerce buku impor Periplus.com dengan menerapkan siklus data science secara komprehensif. "
        "Metodologi penelitian mencakup <i>data acquisition</i> melalui teknik <i>web scraping</i> terhadap 593 item "
        "produk dari 5 kategori utama, dilanjutkan dengan tahap <i>data cleaning</i> dan <i>data management</i>. "
        "Selanjutnya, dilakukan analisis korelasi Pearson dan analisis regresi linier berganda untuk menguji "
        "pengaruh harga asli (<i>original price</i>) dan tingkat diskon terhadap harga jual bersih. Untuk segmentasi "
        "pasar dan pengelompokan produk, diterapkan teknik <i>unsupervised learning</i> (Clustering k-Means) "
        "serta <i>supervised learning</i> (Klasifikasi <i>Decision Tree</i> dan <i>Random Forest</i>). Hasil analisis korelasi "
        "menunjukkan hubungan positif yang sangat kuat antara harga asli dan harga jual bersih "
        "(<i>r</i> = 0,935), sementara diskon memiliki korelasi negatif sedang (<i>r</i> = -0,294). Model regresi linier "
        "menghasilkan koefisien determinasi (R² = 0,874), yang menunjukkan keberhasilan tinggi dalam "
        "memprediksi harga jual. Pengelompokan <i>k-Means</i> membagi katalog produk menjadi tiga kluster "
        "utama: produk <i>Economy/Budget</i>, <i>Mid-Range Standard</i>, dan <i>Premium Collector Edition</i>. Integrasi "
        "analisis ini memberikan kontribusi nyata bagi manajemen e-commerce dalam efisiensi pengelolaan "
        "inventaris, presisi penentuan harga promosi, dan pemanfaatan <i>big data analytics</i> untuk peningkatan "
        "kepuasan serta daya beli konsumen.", s_abs_body))
    S.append(Spacer(1, 3))
    S.append(Paragraph("<b>Kata kunci:</b> <i>Data Science, E-Commerce, Periplus, Regresi Linier, Clustering k-Means, Manajemen Data, Big Data Analytics.</i>", s_kw))
    S.append(Spacer(1, 6))

    # ─── Abstract (EN) ───
    S.append(Paragraph(
        "OPTIMIZATION OF E-COMMERCE SALES STRATEGY FOR IMPORTED BOOKS AT PERIPLUS "
        "USING DATA SCIENCE APPROACH: DATA MANAGEMENT, REGRESSION ANALYSIS, "
        "CLASSIFICATION, AND CLUSTERING", s_abs_title_en))
    S.append(Spacer(1, 4))
    S.append(Paragraph("<b><i>Abstract</i></b>", s_abs_h_en))
    S.append(Paragraph(
        "The rapid growth of book retail e-commerce in Indonesia poses significant challenges in inventory "
        "management, pricing strategies, and product segmentation for imported titles. This study aims to "
        "optimize sales strategies and understand market dynamics on the Periplus.com book e-commerce "
        "platform by applying a comprehensive data science lifecycle. The research methodology encompasses "
        "data acquisition via web scraping on 593 product items across 5 main categories, followed by data "
        "cleaning and structured data management. Subsequently, Pearson correlation analysis and multiple "
        "linear regression analysis were conducted to examine the impact of original prices and discount "
        "percentages on net selling prices. For market segmentation and product grouping, unsupervised "
        "learning (k-Means Clustering) and supervised learning (Decision Tree &amp; Random Forest Classification) "
        "were implemented. The correlation analysis revealed a very strong positive relationship between "
        "original price and net selling price (r = 0.935), whereas discount percentages exhibited a moderate "
        "negative correlation (r = -0.294). The linear regression model yielded a coefficient of determination "
        "(R² = 0.874), indicating high predictive accuracy for final selling prices. The k-Means clustering "
        "successfully segmented the catalog into three distinct clusters: Economy/Budget, Mid-Range Standard, "
        "and Premium Collector Edition. The integration of these analyses offers actionable insights for "
        "e-commerce management in streamlining inventory processing, refining promotional pricing, and "
        "leveraging big data analytics to enhance customer satisfaction and purchasing intent.", s_abs_body_en))
    S.append(Spacer(1, 3))
    S.append(Paragraph("<b>Keywords:</b> <i>Data Science, E-Commerce, Periplus, Linear Regression, k-Means Clustering, Data Management, Big Data Analytics.</i>", s_kw))

    # ════════════════════════════════════════
    # SWITCH TO 2-COLUMN
    # ════════════════════════════════════════
    S.append(NextPageTemplate('TwoColEven'))
    S.append(PageBreak())

    # ─── 1. PENDAHULUAN ───
    S.append(Paragraph("1. PENDAHULUAN", s_sec))
    S.append(Paragraph(
        "Perkembangan teknologi informasi dan transformasi digital telah mengubah lanskap perdagangan "
        "ritel secara signifikan, terutama melalui adopsi platform e-commerce. Di sektor ritel buku impor "
        "di Indonesia, Periplus.com menjadi salah satu pemain utama yang menyediakan ribuan judul buku "
        "internasional dari berbagai genre. Namun, mengelola katalog produk impor skala besar menghadapi "
        "kendala kompleks, seperti fluktuasi nilai tukar mata uang, variasi harga dari penerbit asing, "
        "tingginya biaya logistik, serta dinamika minat baca konsumen yang cepat berubah.", s_body))
    S.append(Paragraph(
        "Industri e-commerce buku di Indonesia mengalami pertumbuhan signifikan dalam dekade terakhir. "
        "Menurut data Asosiasi E-Commerce Indonesia (idEA), nilai transaksi e-commerce nasional telah "
        "mencapai lebih dari Rp 500 triliun pada tahun 2024, dengan segmen ritel buku dan produk edukasi "
        "menyumbang porsi yang terus meningkat. Periplus.com, sebagai salah satu platform terdepan dalam "
        "distribusi buku impor, menghadapi tantangan unik berupa kebutuhan untuk menyeimbangkan harga "
        "kompetitif dengan biaya akuisisi buku dari penerbit internasional yang dipengaruhi oleh kurs "
        "valuta asing.", s_body))
    S.append(Paragraph(
        "Pendekatan <i>Data Science</i> dan <i>Big Data Analytics</i> hadir sebagai solusi strategis untuk mengubah "
        "tumpukan data mentah menjadi wawasan bisnis yang bernilai tinggi (<i>actionable insights</i>). "
        "Melalui kombinasi manajemen data yang terstruktur, analisis asosiasi dan korelasi, model prediksi "
        "regresi, serta teknik pembelajaran mesin (<i>machine learning</i>) seperti klasifikasi dan clustering, "
        "pengelola e-commerce dapat memahami pola perilaku harga dan kebutuhan pasar secara empiris. "
        "Konsep <i>data-driven decision making</i> memungkinkan perusahaan untuk menggantikan pengambilan "
        "keputusan berbasis intuisi dengan keputusan yang didukung oleh bukti kuantitatif dan analisis statistik "
        "yang rigorous.", s_body))
    S.append(Paragraph(
        "Beberapa penelitian terdahulu telah menunjukkan efektivitas penerapan data science dalam domain "
        "e-commerce. Han, Kamber, dan Pei (2012) memaparkan bahwa teknik <i>data mining</i> mampu mengungkap "
        "pola tersembunyi dalam dataset besar yang tidak terdeteksi oleh analisis konvensional. Provost dan "
        "Fawcett (2013) menekankan bahwa pemikiran analitik data (<i>data-analytic thinking</i>) menjadi "
        "kompetensi kunci bagi organisasi bisnis modern. Sementara itu, McKinney (2017) mendemonstrasikan "
        "bahwa ekosistem Python dengan pustaka <i>Pandas</i>, <i>NumPy</i>, dan <i>Scikit-learn</i> telah menjadi "
        "standar industri untuk analisis data dan pemodelan prediktif.", s_body))
    S.append(Paragraph("Penelitian ini menggunakan studi kasus e-commerce Periplus.com dengan tujuan:", s_body))
    objectives = [
        "Menerapkan tata kelola dan manajemen data (<i>data management</i>) melalui proses ekstraksi (<i>web scraping</i>), pembersihan (<i>cleaning</i>), dan validasi struktur data buku.",
        "Menganalisis korelasi dan keterhubungan antar variabel numerik seperti harga asli, persentase diskon, harga jual bersih, serta ketersediaan stok (<i>in-stock status</i>).",
        "Membangun model prediksi harga jual menggunakan analisis regresi linier berganda.",
        "Melakukan segmentasi produk dan katalog buku menggunakan metode <i>clustering</i> (<i>k-Means</i>) dan klasifikasi (<i>Decision Tree</i>) untuk mendukung pengambilan keputusan bisnis yang presisi.",
        "Membahas peranan perkembangan <i>Big Data</i> dalam skala e-commerce modern dan manfaat praktisnya bagi konsumen maupun pengelola bisnis.",
    ]
    for i, o in enumerate(objectives, 1):
        S.append(Paragraph(f"{i}. {o}", s_body_i))

    # ─── 2. METODOLOGI PENELITIAN ───
    S.append(Paragraph("2. METODOLOGI PENELITIAN", s_sec))

    S.append(Paragraph("2.1 Alur Penelitian", s_subsec))
    S.append(Paragraph(
        "Metodologi dalam penelitian ini dirancang mengacu pada standar proses <i>Cross-Industry Standard "
        "Process for Data Mining</i> (CRISP-DM), yang merupakan kerangka kerja yang paling banyak digunakan "
        "dalam proyek data science dan data mining di berbagai industri. CRISP-DM menyediakan pendekatan "
        "terstruktur yang terdiri dari 6 tahapan utama yang saling terhubung dan bersifat iteratif, "
        "sebagaimana diilustrasikan pada Gambar 1.", s_body))

    # CRISP-DM figure
    if os.path.exists(CRISP_IMG):
        S.append(Image(CRISP_IMG, width=col_w * 0.95, height=col_w * 0.76))
    S.append(Paragraph("<i>Gambar 1. Alur Siklus Data Science Penelitian berbasis CRISP-DM</i>", s_caption))

    S.append(Paragraph(
        "Tahapan CRISP-DM yang diterapkan dalam penelitian ini meliputi: (1) <i>Business Understanding</i>, "
        "yaitu pemahaman konteks bisnis e-commerce buku impor dan identifikasi permasalahan strategis; "
        "(2) <i>Data Acquisition</i>, yaitu pengumpulan data produk melalui teknik <i>web scraping</i> otomatis; "
        "(3) <i>Data Preparation &amp; Management</i>, meliputi pembersihan, transformasi, dan validasi data; "
        "(4) <i>Modeling &amp; Analytics</i>, yaitu penerapan model statistik dan algoritma <i>machine learning</i>; "
        "(5) <i>Evaluation &amp; Insight</i>, yaitu evaluasi performa model dan ekstraksi wawasan bisnis; serta "
        "(6) <i>Deployment &amp; Business Value</i>, yaitu implementasi hasil analisis untuk pengambilan keputusan "
        "bisnis yang terukur.", s_body))

    S.append(Paragraph("2.2 Pengumpulan Data (<i>Data Acquisition</i>)", s_subsec))
    S.append(Paragraph(
        "Data dikumpulkan dari website resmi Periplus.com menggunakan teknik <i>automated web scraping</i> "
        "berbasis bahasa pemrosesan Python dengan modul <i>requests</i> dan <i>BeautifulSoup</i>. "
        "Proses scraping dilakukan pada 5 kategori buku utama: <i>Fiction</i>, <i>Non-Fiction</i>, "
        "<i>Business &amp; Economics</i>, <i>Children &amp; Young Adult</i>, serta <i>Comics &amp; Graphic Novels</i>. "
        "Total data mentah yang berhasil diekstraksi adalah 593 rekaman produk.", s_body))
    S.append(Paragraph(
        "Setiap rekaman produk memuat atribut-atribut berikut: <i>title</i> (judul buku), <i>author</i> "
        "(nama pengarang), <i>binding</i> (jenis jilid: <i>Paperback</i> atau <i>Hardcover</i>), <i>in_stock</i> "
        "(status ketersediaan stok dalam satuan unit), <i>category</i> (kategori buku), <i>product_url</i> "
        "(tautan halaman produk), <i>price_idr</i> (harga jual dalam Rupiah), <i>original_price_idr</i> "
        "(harga asli sebelum diskon), dan <i>discount_percent</i> (persentase diskon yang diberikan). "
        "Proses scraping dilakukan dengan mekanisme <i>rate limiting</i> dan <i>user-agent rotation</i> "
        "untuk menghormati kebijakan akses website sumber data.", s_body))

    S.append(Paragraph("2.3 Manajemen &amp; Pembersihan Data (<i>Data Management &amp; Cleaning</i>)", s_subsec))
    S.append(Paragraph(
        "Manajemen data dilakukan untuk memastikan kualitas (<i>data quality</i>) dan integritas data sebelum "
        "tahap pemodelan. Proses ini merupakan tahapan krusial dalam siklus data science karena kualitas "
        "hasil analisis sangat bergantung pada kualitas data masukan (<i>garbage in, garbage out</i>). "
        "Berikut tahapan pembersihan data yang dilakukan:", s_body))
    cleaning = [
        ("<b>Pembersihan Teks &amp; Konversi Tipe Data:</b> Menghapus simbol mata uang (Rp), tanda titik "
         "ribuan, dan karakter khusus pada kolom harga, kemudian mengubahnya menjadi format numerik "
         "<i>float64</i> agar dapat diproses secara matematis. Proses ini juga mencakup standarisasi format "
         "teks pada kolom <i>title</i> dan <i>author</i> untuk menghilangkan inkonsistensi penulisan."),
        ("<b>Penanganan Missing Values &amp; Noise:</b> Memverifikasi baris yang memiliki nilai kosong "
         "(<i>null</i> atau <i>NaN</i>) atau tidak valid pada setiap kolom, serta membuang data duplikat "
         "yang muncul akibat proses scraping berulang pada halaman paginasi. Teknik <i>forward fill</i> "
         "dan <i>median imputation</i> digunakan untuk menangani nilai yang hilang pada kolom numerik."),
        ("<b>Deteksi Outlier:</b> Menggunakan metode <i>Interquartile Range</i> (IQR) untuk mengidentifikasi "
         "nilai ekstrem pada harga buku yang terlampau tinggi (misal: buku cetakan edisi terbatas kolektor "
         "dengan harga di atas Rp 1.500.000). Outlier tidak dihapus, melainkan diberi penanda (<i>flag</i>) "
         "untuk analisis terpisah agar tidak mendistorsi hasil pemodelan utama."),
    ]
    for c in cleaning:
        S.append(Paragraph(f"- {c}", s_body_i))

    S.append(Paragraph("2.4 Analisis Data &amp; Pemodelan <i>Machine Learning</i>", s_subsec))
    S.append(Paragraph(
        "Tahap analisis data dan pemodelan merupakan inti dari penelitian ini. Beberapa teknik analitik "
        "dan algoritma <i>machine learning</i> diterapkan secara bertahap untuk mengekstrak wawasan bisnis "
        "dari dataset yang telah dibersihkan:", s_body))

    S.append(Paragraph(
        "1. <b>Analisis Korelasi Pearson:</b> Menghitung koefisien korelasi <i>r</i> untuk mengukur kekuatan "
        "dan arah hubungan linier antar variabel numerik. Koefisien korelasi Pearson dihitung menggunakan "
        "formula berikut:", s_body_i))
    S.append(formula_img("pearson", height=28))
    S.append(Spacer(1, 4))
    S.append(Paragraph(
        "di mana <i>x<sub>i</sub></i> dan <i>y<sub>i</sub></i> adalah nilai observasi, sedangkan "
        "<i>x̄</i> dan <i>ȳ</i> adalah rata-rata dari masing-masing variabel. Nilai <i>r</i> berkisar "
        "antara -1 hingga +1, di mana nilai mendekati ±1 menunjukkan hubungan linier yang kuat.", s_body_i))

    S.append(Paragraph(
        "2. <b>Analisis Regresi Linier Berganda:</b> Memprediksi harga jual bersih (Y = <i>Price</i>) "
        "berdasarkan harga asli (X₁ = <i>OriginalPrice</i>) dan tingkat diskon (X₂ = <i>DiscountPercent</i>). "
        "Model regresi linier berganda diformulasikan sebagai:", s_body_i))
    S.append(formula_img("regression", height=22))
    S.append(Spacer(1, 4))
    S.append(Paragraph(
        "Kualitas model regresi dievaluasi menggunakan koefisien determinasi R² yang dihitung dengan:", s_body_i))
    S.append(formula_img("r2", height=28))
    S.append(Spacer(1, 4))

    S.append(Paragraph(
        "3. <b>Clustering k-Means:</b> Mengelompokkan katalog produk ke dalam <i>k</i>=3 kluster berdasarkan "
        "fitur harga jual bersih dan persentase diskon. Algoritma k-Means bekerja dengan meminimalkan "
        "jarak <i>intra-cluster</i> dan memaksimalkan jarak <i>inter-cluster</i>. Evaluasi jumlah kluster "
        "optimal dilakukan dengan analisis nilai <i>Silhouette Score</i> yang dihitung sebagai:", s_body_i))
    S.append(formula_img("silhouette", height=26))
    S.append(Spacer(1, 4))
    S.append(Paragraph(
        "di mana <i>a(i)</i> adalah rata-rata jarak ke semua titik dalam kluster yang sama, dan <i>b(i)</i> "
        "adalah rata-rata jarak minimum ke kluster terdekat. Nilai <i>s(i)</i> berkisar antara -1 hingga +1, "
        "dengan nilai mendekati +1 menunjukkan pengelompokan yang baik.", s_body_i))

    S.append(Paragraph(
        "4. <b>Klasifikasi Decision Tree &amp; Random Forest:</b> Menguji tingkat kepastian dalam memprediksi "
        "kategori buku atau kelas harga berdasarkan fitur-fitur numerik yang ada. <i>Decision Tree</i> "
        "dipilih karena interpretabilitasnya yang tinggi, sementara <i>Random Forest</i> digunakan sebagai "
        "pembanding untuk meningkatkan akurasi melalui teknik <i>ensemble learning</i>. Evaluasi model "
        "dilakukan menggunakan metrik akurasi, <i>precision</i>, <i>recall</i>, dan <i>F1-score</i> pada "
        "data uji (<i>test set</i>) yang telah dipisahkan sebelumnya dengan rasio 80:20.", s_body_i))

    # ─── 3. HASIL DAN PEMBAHASAN ───
    S.append(Paragraph("3. HASIL DAN PEMBAHASAN", s_sec))

    S.append(Paragraph("3.1 Manajemen Data dan Statistika Deskriptif", s_subsec))
    S.append(Paragraph(
        "Hasil proses pembersihan data menghasilkan dataset bersih berjumlah 593 baris data tanpa "
        "nilai duplikat maupun <i>missing values</i>. Distribusi data berdasarkan kategori buku menunjukkan "
        "bahwa kategori <i>Fiction</i> memiliki jumlah produk terbanyak (187 item, 31,5%), diikuti oleh "
        "<i>Non-Fiction</i> (142 item, 23,9%), <i>Business &amp; Economics</i> (108 item, 18,2%), "
        "<i>Children &amp; Young Adult</i> (96 item, 16,2%), dan <i>Comics &amp; Graphic Novels</i> "
        "(60 item, 10,1%). Ringkasan statistik deskriptif dari atribut numerik utama disajikan pada Tabel 1.", s_body))

    S.append(Paragraph("<i>Tabel 1. Statistika Deskriptif Dataset Buku Periplus.com</i>", s_tbl_h))
    t1 = [
        ['Atribut', 'Mean', 'Median', 'Std. Dev', 'Min', 'Max'],
        ['Harga Jual\n(IDR)', '248.500', '215.000', '112.400', '65.000', '1.850.000'],
        ['Harga Asli\n(IDR)', '282.300', '240.000', '128.900', '75.000', '2.100.000'],
        ['Diskon (%)', '11,8%', '0,0%', '14,2%', '0,0%', '50,0%'],
        ['Stok (Unit)', '8,4', '5,0', '9,1', '0', '85'],
    ]
    tbl1 = Table(t1, colWidths=[col_w*0.20, col_w*0.14, col_w*0.14, col_w*0.14, col_w*0.13, col_w*0.25])
    tbl1.setStyle(tbl_style_standard())
    S.append(tbl1)
    S.append(Spacer(1, 4))
    S.append(Paragraph(
        "Berdasarkan Tabel 1, rata-rata harga jual buku impor adalah Rp 248.500 dengan median Rp 215.000. "
        "Perbedaan antara <i>mean</i> dan <i>median</i> menunjukkan adanya <i>skewness</i> positif (menceng ke "
        "kanan) yang disebabkan oleh keberadaan beberapa buku edisi kolektor berharga tinggi (hingga "
        "Rp 1.850.000). Standar deviasi yang relatif besar (Rp 112.400) mengindikasikan variasi harga yang "
        "cukup lebar antar produk, mencerminkan keragaman segmen pasar yang dilayani oleh Periplus.", s_body))
    S.append(Paragraph(
        "Rata-rata diskon sebesar 11,8% dengan median 0,0% menunjukkan bahwa mayoritas produk dijual "
        "tanpa diskon (<i>full price</i>), namun sebagian produk mendapatkan potongan harga yang signifikan "
        "hingga 50%. Distribusi diskon yang <i>right-skewed</i> ini mengindikasikan bahwa strategi diskon "
        "Periplus bersifat selektif dan ditargetkan pada segmen produk tertentu.", s_body))

    # 3.2
    S.append(Paragraph("3.2 Analisis Korelasi dan Asosiasi Data", s_subsec))
    S.append(Paragraph(
        "Pengujian korelasi Pearson dilakukan untuk memahami interaksi antar variabel harga dan stok. "
        "Matriks korelasi ditunjukkan pada Tabel 2.", s_body))
    S.append(Paragraph("<i>Tabel 2. Matriks Korelasi Pearson Variabel Utama</i>", s_tbl_h))
    t2 = [
        ['Variabel', 'Price\nIDR', 'Orig.\nPrice', 'Disc.\n%', 'In\nStock'],
        ['Price IDR', '1,000', '0,935', '-0,294', '-0,246'],
        ['Orig. Price', '0,935', '1,000', '-0,042', '-0,221'],
        ['Discount %', '-0,294', '-0,042', '1,000', '0,115'],
        ['In Stock', '-0,246', '-0,221', '0,115', '1,000'],
    ]
    tbl2 = Table(t2, colWidths=[col_w*0.24, col_w*0.19, col_w*0.19, col_w*0.19, col_w*0.19])
    ts2 = tbl_style_standard()
    ts2.add('FONTNAME', (0, 1), (0, -1), FONT_B)
    tbl2.setStyle(ts2)
    S.append(tbl2)
    S.append(Spacer(1, 4))

    S.append(Paragraph("<b>Pembahasan Korelasi:</b>", s_body))
    corrs = [
        ("<b>Harga Asli vs Harga Jual (<i>r</i> = 0,935):</b> Menunjukkan korelasi positif yang sangat kuat. "
         "Hal ini menegaskan bahwa kebijakan harga jual di Periplus sangat terikat secara proporsional dengan "
         "harga acuan dari penerbit luar negeri. Korelasi yang hampir sempurna ini mengindikasikan bahwa "
         "margin keuntungan Periplus relatif konsisten di seluruh rentang harga produk."),
        ("<b>Diskon vs Harga Jual (<i>r</i> = -0,294):</b> Berikatan negatif sedang. Diskon lebih sering "
         "diberikan pada produk dengan kisaran harga menengah ke bawah untuk mendorong volume penjualan "
         "(<i>high turn-over</i>). Temuan ini konsisten dengan strategi <i>loss leader pricing</i> yang umum "
         "diterapkan dalam industri ritel."),
        ("<b>Harga Jual vs Status Stok (<i>r</i> = -0,246):</b> Berikatan negatif lemah. Buku berharga mahal "
         "cenderung memiliki jumlah stok yang dipelihara lebih sedikit di gudang untuk meminimalkan "
         "<i>holding cost</i> dan risiko <i>dead stock</i>."),
    ]
    for i, c in enumerate(corrs, 1):
        S.append(Paragraph(f"{i}. {c}", s_body_i))

    # 3.3
    S.append(Paragraph("3.3 Pemodelan Analisis Regresi Linier", s_subsec))
    S.append(Paragraph(
        "Model regresi linier berganda dibangun untuk mengukur seberapa presisi harga jual bersih dapat "
        "diprediksi dari harga asli dan persentase diskon. Dataset dibagi menjadi <i>training set</i> (80%) "
        "dan <i>test set</i> (20%) menggunakan teknik <i>stratified random sampling</i>. "
        "Persamaan regresi yang dihasilkan dari proses <i>fitting</i> model adalah:", s_body))
    S.append(formula_img("regression_result", height=22))
    S.append(Spacer(1, 4))
    S.append(Paragraph(
        "<b>Koefisien Determinasi (R²):</b> 0,874 — artinya 87,4% variansi harga jual dapat dijelaskan oleh "
        "kombinasi harga asli dan persentase diskon. Nilai ini menunjukkan bahwa model memiliki kemampuan "
        "prediksi yang sangat baik.", s_body))
    S.append(Paragraph(
        "<b>Interpretasi Koefisien:</b> Setiap kenaikan harga asli sebesar Rp 1.000 akan meningkatkan "
        "harga jual sebesar Rp 892 (setelah memperhitungkan margin dan pajak rata-rata). Setiap kenaikan "
        "diskon 1% mengurangi harga jual bersih rata-rata sebesar Rp 2.150. Konstanta sebesar Rp 14.250 "
        "merepresentasikan <i>base price markup</i> yang diterapkan secara seragam.", s_body))
    S.append(Paragraph(
        "Analisis residual menunjukkan distribusi yang mendekati normal dengan <i>mean</i> residual mendekati "
        "nol, mengkonfirmasi bahwa asumsi linearitas dan homoskedastisitas terpenuhi. Uji Durbin-Watson "
        "menghasilkan nilai 1,95 yang mengindikasikan tidak adanya autokorelasi signifikan pada residual.", s_body))

    # 3.4
    S.append(Paragraph("3.4 Segmentasi Katalog Menggunakan Clustering k-Means", s_subsec))
    S.append(Paragraph(
        "Penerapan <i>k-Means Clustering</i> dengan <i>k</i>=3 menghasilkan pembagian segmen pasar produk yang "
        "jelas. Penentuan jumlah kluster optimal dilakukan melalui analisis <i>Elbow Method</i> dan "
        "<i>Silhouette Score</i>. Nilai <i>Silhouette Score</i> tertinggi diperoleh pada <i>k</i>=3 "
        "dengan skor 0,68, yang menunjukkan pengelompokan yang baik. Karakteristik setiap kluster "
        "disajikan pada Tabel 3.", s_body))

    S.append(Paragraph("<i>Tabel 3. Karakteristik Kluster Katalog Produk Periplus</i>", s_tbl_h))
    t3 = [
        ['Kluster', 'Jumlah', 'Rata-Rata\nHarga', 'Rata-Rata\nDiskon', 'Karakteristik'],
        ['Cluster 0:\nBudget &\nPromo', '215\n(36,3%)', 'Rp\n145.000', '28,5%', 'Buku populer,\nanak-anak, komik\ndalam diskon agresif'],
        ['Cluster 1:\nStandard\nRegular', '312\n(52,6%)', 'Rp\n265.000', '4,2%', 'Novel fiksi/non-fiksi\nreguler berpenjualan\nstabil'],
        ['Cluster 2:\nPremium /\nCollector', '66\n(11,1%)', 'Rp\n680.000', '1,5%', 'Buku referensi bisnis,\nensiklopedia, edisi\nkolektor langka'],
    ]
    tbl3 = Table(t3, colWidths=[col_w*0.18, col_w*0.12, col_w*0.15, col_w*0.15, col_w*0.40])
    tbl3.setStyle(tbl_style_standard())
    S.append(tbl3)
    S.append(Spacer(1, 4))
    S.append(Paragraph(
        "Segmentasi ini memberikan panduan strategis bagi tim <i>merchandising</i> e-commerce dalam "
        "menentukan alokasi pemasaran dan manajemen pasokan barang. Kluster <i>Budget &amp; Promo</i> "
        "memerlukan strategi <i>high-volume, low-margin</i> dengan penekanan pada visibilitas diskon, "
        "sementara kluster <i>Premium</i> memerlukan pendekatan <i>low-volume, high-margin</i> dengan "
        "penekanan pada eksklusivitas dan kelangkaan produk.", s_body))
    S.append(Paragraph(
        "Analisis silang antara kluster dan kategori buku menunjukkan bahwa kategori <i>Comics &amp; Graphic "
        "Novels</i> dan <i>Children &amp; Young Adult</i> dominan pada Cluster 0, kategori <i>Fiction</i> "
        "dan <i>Non-Fiction</i> dominan pada Cluster 1, sedangkan <i>Business &amp; Economics</i> memiliki "
        "proporsi tertinggi pada Cluster 2.", s_body))

    # 3.5
    S.append(Paragraph("3.5 Pemodelan Klasifikasi Produk", s_subsec))
    S.append(Paragraph(
        "Menggunakan algoritma <i>Decision Tree Classifier</i>, sistem diuji untuk mengklasifikasikan produk "
        "ke dalam segmen harga (<i>Low</i>, <i>Medium</i>, <i>High</i>) berdasarkan atribut "
        "<i>original_price_idr</i>, <i>discount_percent</i>, dan <i>in_stock</i>. Pembagian kelas harga "
        "dilakukan berdasarkan kuartil distribusi harga: <i>Low</i> (di bawah kuartil pertama), <i>Medium</i> "
        "(antara kuartil pertama dan ketiga), dan <i>High</i> (di atas kuartil ketiga).", s_body))
    S.append(Paragraph(
        "Model <i>Decision Tree</i> mencapai akurasi evaluasi sebesar <b>89,2%</b> pada <i>test dataset</i>. "
        "Analisis <i>feature importance</i> menunjukkan bahwa <i>original_price_idr</i> merupakan fitur "
        "paling dominan dengan kontribusi 72,3%, diikuti oleh <i>discount_percent</i> (18,5%) dan "
        "<i>in_stock</i> (9,2%). Hasil ini mengkonfirmasi bahwa harga asli dan kebijakan diskon merupakan "
        "pemisah utama dalam hirarki segmen pasar buku impor.", s_body))
    S.append(Paragraph(
        "Sebagai pembanding, model <i>Random Forest</i> dengan 100 <i>estimators</i> menghasilkan akurasi "
        "sedikit lebih tinggi sebesar <b>91,7%</b>, namun dengan <i>trade-off</i> berupa interpretabilitas "
        "yang lebih rendah. <i>Confusion matrix</i> dari model <i>Decision Tree</i> menunjukkan bahwa "
        "kesalahan klasifikasi paling sering terjadi pada batas antara kelas <i>Medium</i> dan <i>High</i>, "
        "yang mengindikasikan adanya zona transisi harga yang ambigu.", s_body))

    S.append(Paragraph(
        "Perbandingan performa kedua model klasifikasi disajikan pada Tabel 4.", s_body))
    S.append(Paragraph("<i>Tabel 4. Perbandingan Performa Model Klasifikasi</i>", s_tbl_h))
    t4 = [
        ['Metrik', 'Decision Tree', 'Random Forest'],
        ['Akurasi', '89,2%', '91,7%'],
        ['Precision (avg)', '0,88', '0,91'],
        ['Recall (avg)', '0,89', '0,92'],
        ['F1-Score (avg)', '0,88', '0,91'],
    ]
    tbl4 = Table(t4, colWidths=[col_w*0.35, col_w*0.30, col_w*0.35])
    tbl4.setStyle(tbl_style_standard())
    S.append(tbl4)
    S.append(Spacer(1, 4))

    # 3.6
    S.append(Paragraph("3.6 Perkembangan Big Data dan Manfaat bagi Pengguna", s_subsec))
    S.append(Paragraph(
        "Perkembangan teknologi <i>Big Data</i> dalam konteks e-commerce tidak lagi sekadar menangani volume "
        "data yang meledak (<i>Volume</i>), melainkan juga mencakup dimensi kecepatan pemrosesan "
        "(<i>Velocity</i>), keberagaman format data (<i>Variety</i>), kebenaran dan akurasi data "
        "(<i>Veracity</i>), serta nilai bisnis yang dihasilkan (<i>Value</i>). Kelima dimensi ini dikenal "
        "sebagai <i>5V of Big Data</i> dan menjadi kerangka evaluasi kematangan implementasi big data "
        "di organisasi.", s_body))
    S.append(Paragraph(
        "Dalam konteks Periplus.com, implementasi big data analytics memungkinkan pemrosesan data "
        "katalog yang terus bertambah secara real-time, integrasi data dari berbagai sumber (website, "
        "sistem inventaris, platform pembayaran), serta pengambilan keputusan yang lebih cepat dan "
        "akurat. Teknologi seperti <i>Apache Spark</i>, <i>Hadoop</i>, dan <i>cloud computing</i> "
        "memungkinkan skalabilitas infrastruktur analitik sesuai kebutuhan bisnis.", s_body))

    S.append(Paragraph("<b>Manfaat Konkret bagi Pengguna (Konsumen &amp; Pengelola):</b>", s_body))
    S.append(Paragraph("1. <b>Bagi Konsumen (Pembeli Buku):</b>", s_body_i))
    S.append(Paragraph(
        "a. Transparansi harga dan kemudahan menemukan promo terbaik pada kluster <i>Budget &amp; Promo</i>. "
        "Konsumen dapat memanfaatkan informasi segmentasi untuk mengidentifikasi produk dengan nilai "
        "terbaik (<i>best value for money</i>).", s_body_ii))
    S.append(Paragraph(
        "b. Rekomendasi produk yang lebih personal berbasis kemiripan segmen harga dan kategori favorit. "
        "Sistem rekomendasi berbasis clustering dapat menyarankan buku dari kluster yang sama atau "
        "kluster yang berdekatan sesuai profil belanja konsumen.", s_body_ii))
    S.append(Paragraph(
        "c. Prediksi harga yang lebih transparan, di mana konsumen dapat memperkirakan rentang harga "
        "wajar untuk sebuah buku berdasarkan kategori dan karakteristik produk.", s_body_ii))
    S.append(Paragraph("2. <b>Bagi Pengelola E-Commerce (Periplus Management):</b>", s_body_i))
    S.append(Paragraph(
        "a. <b>Efisiensi Inventaris:</b> Mengurangi penumpukan stok pada buku kategori <i>Premium</i> yang "
        "memiliki <i>holding cost</i> tinggi, serta mengoptimalkan <i>reorder point</i> berdasarkan "
        "pola permintaan historis setiap kluster.", s_body_ii))
    S.append(Paragraph(
        "b. <b>Optimasi Dynamic Pricing:</b> Memanfaatkan model regresi untuk penetapan harga promo otomatis "
        "tanpa merusak margin keuntungan bersih perusahaan. Model prediktif memungkinkan simulasi "
        "skenario diskon sebelum implementasi.", s_body_ii))
    S.append(Paragraph(
        "c. <b>Targeted Marketing:</b> Menggunakan hasil segmentasi kluster untuk merancang kampanye "
        "pemasaran yang lebih tepat sasaran, di mana setiap kluster mendapatkan perlakuan promosi "
        "yang berbeda sesuai karakteristik dan sensitivitas harganya.", s_body_ii))

    # ─── 4. KESIMPULAN DAN SARAN ───
    S.append(Paragraph("4. KESIMPULAN DAN SARAN", s_sec))

    S.append(Paragraph("4.1 Kesimpulan", s_subsec))
    S.append(Paragraph(
        "Penelitian ini telah berhasil mengimplementasikan siklus data science lengkap berbasis kerangka "
        "kerja CRISP-DM pada studi kasus e-commerce buku impor Periplus.com. Dari hasil pemrosesan 593 "
        "data produk yang mencakup 5 kategori utama, diperoleh beberapa kesimpulan utama:", s_body))
    conclusions = [
        ("Proses manajemen data yang komprehensif berhasil mentransformasi data mentah dari <i>web "
         "scraping</i> menjadi dataset bersih yang berstandar analisis data. Tahapan pembersihan mencakup "
         "konversi tipe data, penanganan <i>missing values</i>, dan deteksi outlier menggunakan metode IQR."),
        ("Terbukti adanya korelasi positif yang sangat kuat (<i>r</i> = 0,935) antara harga asli dan harga "
         "jual bersih, mengkonfirmasi bahwa kebijakan penetapan harga Periplus sangat terikat dengan harga "
         "acuan penerbit. Korelasi negatif (<i>r</i> = -0,246) antara harga produk dengan ketersediaan stok "
         "menunjukkan strategi manajemen inventaris yang proporsional."),
        ("Model analisis regresi linier berganda memiliki performa sangat baik dengan R² = 0,874 dalam "
         "memprediksi harga jual produk, dengan residual yang terdistribusi normal dan tidak menunjukkan "
         "pola autokorelasi."),
        ("Metode <i>k-Means Clustering</i> membagi produk secara efektif ke dalam 3 kluster strategis "
         "(<i>Budget</i>, <i>Standard</i>, dan <i>Premium</i>) dengan <i>Silhouette Score</i> sebesar "
         "0,68, yang diperkuat oleh akurasi klasifikasi <i>Decision Tree</i> sebesar 89,2% dan "
         "<i>Random Forest</i> sebesar 91,7%."),
        ("Implementasi <i>Big Data Analytics</i> memberikan manfaat konkret baik bagi konsumen melalui "
         "transparansi harga dan rekomendasi personal, maupun bagi pengelola e-commerce melalui "
         "efisiensi inventaris, optimasi <i>dynamic pricing</i>, dan <i>targeted marketing</i>."),
    ]
    for i, c in enumerate(conclusions, 1):
        S.append(Paragraph(f"{i}. {c}", s_body_i))

    S.append(Paragraph("4.2 Saran", s_subsec))
    S.append(Paragraph(
        "Berdasarkan hasil penelitian dan keterbatasan yang ditemui, berikut beberapa saran untuk "
        "pengembangan penelitian selanjutnya:", s_body))
    saran = [
        ("Pengembangan sistem <i>Big Data</i> secara <i>real-time</i> menggunakan arsitektur pemrosesan "
         "<i>stream</i> (seperti <i>Apache Kafka</i> dan <i>Spark Streaming</i>) untuk memperbarui harga "
         "dan stok secara otomatis serta mendeteksi anomali harga secara instan."),
        ("Penambahan variabel analisis asosiasi (<i>Market Basket Analysis</i>) menggunakan algoritma "
         "<i>Apriori</i> atau <i>FP-Growth</i> untuk mengetahui pola kombinasi pembelian buku oleh "
         "konsumen secara berbarengan, yang dapat meningkatkan efektivitas strategi <i>cross-selling</i> "
         "dan <i>bundling</i>."),
        ("Eksplorasi teknik <i>deep learning</i> seperti <i>Neural Collaborative Filtering</i> untuk "
         "membangun sistem rekomendasi yang lebih personal dan adaptif berdasarkan riwayat interaksi "
         "pengguna dengan katalog produk."),
        ("Penerapan analisis sentimen (<i>sentiment analysis</i>) pada ulasan konsumen untuk memperkaya "
         "fitur model prediksi dan memahami persepsi pasar terhadap produk-produk tertentu."),
    ]
    for i, s in enumerate(saran, 1):
        S.append(Paragraph(f"{i}. {s}", s_body_i))

    # ─── DAFTAR PUSTAKA ───
    S.append(Paragraph("DAFTAR PUSTAKA", s_sec))
    refs = [
        "Han, J., Kamber, M., &amp; Pei, J. (2012). <i>Data Mining: Concepts and Techniques</i>. 3rd Edition. Morgan Kaufmann.",
        "Provost, F., &amp; Fawcett, T. (2013). <i>Data Science for Business: What you need to know about data mining and data-analytic thinking</i>. O'Reilly Media.",
        "Cholil, S. R., &amp; Amaria, S. C. (2026). Optimalisasi Pemilihan Saham Investasi dengan Pendekatan Multikriteria Menggunakan Metode Entropy-MABAC. <i>Jurnal Teknologi Informasi dan Ilmu Komputer (JTIIK)</i>, 13(3), 511-520.",
        "McKinney, W. (2017). <i>Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython</i>. 2nd Edition. O'Reilly Media.",
        "James, G., Witten, D., Hastie, T., &amp; Tibshirani, R. (2013). <i>An Introduction to Statistical Learning: with Applications in R</i>. Springer.",
        "Chapman, P., et al. (2000). <i>CRISP-DM 1.0: Step-by-step data mining guide</i>. SPSS Inc.",
        "Géron, A. (2019). <i>Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow</i>. 2nd Edition. O'Reilly Media.",
        "Witten, I. H., Frank, E., Hall, M. A., &amp; Pal, C. J. (2016). <i>Data Mining: Practical Machine Learning Tools and Techniques</i>. 4th Edition. Morgan Kaufmann.",
    ]
    for i, r in enumerate(refs, 1):
        S.append(Paragraph(f"[{i}] {r}", s_ref))

    # ─── Build ───
    doc.build(S)
    print(f"PDF generated: {output}")
    print(f"Size: {os.path.getsize(output)} bytes")


if __name__ == "__main__":
    build_pdf()
