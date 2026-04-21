import streamlit as st

st.set_page_config(page_title="Cardano CLI Tool", page_icon="🧰", layout="wide")

st.title("🧰 Cardano CLI Generator")
st.markdown("""
Welcome to your semi-automated Cardano CLI tool. 

**👈 Use the sidebar to navigate between modules:**
* **Wallet Creation:** Generate offline keys and build addresses.
* **Utilities:** Query the blockchain and create witness files.
* **Transaction Creation:** Build, sign, and submit transactions.
""")

st.divider()

# --- GLOBAL SETTINGS ---
st.subheader("🌐 Global Network Setting")
st.markdown("Select your network here. Select 'None' if you have your network exported in your `.zshrc`.")

if 'network_choice' not in st.session_state:
    st.session_state['network_choice'] = "Preview (Testnet)"

st.selectbox(
    "Select Network",
    ["Preview (Testnet)", "Preprod (Testnet)", "Mainnet", "None (Configured in shell)"],
    key='network_choice'
)

if st.session_state['network_choice'] == "Preview (Testnet)":
    st.session_state['network_flag'] = "--testnet-magic 2"
elif st.session_state['network_choice'] == "Preprod (Testnet)":
    st.session_state['network_flag'] = "--testnet-magic 1"
elif st.session_state['network_choice'] == "Mainnet":
    st.session_state['network_flag'] = "--mainnet"
else:
    st.session_state['network_flag'] = ""

st.success(f"Network globally set to: **{st.session_state['network_choice']}**")