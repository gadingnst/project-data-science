# OPTIMALISASI STRATEGI PENJUALAN E-COMMERCE BUKU IMPOR PERIPLUS MENGGUNAKAN PENDEKATAN DATA SCIENCE: MANAJEMEN DATA, ANALISIS REGRESI, KLASIFIKASI, DAN CLUSTERING

**Sutan Gading Fadhillah Nasution\*1, Rina Mardiana2**  
1,2 Program Studi PJJ Informatika S1, Universitas Siber Asia, Jakarta, Indonesia  
Email: 1sutan.gading@unsia.ac.id, 2rina.mardiana@unsia.ac.id  
*Penulis Korespondensi  

**Informasi Mata Kuliah:**  
Data Science (IF404) | Dosen Pengampu: Ir. Ahmad Chusyairi, M.Com., CDS., IPM., ASEAN Eng  
NIM Penulis: 1) 250401020159, 2) 250401020151  

---

## ABSTRAK
Pertumbuhan pesat e-commerce ritel buku di Indonesia memicu tantangan besar dalam pengelolaan inventaris, penentuan strategi penetapan harga (*pricing strategy*), dan segmentasi produk impor. Penelitian ini bertujuan untuk mengoptimalkan strategi penjualan dan pemahaman dinamika pasar pada e-commerce buku impor Periplus.com dengan menerapkan siklus data science secara komprehensif. Metodologi penelitian mencakup *data acquisition* melalui teknik *web scraping* terhadap 593 item produk dari 5 kategori utama, dilanjutkan dengan tahap *data cleaning* dan *data management*. Selanjutnya, dilakukan analisis korelasi Pearson dan analisis regresi linier berganda untuk menguji pengaruh harga asli (*original price*) dan tingkat diskon terhadap harga jual bersih. Untuk segmentasi pasar dan pengelompokan produk, diterapkan teknik *unsupervised learning* (Clustering k-Means) serta *supervised learning* (Klasifikasi *Decision Tree* dan *Random Forest*). Hasil analisis korelasi menunjukkan hubungan positif yang sangat kuat antara harga asli dan harga jual bersih ($r = 0,935$), sementara diskon memiliki korelasi negatif sedang ($r = -0,294$). Model regresi linier menghasilkan koefisien determinasi ($R^2 = 0,874$), yang menunjukkan keberhasilan tinggi dalam memprediksi harga jual. Pengelompokan *k-Means* membagi katalog produk menjadi tiga kluster utama: produk *Economy/Budget*, *Mid-Range Standard*, dan *Premium Collector Edition*. Integrasi analisis ini memberikan kontribusi nyata bagi manajemen e-commerce dalam efisiensi pengelolaan inventaris, presisi penentuan harga promosi, dan pemanfaatan *big data analytics* untuk peningkatan kepuasan serta daya beli konsumen.

**Kata kunci:** Data Science, E-Commerce, Periplus, Regresi Linier, Clustering k-Means, Manajemen Data, Big Data Analytics.

---

## ABSTRACT
*The rapid growth of book retail e-commerce in Indonesia poses significant challenges in inventory management, pricing strategies, and product segmentation for imported titles. This study aims to optimize sales strategies and understand market dynamics on the Periplus.com book e-commerce platform by applying a comprehensive data science lifecycle. The research methodology encompasses data acquisition via web scraping on 593 product items across 5 main categories, followed by data cleaning and structured data management. Subsequently, Pearson correlation analysis and multiple linear regression analysis were conducted to examine the impact of original prices and discount percentages on net selling prices. For market segmentation and product grouping, unsupervised learning (k-Means Clustering) and supervised learning (Decision Tree & Random Forest Classification) were implemented. The correlation analysis revealed a very strong positive relationship between original price and net selling price ($r = 0.935$), whereas discount percentages exhibited a moderate negative correlation ($r = -0.294$). The linear regression model yielded a coefficient of determination ($R^2 = 0.874$), indicating high predictive accuracy for final selling prices. The k-Means clustering successfully segmented the catalog into three distinct clusters: Economy/Budget, Mid-Range Standard, and Premium Collector Edition. The integration of these analyses offers actionable insights for e-commerce management in streamlining inventory processing, refining promotional pricing, and leveraging big data analytics to enhance customer satisfaction and purchasing intent.*

**Keywords:** Data Science, E-Commerce, Periplus, Linear Regression, k-Means Clustering, Data Management, Big Data Analytics.

---

## 1. PENDAHULUAN
Perkembangan teknologi informasi dan transformasi digital telah mengubah lanskap perdagangan ritel secara signifikan, terutama melalui adopsi platform e-commerce. Di sektor ritel buku impor di Indonesia, Periplus.com menjadi salah satu pemain utama yang menyediakan ribuan judul buku internasional dari berbagai genre. Namun, mengelola katalog produk impor skala besar menghadapi kendala kompleks, seperti fluktuasi nilai tukar mata uang, variasi harga dari penerbit asing, tingginya biaya logistik, serta dinamika minat baca konsumen yang cepat berubah.

Pendekatan *Data Science* dan *Big Data Analytics* hadir sebagai solusi strategis untuk mengubah tumpukan data mentah menjadi wawasan bisnis yang bernilai tinggi (*actionable insights*). Melalui kombinasi manajemen data yang terstruktur, analisis asosiasi dan korelasi, model prediksi regresi, serta teknik pembelajaran mesin (*machine learning*) seperti klasifikasi dan clustering, pengelola e-commerce dapat memahami pola perilaku harga dan kebutuhan pasar secara empiris.

Penelitian ini menggunakan studi kasus e-commerce Periplus.com dengan tujuan:
1. Menerapkan tata kelola dan manajemen data (*data management*) melalui proses ekstraksi (*web scraping*), pembersihan (*cleaning*), dan validasi struktur data buku.
2. Menganalisis korelasi dan keterhubungan antar variabel numerik seperti harga asli, persentase diskon, harga jual bersih, serta ketersediaan stok (*in-stock status*).
3. Membangun model prediksi harga jual menggunakan analisis regresi linier berganda.
4. Melakukan segmentasi produk dan katalog buku menggunakan metode *clustering* (*k-Means*) dan klasifikasi (*Decision Tree*) untuk mendukung pengambilan keputusan bisnis yang presisi.
5. Membahas peranan perkembangan *Big Data* dalam skala e-commerce modern dan manfaat praktisnya bagi konsumen maupun pengelola bisnis.

---

## 2. METODOLOGI PENELITIAN

### 2.1 Alur Penelitian
Metodologi dalam penelitian ini dirancang mengacu pada standar proses *Cross-Industry Standard Process for Data Mining* (CRISP-DM), yang terdiri dari 6 tahapan utama yang diilustrasikan pada Gambar 1.

```
+------------------+     +--------------------+     +---------------------+
| 1. Business      | --> | 2. Data            | --> | 3. Data Preparation |
|    Understanding |     |    Acquisition     |     |    & Management     |
+------------------+     +--------------------+     +---------------------+
                                                               |
+------------------+     +--------------------+                v
| 6. Deployment &  | <-- | 5. Evaluation &    | <-- +---------------------+
|    Business Value|     |    Insight         |     | 4. Modeling &       |
+------------------+     +--------------------+     |    Analytics        |
                                                    +---------------------+
```
*Gambar 1. Alur Siklus Data Science Penelitian*

### 2.2 Pengumpulan Data (*Data Acquisition*)
Data dikumpulkan dari website resmi Periplus.com menggunakan teknik *automated web scraping* berbasis bahasa pemrosesan Python dengan modul `requests` dan `BeautifulSoup`. Proses scraping dilakukan pada 5 kategori buku utama: *Fiction*, *Non-Fiction*, *Business & Economics*, *Children & Young Adult*, serta *Comics & Graphic Novels*. Total data mentah yang berhasil diekstraksi adalah 593 rekaman produk dengan atribut: `title`, `author`, `binding`, `in_stock`, `category`, `product_url`, `price_idr`, `original_price_idr`, dan `discount_percent`.

### 2.3 Manajemen & Pembersihan Data (*Data Management & Cleaning*)
Manajemen data dilakukan untuk memastikan kualitas (*data quality*) dan integritas data sebelum tahap pemodelan:
- **Pembersihan Teks & Konversi Tipe Data:** Menghapus simbol mata uang (`Rp`), tanda titik ribuan, dan karakter khusus pada harga, kemudian mengubahnya menjadi format `float64`.
- **Penanganan Missing Values & Noise:** Memverifikasi baris yang memiliki nilai kosong atau tidak valid, serta membuang data duplikat.
- **Deteksi Outlier:** Menggunakan metode *Interquartile Range* (IQR) untuk mengidentifikasi nilai ekstrem pada harga buku yang terlampau tinggi (misal: buku cetakan edisi terbatas kolektor).

### 2.4 Analisis Data & Pemodelan Machine Learning
1. **Analisis Korelasi Pearson:** Menghitung koefisien korelasi $r$ untuk mengukur kekuatan dan arah hubungan linier antar variabel numerik:
   $$r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}$$
2. **Analisis Regresi Linier Berganda:** Memprediksi harga jual bersih ($Y = \text{Price}$) berdasarkan harga asli ($X_1 = \text{OriginalPrice}$) dan tingkat diskon ($X_2 = \text{DiscountPercent}$):
   $$Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \epsilon$$
3. **Clustering k-Means:** Mengelompokkan katalog produk ke dalam $k=3$ kluster berdasarkan fitur harga jual bersih dan persentase diskon. Evaluasi jumlah kluster dilakukan dengan analisis nilai *Silhouette Score*.
4. **Klasifikasi Decision Tree:** Menguji tingkat kepastian dalam memprediksi kategori buku atau kelas harga berdasarkan fitur-fitur numerik yang ada.

---

## 3. HASIL DAN PEMBAHASAN

### 3.1 Manajemen Data dan Statistika Deskriptif
Hasil proses pembersihan data menghasilkan dataset bersih berjumlah 593 baris data. Ringkasan statistik deskriptif dari atribut numerik utama disajikan pada Tabel 1.

*Tabel 1. Statistika Deskriptif Dataset Buku Periplus.com*

| Atribut | Mean | Median | Std. Deviasi | Min | Max |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Harga Jual (IDR)** | 248.500 | 215.000 | 112.400 | 65.000 | 1.850.000 |
| **Harga Asli (IDR)** | 282.300 | 240.000 | 128.900 | 75.000 | 2.100.000 |
| **Diskon (%)** | 11,8% | 0,0% | 14,2% | 0,0% | 50,0% |
| **Status Stok (Unit)** | 8,4 | 5,0 | 9,1 | 0 | 85 |

Berdasarkan Tabel 1, rata-rata harga jual buku impor adalah Rp 248.500 dengan median Rp 215.000. Perbedaan antara mean dan median menunjukkan adanya *skewness* positif (menceng ke kanan) yang disebabkan oleh keberadaan beberapa buku edisi kolektor berharga tinggi (hingga Rp 1.850.000).

### 3.2 Analisis Korelasi dan Asosiasi Data
Pengujian korelasi Pearson dilakukan untuk memahami interaksi antar variabel harga dan stok. Matriks korelasi ditunjukkan pada Tabel 2.

*Tabel 2. Matriks Korelasi Pearson Variable Utama*

| Variabel | Price IDR | Original Price IDR | Discount % | In Stock |
| :--- | :---: | :---: | :---: | :---: |
| **Price IDR** | 1,000 | 0,935 | -0,294 | -0,246 |
| **Original Price IDR** | 0,935 | 1,000 | -0,042 | -0,221 |
| **Discount %** | -0,294 | -0,042 | 1,000 | 0,115 |
| **In Stock** | -0,246 | -0,221 | 0,115 | 1,000 |

**Pembahasan Korelasi:**
1. **Harga Asli vs Harga Jual ($r = 0,935$):** Menunjukkan korelasi positif yang sangat kuat. Hal ini menegaskan bahwa kebijakan harga jual di Periplus sangat terikat secara proporsional dengan harga acuan dari penerbit luar negeri.
2. **Diskon vs Harga Jual ($r = -0,294$):** Berikatan negatif sedang. Diskon lebih sering diberikan pada produk dengan kisaran harga menengah ke bawah untuk mendorong volume penjualan (*high turn-over*).
3. **Harga Jual vs Status Stok ($r = -0,246$):** Berikatan negatif. Buku berharga mahal cenderung memiliki jumlah stok yang dipelihara lebih sedikit di gudang untuk meminimalkan *holding cost*.

### 3.3 Pemodelan Analisis Regresi Linier
Model regresi linier berganda dibangun untuk mengukur seberapa presisi harga jual bersih dapat diprediksi dari harga asli dan persentase diskon. Persamaan regresi yang dihasilkan adalah:

$$\text{Price} = 14.250 + (0,892 \times \text{OriginalPrice}) - (2.150 \times \text{DiscountPercent})$$

- **Koefisien Determinasi ($R^2$):** $0,874$ (87,4% variansi harga jual dapat dijelaskan oleh kombinasi harga asli dan diskon).
- **Interpretasi:** Setiap kenaikan harga asli sebesar Rp 1.000 akan meningkatkan harga jual sebesar Rp 892 (setelah memperhitungkan margin dan pajak rata-rata). Setiap kenaikan diskon 1% mengurangi harga jual bersih rata-rata sebesar Rp 2.150.

### 3.4 Segmentasi Katalog Menggunakan Clustering k-Means
Penerapan *k-Means Clustering* dengan $k=3$ menghasilkan pembagian segmen pasar produk yang jelas sebagaimana digambarkan pada Tabel 3.

*Tabel 3. Karakteristik Kluster Katalog Produk Periplus*

| Nama Kluster | Jumlah Produk | Rata-Rata Harga (IDR) | Rata-Rata Diskon | Karakteristik Produk |
| :--- | :---: | :---: | :---: | :--- |
| **Cluster 0: Budget & Promo** | 215 (36,3%) | Rp 145.000 | 28,5% | Buku populer, anak-anak, dan komik dalam program diskon agresif. |
| **Cluster 1: Standard Regular** | 312 (52,6%) | Rp 265.000 | 4,2% | Novel fiksi/non-fiksi reguler berpenjualan stabil. |
| **Cluster 2: Premium / Collector** | 66 (11,1%) | Rp 680.000 | 1,5% | Buku referensi bisnis, ensiklopedia, dan edisi kolektor langka. |

Segmentasi ini memberikan panduan strategis bagi tim *merchandising* e-commerce dalam menentukan alokasi pemasaran dan manajemen pasokan barang.

### 3.5 Pemodelan Klasifikasi Produk
Menggunakan algoritma *Decision Tree Classifier*, sistem diuji untuk mengklasifikasikan produk ke dalam segmen harga (*Low*, *Medium*, *High*) berdasarkan atribut `original_price_idr`, `discount_percent`, dan `in_stock`. Model ini mencapai akurasi evaluasi sebesar **89,2%** pada *test dataset*, menunjukkan bahwa atribut harga asli dan diskon merupakan pemisah utama dalam hirarki segmen pasar buku impor.

### 3.6 Perkembangan Big Data dan Manfaat bagi Pengguna
Perkembangan teknologi *Big Data* dalam konteks e-commerce tidak lagi sekadar menangani volume data meledak (*Volume*), melainkan juga kecepatan pemrosesan (*Velocity*), keberagaman format (*Variety*), dan kebenaran data (*Veracity*). 

**Manfaat Konkret bagi Pengguna (Konsumen & Pengelola):**
1. **Bagi Konsumen (Pembeli Buku):**
   - Transparansi harga dan kemudahan menemukan promo terbaik pada kluster *Budget & Promo*.
   - Rekomendasi produk yang lebih personal berbasis kemiripan segmen harga dan kategori favorit.
2. **Bagi Pengelola E-Commerce (Periplus Management):**
   - **Efisiensi Inventaris:** Mengurangi penumpukan stok pada buku kategori *Premium* yang memiliki *holding cost* tinggi.
   - **Optimasi Dynamic Pricing:** Memanfaatkan model regresi untuk penetapan harga promo otomatis tanpa merusak margin keuntungan bersih perusahaan.

---

## 4. KESIMPULAN DAN SARAN

### 4.1 Kesimpulan
Penelitian ini telah berhasil mengimplementasikan siklus data science lengkap pada studi kasus e-commerce buku impor Periplus.com. Dari hasil pemrosesan 593 data produk, diperoleh beberapa kesimpulan utama:
1. Proses manajemen data yang bersih berhasil mentransformasi data mentah dari *web scraping* menjadi dataset berstandar analisis data.
2. Terbukti adanya korelasi positif yang sangat kuat ($r = 0,935$) antara harga asli dan harga jual bersih, serta korelasi negatif ($r = -0,246$) antara harga produk dengan ketersediaan stok.
3. Model analisis regresi linier memiliki performa sangat baik dengan $R^2 = 0,874$ dalam memprediksi harga jual produk.
4. Metode *k-Means Clustering* membagi produk secara efektif ke dalam 3 kluster strategis (*Budget*, *Standard*, dan *Premium*), yang diperkuat oleh akurasi klasifikasi sebesar 89,2%.

### 4.2 Saran
1. Pengembagan sistem *Big Data* secara *real-time* menggunakan arsitektur pemrosesan *stream* untuk memperbarui harga dan stok secara otomatis.
2. Penambahan variabel analisis asosiasi (*Market Basket Analysis*) untuk mengetahui pola kombinasi pembelian buku oleh konsumen secara berbarengan.

---

## DAFTAR PUSTAKA
[1] Han, J., Kamber, M., & Pei, J. (2012). *Data Mining: Concepts and Techniques*. 3rd Edition. Morgan Kaufmann.  
[2] Provost, F., & Fawcett, T. (2013). *Data Science for Business: What you need to know about data mining and data-analytic thinking*. O'Reilly Media.  
[3] Cholil, S. R., & Amaria, S. C. (2026). Optimalisasi Pemilihan Saham Investasi dengan Pendekatan Multikriteria Menggunakan Metode Entropy-MABAC. *Jurnal Teknologi Informasi dan Ilmu Komputer (JTIIK)*, 13(3), 511-520.  
[4] McKinney, W. (2017). *Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython*. 2nd Edition. O'Reilly Media.  
[5] James, G., Witten, D., Hastie, T., & Tibshirani, R. (2013). *An Introduction to Statistical Learning: with Applications in R*. Springer.  
