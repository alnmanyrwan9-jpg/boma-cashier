import pandas as pd
from datetime import datetime 
import os 
import streamlit as st
LOG_FILE = "daily_orders.csv" 
if not os.path.exists(LOG_FILE):
    df_empty = pd.DataFrame(columns=["رقم الفاتورة","التاريخ و الوقت","الأصناف","الإجمالي"])
    df_empty.to_csv(LOG_FILE, index=False, encoding="utf-8-sig")
    st.sidebar.title("📌 القائمة")
app_mode = st.sidebar.radio("اختر الصفحة:", ["طلب جديد (الكاشير)", "مراجعة فواتير اليوم"])
st.set_page_config(page_title="كاشير بوما", page_icon="☕", layout="wide")

st.title("BOMA Cashier - كاشير بوما")
st.caption("مرحباً بك")

menu = {
    "قهوة مختصة": { 
        "قهوة اليوم": {"صغير": 5.5, "كبير": 7.0},
        "V60 قهوة مقطرة": {"صغير": 12.0, "كبير": 14.0},
        "هوت شوكليت": {"صغير": 8.0, "كبير": 10.0}
    },
   "مشروبات بارده": {
        "كركديه": {"صغير": 5.5, "كبير": 7.0},
        "ايس تي": {"صغير": 5.5, "كبير": 7.0},
        "ماتشا لاتيه": {"حجم واحد": 15.0},
        "ماء": {"حجم واحد": 1.0}
    },
    "حلا": {
       "كوكيز": {"حجم واحد": 8.0},
        "بودنق كوكيز": {"حجم واحد": 13.0},
        "شوكلت كيك بلجيكي": {"حجم واحد": 13.0},
        "بيكان كراميل كيك": {"حجم واحد": 15.0}
    },
    "بوكس الجمعات":{
      "بوكس 1 لتر":{"حجم واحد":35.0}
    }
}

# تهيئة السلة في Session State
if 'cart' not in st.session_state:
    st.session_state.cart = []

st.header("اختيار الطلب")
col1, col2, col3= st.columns(3)

with col1:
    category = st.selectbox("إختر القسم", list(menu.keys()))

with col2:
    item = st.selectbox("إختر الصنف", list(menu[category].keys()))

with col3:
    available_sizes = list(menu[category][item].keys())
    size = st.selectbox("إختر الحجم", available_sizes)

price = menu[category][item][size]

st.info(f"سعر {item}: {price} ريال")

quantity = st.number_input("الكمية", min_value=1, value=1, step=1)
total_item_price = price * quantity
st.write(f"الإجمالي لهذا الصنف: {total_item_price} ريال")

if st.button("إضافة للطلب +"):
    st.session_state.cart.append({
        "item": item,
        "price": price,
        "quantity": quantity,
        "total": total_item_price
    })
    st.success(f"تمت إضافة {quantity} x {item} بنجاح!")

st.markdown("---")
st.header("فاتورة الطلبات الحالية")

grand_total = 0.0  

if len(st.session_state.cart) > 0:
    for i, order in enumerate(st.session_state.cart):
        grand_total += order['total']
        st.write(f"{i+1}. **{order['item']}** - الكمية: {order['quantity']} - السعر: {order['total']} ريال")
    
    st.markdown(f"### الإجمالي الكلي للطلب: {grand_total} ريال")
    
    payment_method = st.radio("طريقة الدفع", ["كاش (Cash)", "شبكة / مدى (POS)"])
    
    if st.button("إتمام الدفع"):
        st.balloons()
        new_order = pd.DataFrame([{"رقم الفاتورة": datetime.now().strftime("%Y%m%d%H%M%S"), "التاريخ والوقت": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "الإجمالي": grand_total}])
        new_order.to_csv(LOG_FILE, mode='a', header=not os.path.exists(LOG_FILE), index=False, encoding="utf-8-sig")
        st.success(f"تم إتمام الطلب بنجاح ({payment_method})! شكراً لزيارتكم BOMA.")
        st.session_state.cart = []
else:
    st.write("السلة فارغة حالياً. قم بإضافة طلبات لعرض الفاتورة.")
if app_mode == "مراجعة فواتير اليوم":
    st.title("📊 مراجعة فواتير اليوم")
    if os.path.exists(LOG_FILE):
        df_orders = pd.read_csv(LOG_FILE, encoding="utf-8-sig")
        st.metric("إجمالي المبيعات", f"{df_orders['الإجمالي'].sum()} ريال")
        st.dataframe(df_orders, use_container_width=True)
else:
     st.info("لا توجد فواتير مسجلة اليوم.")