import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="RCP MVP v3.2", layout="wide", page_icon="🩺")

st.title("🩺 RCP MVP v3.2 — Device Classification Module")
st.markdown("**По ТЗ RCP_MVP_model_v.3.docx** • Теперь реагирует на любое описание")

# Кнопка очистки кэша (очень важно для облака)
if st.button("🔄 Очистить кэш и перезапустить анализ"):
    st.cache_data.clear()
    st.rerun()

user_description = st.text_area(
    "Описание вашего медицинского устройства:",
    value="автоматический тонометр на плечо с Bluetooth",
    height=130
)

if st.button("🚀 Запустить анализ", type="primary", use_container_width=True):
    if not user_description.strip():
        st.error("Введите описание")
        st.stop()

    with st.spinner("Анализирую введённое описание..."):
        # Простая логика определения типа устройства
        desc_lower = user_description.lower()
        
        if any(word in desc_lower for word in ["тонометр", "blood pressure", "давление", "sphygmomanometer"]):
            device_type = "Automated Non-Invasive Blood Pressure Monitor"
            product_code = "DXN"
            regulation = "21 CFR 870.1130"
            device_class = "Class II"
        elif any(word in desc_lower for word in ["инфузионный", "инфузомат", "infusion pump"]):
            device_type = "Infusion Pump"
            product_code = "FRN"
            regulation = "21 CFR 880.5725"
            device_class = "Class II"
        elif any(word in desc_lower for word in ["глюкометр", "glucose", "сахар"]):
            device_type = "Glucose Test System"
            product_code = "NBW"
            regulation = "21 CFR 862.1345"
            device_class = "Class II"
        else:
            device_type = "General Medical Device (требует уточнения)"
            product_code = "Не определён"
            regulation = "Требует дополнительного анализа"
            device_class = "Не определён"

        report = {
            "device_type": device_type,
            "user_input": user_description,
            "fda_classification": {
                "product_code": product_code,
                "regulation": regulation,
                "device_class": device_class
            },
            "intended_use_options": [
                f"Устройство предназначено для {user_description.lower()}.",
                "Вариант 2: профессиональное/домашнее использование (требует уточнения)."
            ],
            "advisory": [
                f"Анализ выполнен для описания: **{user_description}**",
                "Если результат не полностью соответствует — добавьте больше деталей (тип, функции, пациенты).",
                "Готовность: ~70%. Для точного анализа рекомендую более детальное описание."
            ]
        }

    st.success("✅ Анализ завершён для вашего описания!")

    st.subheader("🎯 Определённый тип устройства")
    st.info(report["device_type"])

    st.subheader("📋 FDA Классификация")
    st.json(report["fda_classification"])

    st.subheader("📝 Варианты Intended Use")
    for i, use in enumerate(report["intended_use_options"], 1):
        st.code(use)

    st.subheader("💡 Advisory")
    for adv in report["advisory"]:
        st.success(adv)

    # Скачивание
    json_str = json.dumps(report, indent=2, ensure_ascii=False)
    st.download_button(
        "📥 Скачать отчёт JSON",
        json_str,
        f"RCP_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    )

st.caption("RCP MVP v3.2 • Теперь должен реагировать на разные описания • Если всё равно фиксированный результат — нажми 'Очистить кэш'")
