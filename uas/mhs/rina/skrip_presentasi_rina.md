# Skrip Presentasi Jurnal/Artikel — Rina Mardiana

> Contekan untuk recording Zoom. Bacanya natural, jangan kayak baca teks.

---

## Slide 1 — Title

"Assalamualaikum warahmatullahi wabarakatuh. Selamat pagi/siang Bapak/Ibu dosen dan teman-teman sekalian."

"Perkenalkan, nama saya Rina Mardiana, NIM 250401020151, dari Program Studi PJJ Informatika S1, Universitas Siber Asia."

"Pada kesempatan ini, saya akan mempresentasikan artikel ilmiah kami yang berjudul Optimalisasi Strategi Penjualan E-Commerce Buku Impor Periplus Menggunakan Pendekatan Data Science."

"Artikel ini dikerjakan bersama partner saya, Sutan Gading Fadhillah Nasution. Saya akan fokus membahas bagian metodologi, analisis korelasi Pearson, klasifikasi, dan big data. Sementara Gading sudah mempresentasikan bagian web scraping, regresi linier, dan clustering di presentasi terpisah."

---

## Slide 2 — Latar Belakang

"Mengapa kami mengambil topik ini?"

"Industri e-commerce buku di Indonesia tumbuh pesat. Nilai transaksi e-commerce nasional sudah mencapai lebih dari Rp 500 triliun pada tahun 2024. Periplus.com menjadi salah satu platform utama distribusi buku internasional di Indonesia."

"Tantangan yang dihadapi: bagaimana menetapkan harga yang kompetitif, melakukan segmentasi produk yang tepat, dan mengelola inventaris secara efisien."

"Beberapa penelitian terdahulu mendukung pendekatan ini. Han, Kamber, dan Pei pada 2012 menunjukkan bahwa data mining bisa mengungkap pola tersembunyi dalam dataset besar. Provost dan Fawcett pada 2013 menekankan pentingnya data-analytic thinking. Dan McKinney pada 2017 mendemonstrasikan bahwa ekosistem Python sudah menjadi standar industri untuk analisis data."

---

## Slide 3 — Metodologi CRISP-DM

"Metodologi penelitian kami mengacu pada CRISP-DM, yaitu Cross-Industry Standard Process for Data Mining."

"Ini kerangka kerja yang paling banyak digunakan dalam proyek data science. Terdiri dari 6 tahapan yang saling terhubung dan bersifat iteratif."

"Tahap pertama: Business Understanding — memahami konteks bisnis e-commerce buku impor."
"Kedua: Data Acquisition — pengumpulan data melalui web scraping, menghasilkan 1.514 data mentah."
"Ketiga: Data Preparation — pembersihan dan validasi, menghasilkan 1.322 data bersih."
"Keempat: Modeling & Analytics — penerapan korelasi, regresi, clustering, dan klasifikasi."
"Kelima: Evaluation — evaluasi performa setiap model."
"Dan keenam: Deployment — implementasi hasil analisis untuk rekomendasi bisnis."

---

## Slide 4 — Data Management & Cleaning

"Tahap data management sangat krusial. Prinsipnya: garbage in, garbage out — kualitas hasil analisis sangat bergantung pada kualitas data."

"Dari 1.514 data mentah, kami mengeliminasi 192 rekaman karena duplikasi atau nilai tidak valid. Proses cleaning mencakup:"

"Pertama, konversi tipe data — menghapus simbol Rp dan titik ribuan, mengubah ke format numerik float64."

"Kedua, standarisasi teks pada kolom title dan author."

"Ketiga, deteksi outlier menggunakan metode IQR. Outlier tidak dihapus, tapi diberi flag untuk analisis terpisah. Bisa dilihat di grafik box plot di kanan."

"Keempat, penanganan missing values dengan teknik forward fill dan median imputation."

"Hasilnya: 1.322 baris data bersih tanpa null atau NaN."

---

## Slide 5 — Analisis Korelasi Pearson

"Sekarang masuk ke analisis utama pertama saya: korelasi Pearson."

"Di sebelah kiri adalah heatmap korelasi antar variabel numerik. Ada tiga temuan utama:"

"Pertama, korelasi antara harga asli dan harga jual: r = 0,962. Ini positif sangat kuat, mendekati sempurna. Artinya kebijakan harga Periplus sangat terikat dengan harga dari penerbit."

"Kedua, korelasi diskon terhadap harga jual: r = -0,307. Negatif sedang. Diskon lebih sering diberikan pada produk harga menengah ke bawah."

"Ketiga, korelasi harga terhadap ketersediaan stok: r = -0,429. Negatif sedang. Buku mahal cenderung stoknya lebih sedikit."

---

## Slide 6 — Visualisasi Korelasi

"Di slide ini bisa dilihat scatter plot yang memvisualisasikan hubungan antar variabel secara lebih detail."

"Scatter plot harga asli versus harga jual menunjukkan pola linear yang sangat jelas — titik-titik data hampir membentuk garis lurus. Ini mengkonfirmasi korelasi r = 0,962 yang sangat kuat."

---

## Slide 7 — Interpretasi Korelasi

"Apa implikasi bisnis dari temuan korelasi ini?"

"Korelasi r = 0,962 menunjukkan bahwa margin keuntungan Periplus relatif konsisten di seluruh rentang harga. Mereka tidak mengambil margin lebih besar di buku mahal."

"Korelasi negatif diskon vs harga menunjukkan strategi loss leader pricing — mendiskon produk murah untuk mendorong volume penjualan."

"Dan korelasi negatif harga vs stok menunjukkan manajemen inventaris yang proporsional. Buku mahal distok sedikit untuk meminimalkan holding cost dan risiko dead stock."

---

## Slide 8 — Klasifikasi

"Analisis utama kedua saya: klasifikasi menggunakan Decision Tree dan Random Forest."

"Kami mengklasifikasikan produk ke dalam 3 kelas harga: Low, Medium, dan High, berdasarkan distribusi kuartil."

"Decision Tree menghasilkan akurasi 98,1%. Random Forest sedikit lebih tinggi di 98,5%."

"Yang menarik adalah feature importance. Original price mendominasi dengan 74,8%, diikuti discount percent 25,2%, dan in_stock 0,0%. Artinya harga asli adalah pemisah utama antar kelas harga."

"Dari tabel metrik: precision, recall, dan F1-score semuanya di atas 0,98 untuk kedua model. Ini menunjukkan klasifikasi yang sangat akurat dan reliable."

---

## Slide 9 — Big Data 5V & Manfaat

"Terakhir, saya akan membahas konteks Big Data dan manfaatnya."

"Implementasi big data dalam e-commerce mencakup 5 dimensi: Volume — ribuan produk dan transaksi; Velocity — update katalog real-time; Variety — berbagai format data; Veracity — jaminan kualitas data; dan Value — menghasilkan actionable insights."

"Manfaat bagi konsumen: transparansi harga, rekomendasi personal berbasis clustering, dan prediksi rentang harga wajar."

"Manfaat bagi pengelola: efisiensi inventaris dengan optimasi reorder point, dynamic pricing berbasis model prediksi, dan targeted marketing per segmen kluster."

---

## Slide 10 — Kesimpulan & Saran

"Untuk kesimpulan dari bagian saya:"

"Korelasi sangat kuat antara harga asli dan harga jual dengan r = 0,962."

"Klasifikasi menghasilkan akurasi sangat tinggi — Decision Tree 98,1% dan Random Forest 98,5%. Feature importance mengkonfirmasi harga asli sebagai faktor dominan."

"Big Data 5V memberikan framework evaluasi untuk implementasi analytics di e-commerce."

"Untuk saran pengembangan: pertama, sistem real-time dengan Apache Kafka dan Spark Streaming. Kedua, Market Basket Analysis untuk strategi cross-selling. Ketiga, deep learning untuk sistem rekomendasi. Dan keempat, sentiment analysis pada ulasan konsumen."

---

## Slide 11 — Terima Kasih

"Demikian presentasi dari saya. Terima kasih atas perhatian Bapak/Ibu dosen dan teman-teman sekalian."

"Wassalamualaikum warahmatullahi wabarakatuh."
