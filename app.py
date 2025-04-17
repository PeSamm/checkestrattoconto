import streamlit as st
import pandas as pd

st.set_page_config(page_title="Confronta Mastrino vs Estratto Conto", layout="centered")

st.title("📊 Confronta Mastrino e Estratto Conto")
st.write("Carica i due file Excel per confrontare gli **importi** (cifre).")

# Caricamento file
file1 = st.file_uploader("📁 Carica il Mastrino (Excel)", type=["xlsx"])
file2 = st.file_uploader("📁 Carica l'Estratto Conto (Excel)", type=["xlsx"])

if file1 and file2:
    try:
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)

        st.success("File caricati con successo!")

        # Seleziona la colonna con gli importi
        st.write("### 1️⃣ Seleziona la colonna con le cifre:")
        col1 = st.selectbox("Colonna cifre - Mastrino", df1.columns)
        col2 = st.selectbox("Colonna cifre - Estratto Conto", df2.columns)

        if st.button("🔍 Confronta Importi"):
            importi1 = df1[col1].dropna().astype(float)
            importi2 = df2[col2].dropna().astype(float)

            # Trova differenze
            diff1 = importi1[~importi1.isin(importi2)]
            diff2 = importi2[~importi2.isin(importi1)]

            st.write("### ❌ Importi presenti **solo nel Mastrino**:")
            st.dataframe(diff1)

            st.write("### ❌ Importi presenti **solo nell'Estratto Conto**:")
            st.dataframe(diff2)

            # Salvataggio differenze in Excel
            with pd.ExcelWriter("differenze_output.xlsx", engine='openpyxl') as writer:
                diff1.to_frame(name="Solo nel Mastrino").to_excel(writer, sheet_name="Solo nel Mastrino", index=False)
                diff2.to_frame(name="Solo nell'Estratto Conto").to_excel(writer, sheet_name="Solo nell'Estratto Conto", index=False)

            with open("differenze_output.xlsx", "rb") as f:
                st.download_button("⬇️ Scarica Differenze in Excel", data=f, file_name="differenze.xlsx")

    except Exception as e:
        st.error(f"Errore durante la lettura dei file: {e}")
