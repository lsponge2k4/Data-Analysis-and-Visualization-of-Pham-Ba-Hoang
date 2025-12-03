# cartier_dashboard.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# -----------------------
# 1. Đọc dữ liệu
# -----------------------
df = pd.read_csv('csv/cartier_catalog.csv')

# -----------------------
# 2. Tiêu đề dashboard
# -----------------------
st.title("Dashboard Cartier Catalog")   
st.markdown("Phân tích và trực quan hóa dữ liệu sản phẩm Cartier")

# -----------------------
# 3. Filter nâng cao
# -----------------------
category_list = ['All'] + list(df['categorie'].unique())
selected_category = st.selectbox("Chọn category:", category_list)

top_tags = df['tags'].value_counts().head(10).index
selected_tags = st.multiselect("Chọn tags (top 10):", top_tags, default=list(top_tags))

min_price, max_price = st.slider(
    "Chọn khoảng giá:",
    float(df['price'].min()), float(df['price'].max()),
    (float(df['price'].min()), float(df['price'].max()))
)

filtered_df = df.copy()
if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['categorie'] == selected_category]
filtered_df = filtered_df[filtered_df['tags'].isin(selected_tags)]
filtered_df = filtered_df[(filtered_df['price'] >= min_price) & (filtered_df['price'] <= max_price)]

st.subheader(f"Số lượng sản phẩm sau filter: {len(filtered_df)}")

# -----------------------
# 4. Histogram giá sản phẩm
# -----------------------
st.subheader("Phân bố giá sản phẩm")
fig, ax = plt.subplots()
sns.histplot(filtered_df['price'], bins=20, kde=True, ax=ax)
ax.set_xlabel("Price (USD)")
ax.set_ylabel("Số lượng sản phẩm")
st.pyplot(fig)

# -----------------------
# 5. Scatter plot giá vs tags
# -----------------------
st.subheader("Scatter: Giá sản phẩm theo tags")
scatter_df = filtered_df
fig2, ax2 = plt.subplots()
sns.scatterplot(data=scatter_df, x='tags', y='price', hue='categorie', s=100, ax=ax2)
plt.xticks(rotation=45)
ax2.set_xlabel("Tags")
ax2.set_ylabel("Price (USD)")
st.pyplot(fig2)

# -----------------------
# 6. Pie chart tỷ lệ sản phẩm
# -----------------------
st.subheader("Tỷ lệ sản phẩm theo category")
category_counts = filtered_df['categorie'].value_counts()
fig3, ax3 = plt.subplots()
ax3.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140)
ax3.axis('equal')
st.pyplot(fig3)

# -----------------------
# 7. Bảng chi tiết + download CSV
# -----------------------
st.subheader("Chi tiết sản phẩm")
st.dataframe(filtered_df[['ref', 'title', 'categorie', 'tags', 'price']])

st.download_button(
    label="Tải CSV dữ liệu hiện tại",
    data=filtered_df.to_csv(index=False),
    file_name='filtered_cartier.csv',
    mime='text/csv'
)
