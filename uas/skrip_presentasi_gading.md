# Skrip Presentasi Proyek — Sutan Gading Fadhillah Nasution

> Contekan untuk recording Zoom. Bacanya natural, jangan kayak baca teks.

---

## Slide 1 — Title

"Assalamualaikum warahmatullahi wabarakatuh. Selamat pagi/siang Bapak/Ibu dosen dan teman-teman sekalian."

"Perkenalkan, nama saya Sutan Gading Fadhillah Nasution, NIM 250401020159, dari Program Studi PJJ Informatika S1, Universitas Siber Asia."

"Pada kesempatan ini, saya akan mempresentasikan proyek data science kami yang berjudul Analisis Data E-Commerce Buku Impor Periplus.com Dengan Pendekatan Data Science."

"Proyek ini dikerjakan bersama partner saya, Rina Mardiana. Saya akan fokus membahas bagian web scraping, regresi linier, dan k-Means clustering. Sementara Rina akan mempresentasikan bagian analisis korelasi, klasifikasi, dan big data di presentasi terpisah."

---

## Slide 2 — Overview Proyek

"Sekilas tentang proyek kami. Studi kasus yang kami ambil adalah platform e-commerce buku impor Periplus.com."

"Tujuannya adalah mengekstrak business insights dari data katalog produk mereka. Pipeline yang kami bangun bersifat end-to-end, mulai dari scraping data dari website, cleaning, analisis, sampai modeling dan menghasilkan insights bisnis."

"Tech stack yang kami gunakan: Python sebagai bahasa utama, Pandas untuk data management, Scikit-learn untuk machine learning, Matplotlib untuk visualisasi, dan BeautifulSoup untuk web scraping."

---

## Slide 3 — Web Scraping

"Tahap pertama adalah data acquisition melalui web scraping."

"Kami melakukan scraping pada 8 kategori buku utama di Periplus.com: Fiction & Literature, Business & Self-Help, Children's Books, Computer & IT, Biographies & Memoirs, Arts & Photography, Cooking & Food, dan Health & Fitness."

"Total data mentah yang berhasil diekstraksi adalah 1.514 rekaman. Setiap rekaman memiliki 9 atribut: title, author, binding, in_stock, category, product URL, harga jual, harga asli, dan persentase diskon."

"Proses scraping dilakukan dengan mekanisme rate limiting dan user-agent rotation agar menghormati kebijakan akses website."

---

## Slide 4 — Statistik Deskriptif & Distribusi

"Setelah proses cleaning yang akan dibahas oleh Rina, kami mendapatkan 1.322 data bersih."

"Dari statistik deskriptif, rata-rata harga jual buku impor adalah Rp 376.616 dengan median Rp 299.000. Perbedaan mean dan median ini menunjukkan distribusi yang positif skewed, artinya ada beberapa buku kolektor berharga sangat tinggi yang menarik rata-rata ke atas."

"Standar deviasi cukup besar, Rp 263.249, menunjukkan variasi harga yang lebar. Rentang harga mulai dari Rp 29.400 sampai hampir Rp 2 juta."

"Di grafik kiri bisa dilihat distribusi per kategori cukup merata, kecuali Health & Fitness yang jumlahnya lebih sedikit. Di kanan adalah distribusi harga yang memang skewed ke kanan."

---

## Slide 5 — Regresi Linier Berganda

"Sekarang masuk ke analisis utama pertama saya: regresi linier berganda."

"Model ini dibangun untuk memprediksi harga jual bersih berdasarkan dua variabel: harga asli dari penerbit dan persentase diskon. Dataset dibagi 80% training dan 20% testing."

"Hasilnya sangat bagus. R² score yang kami dapatkan adalah 0,990 — artinya 99% variansi harga jual bisa dijelaskan oleh model ini. Uji Durbin-Watson menghasilkan 1,94, yang berarti tidak ada autokorelasi signifikan pada residual."

"Persamaan regresinya: Harga Jual = 14.971 + 0,964 kali Harga Asli minus 3.756 kali Persen Diskon."

---

## Slide 6 — Interpretasi Regresi

"Apa artinya angka-angka ini untuk bisnis?"

"Pertama, setiap kenaikan harga asli Rp 1.000 akan meningkatkan harga jual Rp 964. Ini menunjukkan margin Periplus relatif tipis dan konsisten."

"Kedua, setiap kenaikan diskon 1% mengurangi harga jual Rp 3.756. Jadi diskon punya dampak signifikan."

"Konstanta Rp 14.971 merepresentasikan base markup yang diterapkan Periplus di atas harga penerbit."

"Model ini bisa dipakai untuk simulasi bisnis. Misalnya, kalau Periplus mau kasih diskon 20% ke buku seharga Rp 500 ribu, model bisa prediksi harga jualnya jadi berapa."

---

## Slide 7 — K-Means Clustering

"Analisis utama kedua saya: K-Means Clustering untuk segmentasi produk."

"Kami mengelompokkan 1.322 produk menjadi 3 kluster berdasarkan harga jual dan persentase diskon. Penentuan k=3 dilakukan melalui Elbow Method dan Silhouette Score."

"Silhouette Score yang kami dapat adalah 0,63 — ini menunjukkan pengelompokan yang cukup baik. Di grafik kiri terlihat visualisasi 3 kluster yang terbentuk, dan di kanan adalah grafik elbow dan silhouette yang mengkonfirmasi k=3 adalah pilihan optimal."

---

## Slide 8 — Detail Kluster

"Mari kita lihat karakteristik masing-masing kluster."

"Kluster pertama: Budget & Promo. Berisi 197 item atau 14,9% dari total. Rata-rata harga Rp 196.722 dengan diskon rata-rata 44,3%. Ini adalah buku-buku populer yang didiskon agresif. Strateginya: high-volume, low-margin."

"Kluster kedua: Standard Regular. Ini segmen terbesar, 1.013 item atau 76,6%. Rata-rata harga Rp 336.256 dengan diskon hanya 1,5%. Ini tulang punggung pendapatan Periplus — novel, buku bisnis, referensi reguler yang penjualannya stabil."

"Kluster ketiga: Premium Collector. Hanya 112 item atau 8,5%, tapi rata-rata harganya Rp 1.058.080 dengan diskon nyaris nol, 0,4%. Ini ensiklopedia, art books, dan edisi kolektor langka. Strateginya: low-volume, high-margin."

---

## Slide 9 — Business Insights

"Apa business insights yang bisa diambil?"

"Bagi konsumen: mereka bisa memanfaatkan informasi kluster Budget & Promo untuk menemukan promo terbaik. Sistem rekomendasi berbasis clustering juga bisa menyarankan buku dari segmen yang sama."

"Bagi pengelola e-commerce: model regresi bisa dipakai untuk dynamic pricing — simulasi skenario diskon tanpa merusak margin. Hasil clustering memungkinkan targeted marketing yang berbeda per segmen."

"Secara keseluruhan, R² 0,990 menunjukkan harga sangat bisa diprediksi. 3 kluster strategis memberikan framework jelas untuk strategi pemasaran yang berbeda."

---

## Slide 10 — Kesimpulan

"Untuk kesimpulan dari bagian saya:"

"Pipeline data science end-to-end berhasil diimplementasikan dari scraping hingga modeling."

"Model regresi linier menghasilkan R² = 0,990 — prediksi harga sangat akurat."

"K-Means membagi produk ke 3 kluster strategis dengan Silhouette Score 0,63."

"Hasil analisis ini siap digunakan untuk optimasi strategi penjualan e-commerce."

"Untuk pembahasan korelasi, klasifikasi, dan big data, akan dipresentasikan oleh partner saya, Rina Mardiana."

---

## Slide 11 — Terima Kasih

"Demikian presentasi dari saya. Terima kasih atas perhatian Bapak/Ibu dosen dan teman-teman sekalian."

"Wassalamualaikum warahmatullahi wabarakatuh."
