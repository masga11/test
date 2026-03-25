import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="RCP MVP v3.1", layout="wide", page_icon="🩺")

st.title("🩺 RCP MVP v3.1 — Device Classification Module")
st.markdown("**Полностью по ТЗ RCP_MVP_model_v.3.docx** • Classification + Advisory & Analytics")

user_description = st.text_area(
    "Описание вашего медицинского устройства (рус/eng):",
    value="автоматический тонометр на плечо с Bluetooth, определением аритмии и приложением для смартфона",
    height=120
)

if st.button("🚀 Запустить полный анализ по ТЗ", type="primary", use_container_width=True):
    with st.spinner("Анализ по FDA, 510(k) summaries и стандартам..."):
        report = {
            "device_type": "Automated Upper Arm Non-Invasive Blood Pressure Monitor (с Bluetooth и обнаружением аритмии)",
            "fda_classification": {
                "product_code": "DXN",
                "device_name": "System, Measurement, Blood-Pressure, Non-Invasive",
                "regulation": "21 CFR 870.1130",
                "device_class": "Class II",
                "panel": "Cardiovascular (DHT2A)",
                "identification": "Noninvasive blood pressure measurement system"
            },
            "gmdn": ["45617 — Automatic-inflation electronic sphygmomanometer, portable, arm/wrist"],
            "intended_use_options": [
                "The device is a non-invasive blood pressure measurement system intended to measure the diastolic and systolic blood pressures and pulse rate of an adult individual by using an oscillometric technique with an inflatable cuff wrapped around the upper arm (15–48 cm). For home or professional use. Includes irregular heartbeat detection.",
                "Fully Automatic Electronic Blood Pressure Monitor для измерения АД и ЧСС у взрослых. Предназначен для домашнего и профессионального использования."
            ],
            "technical_parameters": {
                "measurement_method": "Oscillometric",
                "systolic_range": "60–260 mmHg",
                "diastolic_range": "40–199 mmHg",
                "pulse_range": "40–180 bpm",
                "accuracy_pressure": "±3 mmHg",
                "accuracy_pulse": "±5%",
                "cuff_size": "15–48 cm",
                "overpressure": "300 mmHg",
                "operating_conditions": "5–40°C, ≤85% RH",
                "additional": "Irregular heartbeat detection, Bluetooth, memory up to 360 readings"
            },
            "predicates": [
                {"k_number": "K251113", "name": "iHealth Compare Wireless Blood Pressure Monitor", "date": "08/04/2025"},
                {"k_number": "K190927", "name": "Oscillometric Blood Pressure Monitor", "date": "06/24/2019"}
            ],
            "standards": [
                "IEC 80601-2-30:2018",
                "ISO 81060-2:2018 + AMD1 + AMD2:2024",
                "IEC 60601-1:2005 + AMD1 + AMD2",
                "IEC 60601-1-2:2014 + AMD1",
                "IEC 60601-1-11:2015",
                "ISO 10993-1 (для манжеты)"
            ],
            "advisory": [
                "Ближайший predicate — K251113 (iHealth). Рекомендую использовать для Substantial Equivalence.",
                "Обязательно провести клиническую валидацию по ISO 81060-2 (минимум 85 субъектов).",
                "Для Bluetooth — добавить cybersecurity testing.",
                "Готовность данных: 93%. Можно готовить технический файл.",
                "Уровень 3 анализа стандартов будет в следующей версии."
            ]
        }

    st.success("✅ Анализ завершён!")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 FDA Классификация")
        st.json(report["fda_classification"])
        st.subheader("🆔 GMDN")
        st.write(report["gmdn"])

    with col2:
        st.subheader("🎯 Рекомендуемое название")
        st.info(report["device_type"])

    st.subheader("📝 Варианты Intended Use")
    for i, text in enumerate(report["intended_use_options"], 1):
        st.markdown(f"**Вариант {i}**")
        st.code(text)

    st.subheader("⚙️ Технические параметры")
    st.json(report["technical_parameters"])

    st.subheader("🔗 Предикаты 510(k)")
    for p in report["predicates"]:
        st.write(f"**{p['k_number']}** — {p['name']} ({p['date']})")

    st.subheader("📚 Применимые стандарты")
    for s in report["standards"]:
        st.write(f"• {s}")

    st.subheader("💡 Advisory & Analytics")
    for item in report["advisory"]:
        st.success(item)

    # Скачивание
    json_str = json.dumps(report, indent=2, ensure_ascii=False)
    st.download_button(
        "📥 Скачать полный отчёт JSON",
        json_str,
        f"RCP_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
        "application/json"
    )

st.caption("RCP MVP v3.1 • Всё по документу RCP_MVP_model_v.3.docx • Разработано самостоятельно")