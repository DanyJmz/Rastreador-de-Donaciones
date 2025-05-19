import streamlit as st
from blockchain import Blockchain
from models import Session, Donation, Disbursement, init_db
import time
import pandas as pd

init_db()
session = Session()
blockchain = Blockchain()
donaciones_previas = session.query(Donation).all()

for d in donaciones_previas:
    blockchain.add_block({'type': 'donación', 'donor': d.donor, 'amount': d.amount, 'campaign': d.campaign, 'timestamp': d.timestamp})
desembolsos_previos = session.query(Disbursement).all()

for r in desembolsos_previos:
    blockchain.add_block({'type': 'desembolso', 'campaign': r.campaign, 'recipient': r.recipient, 'amount': r.amount, 'timestamp': r.timestamp})
desembolsos_previos = session.query(Disbursement).all()

for r in desembolsos_previos:
    blockchain.add_block({'type': 'desembolso', 'campaign': r.campaign, 'recipient': r.recipient, 'amount': r.amount, 'timestamp': r.timestamp})

st.title("Rastreador de Donaciones")

st.header("Registrar una Donación")
with st.form("donate_form"):
    donor = st.text_input("Nombre del donante")
    amount = st.number_input("Cantidad (USD)", min_value=0.01, step=0.01)
    campaign = st.text_input("Nombre de la campaña")
    submitted = st.form_submit_button("Registrar Donación")
    if submitted:
        data = {'type': 'donación', 'donor': donor, 'amount': amount, 'campaign': campaign, 'timestamp': time.time()}
        block = blockchain.add_block(data)
        donation = Donation(donor=donor, amount=amount, campaign=campaign, timestamp=data['timestamp'], tx_hash=block.hash)
        session.add(donation)
        session.commit()
        st.success(f"Donación registrada con hash: {block.hash}")

st.header("Registrar un Desembolso")
with st.form("disburse_form"):
    campaign_d = st.text_input("Campaña para el desembolso")
    recipient = st.text_input("Nombre del beneficiario")
    amount_d = st.number_input("Cantidad desembolsada (USD)", min_value=0.01, step=0.01)
    submitted_d = st.form_submit_button("Registrar Desembolso")
    if submitted_d:
        data = {'type': 'desembolso', 'campaign': campaign_d, 'recipient': recipient, 'amount': amount_d, 'timestamp': time.time()}
        block = blockchain.add_block(data)
        disb = Disbursement(campaign=campaign_d, amount=amount_d, recipient=recipient, timestamp=data['timestamp'], tx_hash=block.hash)
        session.add(disb)
        session.commit()
        st.success(f"Desembolso registrado con hash: {block.hash}")

st.header("Panel de Control")

donations = session.query(Donation).all()
disbursements = session.query(Disbursement).all()

df_don = pd.DataFrame([{'ID': d.id, 'Donante': d.donor, 'Cantidad': d.amount, 'Campaña': d.campaign,
                        'Fecha y Hora': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(d.timestamp)), 'Hash': d.tx_hash}
                       for d in donations])

df_dis = pd.DataFrame([{'ID': r.id, 'Campaña': r.campaign, 'Beneficiario': r.recipient, 'Cantidad': r.amount,
                        'Fecha y Hora': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(r.timestamp)), 'Hash': r.tx_hash}
                       for r in disbursements])

tabs = st.tabs(["Donaciones", "Desembolsos", "Blockchain"])
with tabs[0]:
    st.dataframe(df_don if not df_don.empty else pd.DataFrame([{"Info": "No hay donaciones registradas."}]))
with tabs[1]:
    st.dataframe(df_dis if not df_dis.empty else pd.DataFrame([{"Info": "No hay desembolsos registrados."}]))
with tabs[2]:
    chain_df = pd.DataFrame(blockchain.to_dict())
    st.dataframe(chain_df)
