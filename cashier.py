import streamlit as st

st.set_page_config(page_title="كاشير بوما", page_icon="☕", layout="wide")

st.title("BOMA Cashier - كاشير بوما")
st.caption("مرحباً بك في الطلبات")

# قائمة المنتجات والأسعار
menu = {
    "قهوة مختصة": {
        "قهوة اليوم": 7.0,
        "إسبريسو": 8.0,
        "فلات وايت": 12.0,
        "لاتيه": 14.0
    },
    "مشروبات باردة": {
        "آيس لاتيه": 15.0,
        "آيس سبانيش": 17.0,
        "موهيتو": 13.0
    },
    "حلا": {
        "كيكة شوكولاتة": 16.0,
        "تشيز كيك": 18.0,
        "كرواسون": 9.0
    }
}

# تهيئة السلة في Session State
if 'cart' not in st.session_state:
    st.session_state.cart = []

st.header("اختيار الطلب")
col1, col2 = st.columns(2)

with col1:
    category = st.selectbox("إختر القسم", list(menu.keys()))

with col2:
    item = st.selectbox("إختر الصنف", list(menu[category].keys()))

price = menu[category][item]
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

grand_total = 0.0  # تعريف المتغير تفادياً للـ NameError

if len(st.session_state.cart) > 0:
    for i, order in enumerate(st.session_state.cart):
        grand_total += order['total']
        st.write(f"{i+1}. **{order['item']}** - الكمية: {order['quantity']} - السعر: {order['total']} ريال")
    
    st.markdown(f"### الإجمالي الكلي للطلب: {grand_total} ريال")
    
    payment_method = st.radio("طريقة الدفع", ["كاش (Cash)", "شبكة / مدى (POS)"])
    
    if st.button("إتمام الدفع"):
        st.balloons()
        st.success(f"تم إتمام الطلب بنجاح ({payment_method})! شكراً لزيارتكم BOMA.")
        st.session_state.cart = []
else:
    st.write("السلة فارغة حالياً. قم بإضافة طلبات لعرض الفاتورة.")