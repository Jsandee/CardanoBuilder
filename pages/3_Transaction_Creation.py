import streamlit as st

st.set_page_config(page_title="Transaction Builder", page_icon="💸")

st.title("💸 Transaction Builder & Signer")

if 'network_flag' not in st.session_state:
    st.session_state['network_flag'] = "--testnet-magic 2"
network_flag = st.session_state['network_flag']

# Used for the unchanged signing/submit section
net_line = f" \\\n{network_flag}" if network_flag else ""

st.info(f"Current Network Flag: `{network_flag if network_flag else 'None'}`")
st.divider()

st.subheader("1. Build the Transaction")
st.markdown("Specify the UTXOs you are spending and where the funds are going.")

# --- 1. Multi line Input ---
tx_in_raw = st.text_area(
    "Input UTXOs (TxHash#Index)",
    placeholder="hash1#0\nhash2#1",
    help="Paste one UTXO per line",
    height=100
)

# --- 2. Change Address ---
sender_addr = st.text_input(
    "Sender / Change Address File",
    value="my_wallet.addr"
)

# --- 3. Multiline Output ---
receivers_raw = st.text_area(
    "Recipients (FileOrAddress:Lovelace)",
    value="receiver.addr:5000000\naddr_test1...:2000000",
    height=100
)

# --- 4. Optional Advanced Settings (Metadata & Signers) ---
st.markdown("**Optional Settings**")
metadata_file = st.text_input(
    "Metadata JSON File Name (Optional)",
    placeholder="credential_data.json",
    help="Leave blank if no metadata is needed."
)

required_signers_raw = st.text_area(
    "Required Signer Hashes (Optional)",
    placeholder="hash1\nhash2",
    help="One hash per line. Leave blank if not using smart contracts or multi-sig.",
    height=80
)

# --- 5. Generate Button ---
if st.button("Generate Build Command"):
    if tx_in_raw.strip() and sender_addr.strip():
        # Handle Change Address
        if sender_addr.strip().endswith(".addr"):
            sender_formatted = f"$(cat {sender_addr.strip()})"
        else:
            sender_formatted = sender_addr.strip()

        # Handle Multiple Inputs
        tx_ins = []
        for line in tx_in_raw.split('\n'):
            line = line.strip()
            if line:  # Ignore empty lines
                tx_ins.append(f"--tx-in {line}")

        # Handle Multiple Outputs
        tx_outs = []
        for line in receivers_raw.split('\n'):
            line = line.strip()
            if ':' in line:
                addr, amt = line.split(':', 1)
                addr = addr.strip()
                amt = amt.strip()

                if addr.endswith(".addr"):
                    addr_formatted = f"$(cat {addr})"
                else:
                    addr_formatted = addr

                tx_outs.append(f"--tx-out {addr_formatted}+{amt}")

        # Dynamically assemble the command as a list
        cmd_parts = ["cardano-cli latest transaction build"]
        cmd_parts.extend(tx_ins)
        if tx_outs:
            cmd_parts.extend(tx_outs)

        # Append Metadata if provided
        if metadata_file.strip():
            cmd_parts.append(f"--metadata-json-file {metadata_file.strip()}")

        # Append Required Signers if provided
        for line in required_signers_raw.split('\n'):
            line = line.strip()
            if line:
                cmd_parts.append(f"--required-signer-hash {line}")

        cmd_parts.append(f"--change-address {sender_formatted}")

        if network_flag:
            cmd_parts.append(network_flag)

        cmd_parts.append("--out-file tx.raw")

        # Join with backslash and newline
        cmd_build_str = " \\\n".join(cmd_parts)
        cmd_build = f"# 1. Build the raw transaction\n{cmd_build_str}"

        st.code(cmd_build, language="bash")
    else:
        st.warning("Please provide at least one Input UTXO and a Change Address.")

st.divider()

# --- UNCHANGED: SIGNING AND SUBMITTING ---
st.subheader("2. Sign & Submit")

col3, col4 = st.columns(2)
with col3:
    tx_body = st.text_input("Transaction Body File", value="tx.raw")
    skey_file = st.text_input("Signing Key File", value="my_wallet.skey")
with col4:
    tx_signed = st.text_input("Output Signed File", value="tx.signed")

if st.button("Generate Sign & Submit Commands"):
    cmd_sign = f"""# 2. Sign the transaction
cardano-cli latest transaction sign \\
--tx-body-file {tx_body.strip()} \\
--signing-key-file {skey_file.strip()}{net_line} \\
--out-file {tx_signed.strip()}"""

    cmd_submit = f"""# 3. Submit to the blockchain
cardano-cli latest transaction submit \\
--tx-file {tx_signed.strip()}{net_line}"""

    st.code(cmd_sign, language="bash")
    st.code(cmd_submit, language="bash")