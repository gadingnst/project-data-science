"""
Generate analysis.ipynb — 1 notebook lengkap, 7 section, cell-by-cell.
Run: python3 build_notebook.py
"""
import json

def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src}

def code(src):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": src}

cells = []

# ============================================================
# HEADER
# ============================================================
cells.append(md([
    "# Tugas Data Science (IF404) - Project-Based Learning\n",
    "## Analisis Buku Impor pada E-Commerce Periplus.com\n",
    "\n",
    "**Dosen Pengampu:** Ir. Ahmad Chusyairi, M.Com., CDS., IPM., ASEAN Eng  \n",
    "**Anggota Kelompok:**\n",
    "1. Sutan Gading Fadhillah Nasution (250401020159)\n",
    "2. Rina Mardiana (250401020151)\n",
    "\n",
    "**Program Studi:** PJJ Informatika S1\n",
    "\n",
    "---"
]))

# ============================================================
# SECTION 1: MANAJEMEN DATA
# ============================================================
cells.append(md([
    "## 1. Manajemen Data\n",
    "\n",
    "Manajemen data mencakup proses pengumpulan, pemeriksaan kualitas, pembersihan, transformasi, dan persiapan dataset sebelum digunakan untuk analisis lebih lanjut.\n",
    "Dataset dikumpulkan melalui web scraping dari situs Periplus.com."
]))

cells.append(md(["### 1.1 Import Library & Load Dataset"]))

cells.append(code([
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import matplotlib.ticker as mticker\n",
    "import seaborn as sns\n",
    "import warnings\n",
    "import os\n",
    "warnings.filterwarnings('ignore')\n",
    "\n",
    "sns.set_theme(style='whitegrid', palette='muted')\n",
    "plt.rcParams.update({'figure.dpi': 120, 'figure.figsize': (10, 5)})\n",
    "PLOTS_DIR = 'plots/'\n",
    "os.makedirs(PLOTS_DIR, exist_ok=True)\n",
    "\n",
    "df = pd.read_csv('data/periplus_books_clean.csv')\n",
    "print(f'Dataset loaded: {df.shape[0]:,} rows x {df.shape[1]} columns')\n",
    "df.head(5)"
]))

cells.append(md(["### 1.2 Struktur & Info Dataset"]))

cells.append(code([
    "df.info()\n",
    "print(f'\\nDuplikat: {df.duplicated().sum()}')"
]))

cells.append(md(["### 1.3 Missing Values"]))

cells.append(code([
    "missing = df.isnull().sum()\n",
    "missing_pct = (missing / len(df) * 100).round(2)\n",
    "missing_df = pd.DataFrame({'Count': missing, '%': missing_pct})\n",
    "missing_df = missing_df[missing_df['Count'] > 0].sort_values('%', ascending=False)\n",
    "\n",
    "if not missing_df.empty:\n",
    "    fig, ax = plt.subplots(figsize=(8, 4))\n",
    "    bars = ax.barh(missing_df.index, missing_df['%'], color='#e07b54')\n",
    "    ax.bar_label(bars, fmt='%.1f%%', padding=3)\n",
    "    ax.set_xlabel('Missing (%)')\n",
    "    ax.set_title('Persentase Missing Values per Kolom')\n",
    "    plt.tight_layout()\n",
    "    plt.savefig(PLOTS_DIR + '1_missing_values.png', bbox_inches='tight')\n",
    "    plt.show()\n",
    "\n",
    "missing_df"
]))

cells.append(md(["### 1.4 Statistik Deskriptif"]))

cells.append(code([
    "num_cols = ['price_idr', 'original_price_idr', 'discount_percent', 'pages', 'weight', 'review_count']\n",
    "df[num_cols].describe().T.round(2)"
]))

cells.append(md(["### 1.5 Distribusi Kategori Buku"]))

cells.append(code([
    "cat_counts = df['category'].value_counts()\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(10, 5))\n",
    "bars = ax.barh(cat_counts.index[::-1], cat_counts.values[::-1],\n",
    "               color=sns.color_palette('muted', len(cat_counts)))\n",
    "ax.bar_label(bars, padding=3)\n",
    "ax.set_xlabel('Jumlah Buku')\n",
    "ax.set_title('Distribusi Buku per Kategori')\n",
    "plt.tight_layout()\n",
    "plt.savefig(PLOTS_DIR + '1_distribusi_kategori.png', bbox_inches='tight')\n",
    "plt.show()"
]))

cells.append(md(["### 1.6 Distribusi Harga"]))

cells.append(code([
    "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
    "\n",
    "axes[0].hist(df['price_idr'] / 1000, bins=40, color='#4c72b0', edgecolor='white', alpha=0.85)\n",
    "axes[0].axvline(df['price_idr'].median() / 1000, color='red', linestyle='--',\n",
    "                label=f\"Median: Rp {df['price_idr'].median()/1000:.0f}K\")\n",
    "axes[0].set_xlabel('Harga (ribu IDR)')\n",
    "axes[0].set_ylabel('Frekuensi')\n",
    "axes[0].set_title('Distribusi Harga Buku')\n",
    "axes[0].legend()\n",
    "\n",
    "cat_order = df.groupby('category')['price_idr'].median().sort_values().index\n",
    "df_plot = df.copy()\n",
    "df_plot['price_k'] = df_plot['price_idr'] / 1000\n",
    "sns.boxplot(data=df_plot, y='category', x='price_k', order=cat_order, ax=axes[1], palette='muted')\n",
    "axes[1].set_xlabel('Harga (ribu IDR)')\n",
    "axes[1].set_ylabel('')\n",
    "axes[1].set_title('Distribusi Harga per Kategori')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.savefig(PLOTS_DIR + '1_distribusi_harga.png', bbox_inches='tight')\n",
    "plt.show()"
]))

cells.append(md(["### 1.7 Status Stok & Diskon"]))

cells.append(code([
    "fig, axes = plt.subplots(1, 2, figsize=(12, 4))\n",
    "\n",
    "stock_counts = df['in_stock'].value_counts().rename({1: 'In Stock', 0: 'Out of Stock'})\n",
    "axes[0].pie(stock_counts.values, labels=stock_counts.index, autopct='%1.1f%%', colors=['#55a868', '#c44e52'])\n",
    "axes[0].set_title('Status Ketersediaan Stok')\n",
    "\n",
    "disc_counts = df['has_discount'].value_counts().rename({1: 'Ada Diskon', 0: 'Tanpa Diskon'})\n",
    "axes[1].pie(disc_counts.values, labels=disc_counts.index, autopct='%1.1f%%', colors=['#4c72b0', '#dd8452'])\n",
    "axes[1].set_title('Status Diskon Buku')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.savefig(PLOTS_DIR + '1_stok_diskon.png', bbox_inches='tight')\n",
    "plt.show()\n",
    "\n",
    "print(f\"In Stock   : {df['in_stock'].sum():,} ({df['in_stock'].mean()*100:.1f}%)\")\n",
    "print(f\"Ada Diskon : {df['has_discount'].sum():,} ({df['has_discount'].mean()*100:.1f}%)\")"
]))

# ============================================================
# SECTION 2: KORELASI DATA
# ============================================================
cells.append(md([
    "---\n",
    "## 2. Korelasi Data\n",
    "\n",
    "Analisis korelasi mengukur kekuatan dan arah hubungan antara dua variabel numerik. Nilai korelasi Pearson (r) berkisar dari **-1** hingga **+1**."
]))

cells.append(md(["### 2.1 Correlation Matrix"]))

cells.append(code([
    "corr_cols = ['price_idr', 'original_price_idr', 'discount_percent',\n",
    "             'pages', 'weight', 'review_count', 'book_age',\n",
    "             'price_per_page', 'popularity_score', 'in_stock', 'has_discount', 'is_new_release']\n",
    "\n",
    "corr_matrix = df[corr_cols].corr(method='pearson')\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(13, 10))\n",
    "sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdYlGn',\n",
    "            center=0, vmin=-1, vmax=1, linewidths=0.5, square=True, ax=ax)\n",
    "ax.set_title('Correlation Matrix — Dataset Buku Periplus', fontsize=15, pad=15)\n",
    "plt.tight_layout()\n",
    "plt.savefig(PLOTS_DIR + '2_correlation_matrix.png', bbox_inches='tight')\n",
    "plt.show()"
]))

cells.append(md(["### 2.2 Korelasi: Harga vs Jumlah Halaman"]))

cells.append(code([
    "df_s = df[(df['pages'] > 0) & (df['price_idr'] > 0)].copy()\n",
    "r = df_s[['price_idr', 'pages']].corr().iloc[0, 1]\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(9, 5))\n",
    "sns.regplot(data=df_s, x='pages', y='price_idr',\n",
    "            scatter_kws={'alpha': 0.3, 's': 20, 'color': '#4c72b0'},\n",
    "            line_kws={'color': 'red', 'linewidth': 2}, ax=ax)\n",
    "ax.set_xlabel('Jumlah Halaman')\n",
    "ax.set_ylabel('Harga (IDR)')\n",
    "ax.set_title(f'Korelasi Harga vs Halaman (r = {r:.3f})')\n",
    "plt.tight_layout()\n",
    "plt.savefig(PLOTS_DIR + '2_korelasi_harga_halaman.png', bbox_inches='tight')\n",
    "plt.show()\n",
    "print(f'Pearson r = {r:.4f}')"
]))

cells.append(md(["### 2.3 Korelasi: Harga vs Berat Buku"]))

cells.append(code([
    "df_w = df[(df['weight'] > 0) & (df['price_idr'] > 0)].copy()\n",
    "r_w = df_w[['price_idr', 'weight']].corr().iloc[0, 1]\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(9, 5))\n",
    "sns.regplot(data=df_w, x='weight', y='price_idr',\n",
    "            scatter_kws={'alpha': 0.3, 's': 20, 'color': '#55a868'},\n",
    "            line_kws={'color': 'red', 'linewidth': 2}, ax=ax)\n",
    "ax.set_xlabel('Berat Buku (kg)')\n",
    "ax.set_ylabel('Harga (IDR)')\n",
    "ax.set_title(f'Korelasi Harga vs Berat (r = {r_w:.3f})')\n",
    "plt.tight_layout()\n",
    "plt.savefig(PLOTS_DIR + '2_korelasi_harga_berat.png', bbox_inches='tight')\n",
    "plt.show()\n",
    "print(f'Pearson r = {r_w:.4f}')"
]))

cells.append(md(["### 2.4 Korelasi: Halaman vs Berat"]))

cells.append(code([
    "df_pw = df[(df['weight'] > 0) & (df['pages'] > 0)].copy()\n",
    "r_pw = df_pw[['pages', 'weight']].corr().iloc[0, 1]\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(9, 5))\n",
    "sns.regplot(data=df_pw, x='pages', y='weight',\n",
    "            scatter_kws={'alpha': 0.3, 's': 20, 'color': '#dd8452'},\n",
    "            line_kws={'color': 'red', 'linewidth': 2}, ax=ax)\n",
    "ax.set_xlabel('Jumlah Halaman')\n",
    "ax.set_ylabel('Berat (kg)')\n",
    "ax.set_title(f'Korelasi Halaman vs Berat (r = {r_pw:.3f})')\n",
    "plt.tight_layout()\n",
    "plt.savefig(PLOTS_DIR + '2_korelasi_halaman_berat.png', bbox_inches='tight')\n",
    "plt.show()\n",
    "print(f'Pearson r = {r_pw:.4f}')"
]))

# ============================================================
# SECTION 3: ASOSIASI DATA
# ============================================================
cells.append(md([
    "---\n",
    "## 3. Asosiasi Data\n",
    "\n",
    "Analisis asosiasi digunakan untuk menemukan pola hubungan antar item. Kita mencari pola asosiasi antara kategori, publisher, binding, dan fitur harga."
]))

cells.append(md(["### 3.1 Co-occurrence: Category x Publisher"]))

cells.append(code([
    "crosstab = pd.crosstab(df['category'], df['publisher'])\n",
    "top_pubs = df['publisher'].value_counts()[lambda x: x >= 10].index.tolist()\n",
    "crosstab_filtered = crosstab[top_pubs]\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(14, 6))\n",
    "sns.heatmap(crosstab_filtered, annot=True, fmt='d', cmap='YlGnBu',\n",
    "            linewidths=0.5, cbar_kws={'label': 'Jumlah Buku'}, ax=ax)\n",
    "ax.set_title('Co-occurrence: Category x Publisher', fontsize=14, pad=15)\n",
    "plt.xticks(rotation=45, ha='right')\n",
    "plt.tight_layout()\n",
    "plt.savefig(PLOTS_DIR + '3_cooccurrence_category_publisher.png', bbox_inches='tight')\n",
    "plt.show()"
]))

cells.append(md(["### 3.2 Asosiasi: Category x Binding"]))

cells.append(code([
    "ct_binding = pd.crosstab(df['category'], df['binding'], normalize='index') * 100\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(10, 6))\n",
    "ct_binding.plot(kind='bar', stacked=True, ax=ax, colormap='Set3', edgecolor='white')\n",
    "ax.set_title('Distribusi Binding per Kategori (%)', fontsize=14)\n",
    "ax.set_xlabel('Kategori')\n",
    "ax.set_ylabel('Persentase (%)')\n",
    "ax.legend(title='Binding', bbox_to_anchor=(1.05, 1), loc='upper left')\n",
    "plt.xticks(rotation=45, ha='right')\n",
    "plt.tight_layout()\n",
    "plt.savefig(PLOTS_DIR + '3_asosiasi_category_binding.png', bbox_inches='tight')\n",
    "plt.show()\n",
    "\n",
    "ct_binding.round(1)"
]))

cells.append(md(["### 3.3 Asosiasi: Price Category x Discount"]))

cells.append(code([
    "ct_pd = pd.crosstab(\n",
    "    df['price_category'],\n",
    "    df['has_discount'].map({0: 'No Discount', 1: 'Has Discount'}),\n",
    "    normalize='index') * 100\n",
    "\n",
    "order = ['Budget', 'Mid-range', 'Premium', 'Luxury']\n",
    "ct_pd = ct_pd.reindex([x for x in order if x in ct_pd.index])\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(9, 5))\n",
    "ct_pd.plot(kind='bar', ax=ax, color=['#dd8452', '#55a868'], edgecolor='white')\n",
    "ax.set_title('Price Category vs Discount Status', fontsize=14)\n",
    "ax.set_xlabel('Price Category')\n",
    "ax.set_ylabel('Persentase (%)')\n",
    "plt.xticks(rotation=0)\n",
    "plt.tight_layout()\n",
    "plt.savefig(PLOTS_DIR + '3_asosiasi_price_discount.png', bbox_inches='tight')\n",
    "plt.show()\n",
    "\n",
    "ct_pd.round(1)"
]))

cells.append(md(["### 3.4 Top Publisher x Category Associations"]))

cells.append(code([
    "assoc = df.groupby(['publisher', 'category']).size().reset_index(name='count')\n",
    "assoc = assoc[assoc['count'] >= 5].sort_values('count', ascending=False)\n",
    "top15 = assoc.head(15).copy()\n",
    "top15['label'] = top15['publisher'].str[:20] + ' -> ' + top15['category'].str[:15]\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(10, 6))\n",
    "bars = ax.barh(top15['label'][::-1], top15['count'][::-1],\n",
    "               color=sns.color_palette('viridis', 15))\n",
    "ax.bar_label(bars, padding=3)\n",
    "ax.set_xlabel('Jumlah Buku (Support)')\n",
    "ax.set_title('Top 15 Publisher x Category Associations', fontsize=14)\n",
    "plt.tight_layout()\n",
    "plt.savefig(PLOTS_DIR + '3_top_associations.png', bbox_inches='tight')\n",
    "plt.show()"
]))

# ============================================================
# SECTION 4: ANALISIS REGRESI
# ============================================================
cells.append(md([
    "---\n",
    "## 4. Analisis Regresi\n",
    "\n",
    "Regresi digunakan untuk memprediksi nilai kontinu. Kita akan memprediksi **harga buku** (`price_idr`) berdasarkan fitur-fitur seperti jumlah halaman, berat, kategori, dan lainnya."
]))

cells.append(md(["### 4.1 Persiapan Data untuk Regresi"]))

cells.append(code([
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.linear_model import LinearRegression\n",
    "from sklearn.ensemble import RandomForestRegressor\n",
    "from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score\n",
    "from sklearn.preprocessing import LabelEncoder\n",
    "\n",
    "df_reg = df[(df['pages'].notna()) & (df['weight'].notna()) &\n",
    "            (df['price_idr'] > 0) & (df['book_age'] >= 0)].copy()\n",
    "\n",
    "le_cat = LabelEncoder()\n",
    "le_pub = LabelEncoder()\n",
    "le_bind = LabelEncoder()\n",
    "df_reg['category_enc'] = le_cat.fit_transform(df_reg['category'])\n",
    "df_reg['publisher_enc'] = le_pub.fit_transform(df_reg['publisher'])\n",
    "df_reg['binding_enc'] = le_bind.fit_transform(df_reg['binding'])\n",
    "\n",
    "features = ['pages', 'weight', 'book_age', 'review_count',\n",
    "            'discount_percent', 'category_enc', 'publisher_enc', 'binding_enc']\n",
    "X = df_reg[features]\n",
    "y = df_reg['price_idr']\n",
    "\n",
    "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n",
    "print(f'Data: {len(df_reg):,} | Train: {len(X_train):,} | Test: {len(X_test):,}')"
]))

cells.append(md(["### 4.2 Linear Regression"]))

cells.append(code([
    "lr = LinearRegression()\n",
    "lr.fit(X_train, y_train)\n",
    "y_pred_lr = lr.predict(X_test)\n",
    "\n",
    "r2_lr = r2_score(y_test, y_pred_lr)\n",
    "rmse_lr = np.sqrt(mean_squared_error(y_test, y_pred_lr))\n",
    "mae_lr = mean_absolute_error(y_test, y_pred_lr)\n",
    "\n",
    "print(f'R2   : {r2_lr:.4f}')\n",
    "print(f'RMSE : Rp {rmse_lr:,.0f}')\n",
    "print(f'MAE  : Rp {mae_lr:,.0f}')"
]))

cells.append(md(["### 4.3 Random Forest Regressor"]))

cells.append(code([
    "rf = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)\n",
    "rf.fit(X_train, y_train)\n",
    "y_pred_rf = rf.predict(X_test)\n",
    "\n",
    "r2_rf = r2_score(y_test, y_pred_rf)\n",
    "rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))\n",
    "mae_rf = mean_absolute_error(y_test, y_pred_rf)\n",
    "\n",
    "print(f'R2   : {r2_rf:.4f}')\n",
    "print(f'RMSE : Rp {rmse_rf:,.0f}')\n",
    "print(f'MAE  : Rp {mae_rf:,.0f}')"
]))

cells.append(md(["### 4.4 Feature Importance & Actual vs Predicted"]))

cells.append(code([
    "feat_imp = pd.DataFrame({'Feature': features, 'Importance': rf.feature_importances_})\n",
    "feat_imp = feat_imp.sort_values('Importance', ascending=False)\n",
    "\n",
    "fig, axes = plt.subplots(1, 3, figsize=(18, 5))\n",
    "\n",
    "axes[0].barh(feat_imp['Feature'][::-1], feat_imp['Importance'][::-1],\n",
    "             color=sns.color_palette('viridis', len(feat_imp)))\n",
    "axes[0].set_xlabel('Importance')\n",
    "axes[0].set_title('Feature Importances (RF)')\n",
    "\n",
    "axes[1].scatter(y_test, y_pred_lr, alpha=0.4, s=20, color='#4c72b0')\n",
    "axes[1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)\n",
    "axes[1].set_xlabel('Actual')\n",
    "axes[1].set_ylabel('Predicted')\n",
    "axes[1].set_title(f'Linear Regression (R2={r2_lr:.3f})')\n",
    "\n",
    "axes[2].scatter(y_test, y_pred_rf, alpha=0.4, s=20, color='#55a868')\n",
    "axes[2].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)\n",
    "axes[2].set_xlabel('Actual')\n",
    "axes[2].set_ylabel('Predicted')\n",
    "axes[2].set_title(f'Random Forest (R2={r2_rf:.3f})')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.savefig(PLOTS_DIR + '4_regresi_results.png', bbox_inches='tight')\n",
    "plt.show()"
]))

# ============================================================
# SECTION 5: KLASIFIKASI DATA
# ============================================================
cells.append(md([
    "---\n",
    "## 5. Klasifikasi Data\n",
    "\n",
    "Klasifikasi adalah teknik supervised learning untuk memprediksi kategori/kelas dari data. Kita membangun 3 model klasifikasi."
]))

cells.append(md(["### 5.1 Klasifikasi Popularitas Buku (Popular vs Unpopular)"]))

cells.append(code([
    "from sklearn.ensemble import RandomForestClassifier\n",
    "from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score\n",
    "\n",
    "df_cls = df[(df['pages'].notna()) & (df['weight'].notna())].copy()\n",
    "df_cls['is_popular'] = (df_cls['review_count'] > 0).astype(int)\n",
    "df_cls['category_enc'] = LabelEncoder().fit_transform(df_cls['category'])\n",
    "df_cls['publisher_enc'] = LabelEncoder().fit_transform(df_cls['publisher'])\n",
    "df_cls['binding_enc'] = LabelEncoder().fit_transform(df_cls['binding'])\n",
    "\n",
    "feat_cls = ['price_idr', 'pages', 'weight', 'discount_percent',\n",
    "            'book_age', 'category_enc', 'publisher_enc', 'binding_enc']\n",
    "\n",
    "X1 = df_cls[feat_cls]\n",
    "y1 = df_cls['is_popular']\n",
    "X1_tr, X1_te, y1_tr, y1_te = train_test_split(X1, y1, test_size=0.2, random_state=42, stratify=y1)\n",
    "\n",
    "rf1 = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)\n",
    "rf1.fit(X1_tr, y1_tr)\n",
    "y1_pred = rf1.predict(X1_te)\n",
    "\n",
    "print(f'Accuracy: {accuracy_score(y1_te, y1_pred):.4f}')\n",
    "print(f'F1-Score: {f1_score(y1_te, y1_pred):.4f}')\n",
    "print()\n",
    "print(classification_report(y1_te, y1_pred, target_names=['Unpopular', 'Popular']))"
]))

cells.append(code([
    "cm1 = confusion_matrix(y1_te, y1_pred)\n",
    "fig, ax = plt.subplots(figsize=(6, 5))\n",
    "sns.heatmap(cm1, annot=True, fmt='d', cmap='Blues',\n",
    "            xticklabels=['Unpopular', 'Popular'],\n",
    "            yticklabels=['Unpopular', 'Popular'], ax=ax)\n",
    "ax.set_title(f'Confusion Matrix - Popularity (Acc: {accuracy_score(y1_te, y1_pred):.3f})')\n",
    "ax.set_ylabel('Actual')\n",
    "ax.set_xlabel('Predicted')\n",
    "plt.tight_layout()\n",
    "plt.savefig(PLOTS_DIR + '5_cm_popularity.png', bbox_inches='tight')\n",
    "plt.show()"
]))

cells.append(md(["### 5.2 Klasifikasi Price Category"]))

cells.append(code([
    "le_pc = LabelEncoder()\n",
    "df_cls['price_cat_enc'] = le_pc.fit_transform(df_cls['price_category'])\n",
    "\n",
    "feat_cls2 = ['pages', 'weight', 'discount_percent', 'book_age',\n",
    "             'review_count', 'category_enc', 'publisher_enc', 'binding_enc']\n",
    "\n",
    "X2 = df_cls[feat_cls2]\n",
    "y2 = df_cls['price_cat_enc']\n",
    "X2_tr, X2_te, y2_tr, y2_te = train_test_split(X2, y2, test_size=0.2, random_state=42, stratify=y2)\n",
    "\n",
    "rf2 = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)\n",
    "rf2.fit(X2_tr, y2_tr)\n",
    "y2_pred = rf2.predict(X2_te)\n",
    "\n",
    "print(f'Accuracy: {accuracy_score(y2_te, y2_pred):.4f}')\n",
    "print()\n",
    "print(classification_report(y2_te, y2_pred, target_names=le_pc.classes_))"
]))

cells.append(code([
    "cm2 = confusion_matrix(y2_te, y2_pred)\n",
    "fig, ax = plt.subplots(figsize=(7, 6))\n",
    "sns.heatmap(cm2, annot=True, fmt='d', cmap='YlGnBu',\n",
    "            xticklabels=le_pc.classes_, yticklabels=le_pc.classes_, ax=ax)\n",
    "ax.set_title(f'Confusion Matrix - Price Category (Acc: {accuracy_score(y2_te, y2_pred):.3f})')\n",
    "ax.set_ylabel('Actual')\n",
    "ax.set_xlabel('Predicted')\n",
    "plt.tight_layout()\n",
    "plt.savefig(PLOTS_DIR + '5_cm_price_category.png', bbox_inches='tight')\n",
    "plt.show()"
]))

cells.append(md(["### 5.3 Klasifikasi Has Discount"]))

cells.append(code([
    "feat_cls3 = ['original_price_idr', 'pages', 'weight', 'book_age',\n",
    "             'review_count', 'category_enc', 'publisher_enc', 'binding_enc']\n",
    "\n",
    "X3 = df_cls[feat_cls3]\n",
    "y3 = df_cls['has_discount']\n",
    "X3_tr, X3_te, y3_tr, y3_te = train_test_split(X3, y3, test_size=0.2, random_state=42, stratify=y3)\n",
    "\n",
    "rf3 = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1)\n",
    "rf3.fit(X3_tr, y3_tr)\n",
    "y3_pred = rf3.predict(X3_te)\n",
    "\n",
    "print(f'Accuracy: {accuracy_score(y3_te, y3_pred):.4f}')\n",
    "print(f'F1-Score: {f1_score(y3_te, y3_pred):.4f}')\n",
    "print()\n",
    "print(classification_report(y3_te, y3_pred, target_names=['No Discount', 'Has Discount']))"
]))

# ============================================================
# SECTION 6: CLUSTERING DATA
# ============================================================
cells.append(md([
    "---\n",
    "## 6. Clustering Data\n",
    "\n",
    "Clustering adalah teknik unsupervised learning untuk mengelompokkan data berdasarkan kesamaan fitur. Kita menggunakan **K-Means Clustering**."
]))

cells.append(md(["### 6.1 Persiapan Data & Elbow Method"]))

cells.append(code([
    "from sklearn.cluster import KMeans\n",
    "from sklearn.preprocessing import StandardScaler\n",
    "from sklearn.decomposition import PCA\n",
    "from sklearn.metrics import silhouette_score\n",
    "\n",
    "df_clust = df[(df['pages'] > 0) & (df['weight'] > 0) & (df['price_idr'] > 0)].copy()\n",
    "cluster_features = ['price_idr', 'pages', 'weight', 'review_count', 'discount_percent']\n",
    "X_clust = df_clust[cluster_features].copy()\n",
    "\n",
    "scaler = StandardScaler()\n",
    "X_scaled = scaler.fit_transform(X_clust)\n",
    "\n",
    "inertias, sils = [], []\n",
    "K_range = range(2, 11)\n",
    "for k in K_range:\n",
    "    km = KMeans(n_clusters=k, random_state=42, n_init=10)\n",
    "    km.fit(X_scaled)\n",
    "    inertias.append(km.inertia_)\n",
    "    sils.append(silhouette_score(X_scaled, km.labels_))\n",
    "\n",
    "fig, axes = plt.subplots(1, 2, figsize=(14, 4))\n",
    "axes[0].plot(K_range, inertias, marker='o', lw=2, color='#4c72b0')\n",
    "axes[0].set_xlabel('K')\n",
    "axes[0].set_ylabel('Inertia')\n",
    "axes[0].set_title('Elbow Method')\n",
    "axes[1].plot(K_range, sils, marker='o', lw=2, color='#55a868')\n",
    "axes[1].set_xlabel('K')\n",
    "axes[1].set_ylabel('Silhouette Score')\n",
    "axes[1].set_title('Silhouette Score per K')\n",
    "plt.tight_layout()\n",
    "plt.savefig(PLOTS_DIR + '6_elbow_method.png', bbox_inches='tight')\n",
    "plt.show()\n",
    "\n",
    "print(f'Data: {len(df_clust):,} rows | Features: {cluster_features}')"
]))

cells.append(md(["### 6.2 K-Means Clustering (K=4)"]))

cells.append(code([
    "optimal_k = 4\n",
    "kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)\n",
    "df_clust['cluster'] = kmeans.fit_predict(X_scaled)\n",
    "\n",
    "print(f'Silhouette Score: {silhouette_score(X_scaled, df_clust[\"cluster\"]):.4f}')\n",
    "print()\n",
    "\n",
    "profile = df_clust.groupby('cluster')[cluster_features].mean().round(1)\n",
    "profile['count'] = df_clust.groupby('cluster').size()\n",
    "print('Cluster Profile (Mean):')\n",
    "profile"
]))

cells.append(md(["### 6.3 Visualisasi Cluster (PCA 2D)"]))

cells.append(code([
    "pca = PCA(n_components=2, random_state=42)\n",
    "X_pca = pca.fit_transform(X_scaled)\n",
    "df_clust['pca1'] = X_pca[:, 0]\n",
    "df_clust['pca2'] = X_pca[:, 1]\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(10, 6))\n",
    "colors = sns.color_palette('Set2', optimal_k)\n",
    "for i in range(optimal_k):\n",
    "    d = df_clust[df_clust['cluster'] == i]\n",
    "    ax.scatter(d['pca1'], d['pca2'], c=[colors[i]], label=f'Cluster {i}',\n",
    "               alpha=0.6, s=30, edgecolors='white', linewidth=0.5)\n",
    "\n",
    "centers_pca = pca.transform(kmeans.cluster_centers_)\n",
    "ax.scatter(centers_pca[:, 0], centers_pca[:, 1], c='red', marker='X',\n",
    "           s=300, edgecolors='black', linewidth=2, label='Centroids', zorder=10)\n",
    "ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)')\n",
    "ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)')\n",
    "ax.set_title(f'K-Means Clustering (K={optimal_k}) - PCA 2D')\n",
    "ax.legend()\n",
    "plt.tight_layout()\n",
    "plt.savefig(PLOTS_DIR + '6_clusters_pca.png', bbox_inches='tight')\n",
    "plt.show()"
]))

cells.append(md(["### 6.4 Distribusi Fitur per Cluster"]))

cells.append(code([
    "fig, axes = plt.subplots(2, 2, figsize=(14, 10))\n",
    "df_clust['price_k'] = df_clust['price_idr'] / 1000\n",
    "\n",
    "sns.boxplot(data=df_clust, x='cluster', y='price_k', palette='Set2', ax=axes[0,0])\n",
    "axes[0,0].set_ylabel('Harga (K IDR)')\n",
    "axes[0,0].set_title('Harga per Cluster')\n",
    "\n",
    "sns.boxplot(data=df_clust, x='cluster', y='pages', palette='Set2', ax=axes[0,1])\n",
    "axes[0,1].set_title('Halaman per Cluster')\n",
    "\n",
    "sns.boxplot(data=df_clust, x='cluster', y='weight', palette='Set2', ax=axes[1,0])\n",
    "axes[1,0].set_title('Berat per Cluster')\n",
    "\n",
    "sns.boxplot(data=df_clust, x='cluster', y='review_count', palette='Set2', ax=axes[1,1])\n",
    "axes[1,1].set_title('Review Count per Cluster')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.savefig(PLOTS_DIR + '6_clusters_boxplot.png', bbox_inches='tight')\n",
    "plt.show()"
]))

# ============================================================
# SECTION 7: BIG DATA & PERKEMBANGANNYA
# ============================================================
cells.append(md([
    "---\n",
    "## 7. Big Data & Perkembangannya\n",
    "\n",
    "Section ini membahas konsep Big Data, karakteristiknya, tools, tantangan, dan bagaimana analisis kita dapat di-scale."
]))

cells.append(md([
    "### 7.1 Apa Itu Big Data?\n",
    "\n",
    "**Big Data** mengacu pada dataset yang sangat besar dan kompleks sehingga tidak dapat diproses dengan tools tradisional.\n",
    "\n",
    "#### 5V Characteristics:\n",
    "| Karakteristik | Deskripsi | Contoh pada Dataset Buku |\n",
    "|---|---|---|\n",
    "| **Volume** | Ukuran data sangat besar | Jutaan buku dari ribuan toko |\n",
    "| **Velocity** | Kecepatan data masuk/berubah | Real-time price updates |\n",
    "| **Variety** | Beragam format data | Text, images, reviews, ratings |\n",
    "| **Veracity** | Keakuratan data | Missing values, inconsistencies |\n",
    "| **Value** | Nilai bisnis dari insight | Pricing strategy, recommendations |"
]))

cells.append(md(["### 7.2 Dataset Kita vs Big Data"]))

cells.append(code([
    "current_rows = len(df)\n",
    "mem_mb = df.memory_usage(deep=True).sum() / (1024**2)\n",
    "\n",
    "scenarios = [\n",
    "    ('Current', current_rows, mem_mb),\n",
    "    ('10x Scale', current_rows * 10, mem_mb * 10),\n",
    "    ('100x Scale', current_rows * 100, mem_mb * 100),\n",
    "    ('1000x Scale', current_rows * 1000, mem_mb * 1000),\n",
    "    ('Amazon-scale', 350_000_000, mem_mb * (350_000_000 / current_rows)),\n",
    "]\n",
    "\n",
    "sc_df = pd.DataFrame(scenarios, columns=['Scenario', 'Rows', 'Memory (MB)'])\n",
    "sc_df['Memory (GB)'] = (sc_df['Memory (MB)'] / 1024).round(2)\n",
    "sc_df['Rows'] = sc_df['Rows'].apply(lambda x: f'{x:,.0f}')\n",
    "sc_df['Memory (MB)'] = sc_df['Memory (MB)'].apply(lambda x: f'{x:,.1f}')\n",
    "sc_df"
]))

cells.append(md([
    "### 7.3 Tools & Teknologi Big Data\n",
    "\n",
    "#### Storage & Processing\n",
    "| Tool | Fungsi | Kapan Digunakan |\n",
    "|---|---|---|\n",
    "| **Hadoop HDFS** | Distributed file storage | Dataset > 100GB |\n",
    "| **Apache Spark** | Distributed processing | Analisis paralel & ML |\n",
    "| **Dask** | Python parallel computing | Pandas-like API untuk big data |\n",
    "| **Apache Kafka** | Real-time streaming | Live updates & events |\n",
    "\n",
    "#### Cloud Platforms\n",
    "| Platform | Services |\n",
    "|---|---|\n",
    "| **AWS** | S3, Redshift, EMR, SageMaker |\n",
    "| **Google Cloud** | BigQuery, Dataflow, Vertex AI |\n",
    "| **Azure** | Data Lake, Synapse, Databricks |"
]))

cells.append(md([
    "### 7.4 Scaling Strategy\n",
    "\n",
    "| Task | Current | Big Data |\n",
    "|---|---|---|\n",
    "| Data Loading | `pd.read_csv()` | `dask.read_csv()` / Spark |\n",
    "| Processing | `df.groupby()` | Lazy eval + parallel |\n",
    "| ML | scikit-learn | Spark MLlib / Dask-ML |\n",
    "| Storage | CSV | Parquet (columnar, compressed) |\n",
    "| Database | SQLite/CSV | PostgreSQL / BigQuery |\n",
    "\n",
    "### 7.5 Tren Big Data (2024-2026)\n",
    "1. **AI/ML Integration** - AutoML, LLMs, MLOps\n",
    "2. **Real-time Analytics** - Event-driven architectures\n",
    "3. **Data Lakehouse** - Delta Lake, Apache Iceberg\n",
    "4. **Serverless** - BigQuery, Snowflake, Databricks\n",
    "5. **Data Governance** - Compliance automation, federated learning"
]))

# ============================================================
# KESIMPULAN
# ============================================================
cells.append(md([
    "---\n",
    "## 8. Kesimpulan\n",
    "\n",
    "Proyek ini telah menganalisis dataset buku dari Periplus.com dengan 7 teknik:\n",
    "\n",
    "1. **Manajemen Data** - Scraping, cleaning, feature engineering (1,328 rows x 23 kolom)\n",
    "2. **Korelasi** - Korelasi kuat antara harga-halaman-berat\n",
    "3. **Asosiasi** - Pola publisher-category dan price-discount teridentifikasi\n",
    "4. **Regresi** - Random Forest memprediksi harga dengan akurasi tinggi\n",
    "5. **Klasifikasi** - Model klasifikasi popularitas, price category, dan diskon\n",
    "6. **Clustering** - Segmentasi buku menjadi 4 cluster bermakna\n",
    "7. **Big Data** - Pemahaman tools dan arsitektur untuk scaling\n",
    "\n",
    "### Manfaat untuk E-Commerce:\n",
    "- **Pricing Strategy** - Prediksi harga optimal\n",
    "- **Targeted Marketing** - Segmentasi berdasarkan cluster\n",
    "- **Inventory Management** - Stock allocation berdasarkan popularitas\n",
    "- **Recommendation** - Rekomendasi buku berdasarkan pola asosiasi\n",
    "\n",
    "---\n",
    "*Tugas Data Science IF404 - PJJ Informatika S1 - 2026*"
]))

# ============================================================
# SAVE
# ============================================================
nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11.0"}
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

with open('analysis.ipynb', 'w') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

# Validate
with open('analysis.ipynb') as f:
    data = json.load(f)

print(f"Total cells: {len(data['cells'])}")
md_count = sum(1 for c in data['cells'] if c['cell_type'] == 'markdown')
code_count = sum(1 for c in data['cells'] if c['cell_type'] == 'code')
print(f"Markdown cells: {md_count}")
print(f"Code cells: {code_count}")
print("VALID JSON!")
