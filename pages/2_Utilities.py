import streamlit as st

st.set_page_config(page_title="Utilities", page_icon="🛠️")

st.title("🛠️ Cardano CLI Utilities")
st.markdown("Quick commands using your **local file names**.")

if 'network_flag' not in st.session_state:
    st.session_state['network_flag'] = "--testnet-magic 2"
network_flag = st.session_state['network_flag']
net_line = f" \\\n{network_flag}" if network_flag else ""

st.info(f"Current Network Flag: `{network_flag if network_flag else 'None'}`")
st.divider()

# Added the fourth tab for Key Hash extraction
tab1, tab2, tab3, tab4 = st.tabs([
    "💰 Check Balance",
    "✍️ Create Witness",
    "🧩 Assemble Tx",
    "🔑 Get Key Hash"
])

with tab1:
    st.subheader("Query Address Balance")
    address_input = st.text_input("Address String OR File Name", value="my_wallet.addr")

    if address_input.strip():
        if address_input.endswith(".addr"):
            formatted_address = f"$(cat {address_input.strip()})"
        else:
            formatted_address = address_input.strip()

        cmd_utxo = f"""# Query UTXO using the address
cardano-cli latest query utxo --address {formatted_address} --output-text {net_line} """

        st.code(cmd_utxo, language="bash")

with tab2:
    st.subheader("Generate a Witness File")

    col1, col2 = st.columns(2)
    with col1:
        tx_body = st.text_input("Transaction Body File Name", value="tx.raw")
        skey_file = st.text_input("Signing Key File Name", value="my_wallet.skey")
    with col2:
        witness_out = st.text_input("Output Witness File Name", value="my_wallet.witness")

    if tx_body and skey_file and witness_out:
        cmd_witness = f"""# Create a transaction witness
cardano-cli latest transaction witness \\
--tx-body-file {tx_body.strip()} \\
--signing-key-file {skey_file.strip()}{net_line} \\
--out-file {witness_out.strip()}"""

        st.code(cmd_witness, language="bash")

with tab3:
    st.subheader("Assemble Transaction from Witnesses")
    st.markdown("Combine a transaction body with one or more witness files.")

    col3, col4 = st.columns(2)
    with col3:
        assemble_tx_body = st.text_input("Transaction Body File", value="tx.raw", key="assemble_tx_body")
        assemble_out_file = st.text_input("Output Signed File", value="tx.signed", key="assemble_out_file")
    with col4:
        witnesses_raw = st.text_area(
            "Witness Files",
            value="witness1.witness\nwitness2.witness",
            help="One witness file per line",
            height=100
        )

    if st.button("Generate Assemble Command"):
        if assemble_tx_body.strip() and assemble_out_file.strip() and witnesses_raw.strip():

            witness_flags = []
            for line in witnesses_raw.split('\n'):
                line = line.strip()
                if line:
                    witness_flags.append(f"--witness-file {line}")

            witness_str = " \\\n".join(witness_flags)

            cmd_assemble = f"""# Assemble the signed transaction
cardano-cli latest transaction assemble \\
--tx-body-file {assemble_tx_body.strip()} \\
{witness_str} \\
--out-file {assemble_out_file.strip()}"""

            st.code(cmd_assemble, language="bash")
        else:
            st.warning("Please provide the transaction body, output file, and at least one witness file.")

with tab4:
    st.subheader("Extract Key Hash")
    st.markdown(
        "Extract the raw hash from a verification key. This is required for the `--required-signer-hash` flag when building advanced transactions.")

    vkey_file = st.text_input("Verification Key File Name", value="my_wallet.vkey")

    if vkey_file.strip():
        cmd_hash = f"""# Get the Key Hash
cardano-cli latest address key-hash \\
--payment-verification-key-file {vkey_file.strip()}"""

        st.code(cmd_hash, language="bash")