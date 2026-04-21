import streamlit as st

st.set_page_config(page_title="Wallet Creation", page_icon="👛")

st.title("👛 Cardano Wallet Creator")
st.markdown("Generate your offline keys and compile your wallet address.")

if 'network_flag' not in st.session_state:
    st.session_state['network_flag'] = "--testnet-magic 2"
network_flag = st.session_state['network_flag']

# Cleanly handle the backslash if the flag is empty
net_line = f" \\\n{network_flag}" if network_flag else ""

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        wallet_name = st.text_input("Wallet Name Prefix", value="my_wallet")
    with col2:
        st.info(f"Current Network Flag: `{network_flag if network_flag else 'None'}`")

    enable_staking = st.checkbox("Include Stake Key", value=False)

st.divider()
st.subheader("📋 Generated Commands")

if wallet_name.strip() == "":
    st.warning("Please enter a valid Wallet Name Prefix.")
else:
    name = wallet_name.strip()

    cmd = f"""# 1. Generate Payment Keys
cardano-cli latest address key-gen \\
--verification-key-file {name}.vkey \\
--signing-key-file {name}.skey
"""

    if enable_staking:
        cmd += f"""
# 2. Generate Stake Keys
cardano-cli latest stake-address key-gen \\
--verification-key-file {name}_stake.vkey \\
--signing-key-file {name}_stake.skey

# 3. Build Address (With Stake Key Linked)
cardano-cli latest address build \\
--payment-verification-key-file {name}.vkey \\
--stake-verification-key-file {name}_stake.vkey \\
--out-file {name}.addr{net_line}
"""
    else:
        cmd += f"""
# 2. Build Address (No Stake Key)
cardano-cli latest address build \\
--payment-verification-key-file {name}.vkey \\
--out-file {name}.addr{net_line}
"""
    st.code(cmd, language="bash")