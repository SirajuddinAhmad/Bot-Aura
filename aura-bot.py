import os
import time
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

# 1. Konfigurasi Jaringan LitVM & Wallet
RPC_LITVM = os.getenv("RPC_LITVM", "https://caldera.xyz")
CHAIN_ID_LITVM = 4441
PRIVATE_KEY = os.getenv("EVM_PRIVATE_KEY")

w3 = Web3(Web3.HTTPProvider(RPC_LITVM))
account = w3.eth.account.from_key(PRIVATE_KEY)

# 2. Alamat Router & Raw Input Data dari Transaksi Manual yang Sukses
# Ganti dengan alamat lengkap dari kolom "Interacted with contract" (0xF664B569...)
ROUTER_ADDRESS = w3.to_checksum_address("0xF664B56933f3cF0d7d69982b5A8eC90000000000") 

# TEMPELKAN RAW INPUT DATA (0x...) DARI TRANSAKSI SUKSES DI SINI:
RAW_INPUT_DATA = "0x_tempel_raw_input_data_transaksi_sukses_di_sini"

def jalankan_raw_swap():
    if "tempel" in RAW_INPUT_DATA:
        print("[!] ERROR: Harap tempelkan Raw Input Data (0x...) dari transaksi sukses Anda terlebih dahulu!")
        return

    nonce = w3.eth.get_transaction_count(account.address, "pending")
    hitungan = 1

    print(f"Memulai Auto-Swap LitVM setiap 10 detik | Wallet: {account.address}")
    print("Tekan Ctrl+C untuk berhenti.\n")

    while True:
        try:
            # Simulasi transaksi terlebih dahulu untuk memastikan tidak akan Failed
            tx_params = {
                "chainId": CHAIN_ID_LITVM,
                "from": account.address,
                "to": ROUTER_ADDRESS,
                "value": 0, # Ubah jika transaksi manual Anda mengirim zkLTC (Value > 0)
                "data": RAW_INPUT_DATA,
                "gasPrice": int(w3.eth.gas_price * 1.15),
                "nonce": nonce,
            }

            # Hitung estimasi gas otomatis agar tidak Out of Gas
            estimated_gas = w3.eth.estimate_gas(tx_params)
            tx_params["gas"] = int(estimated_gas * 1.25)

            signed_tx = w3.eth.account.sign_transaction(tx_params, PRIVATE_KEY)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

            print(f"[LitVM Swap #{hitungan}] SUKSES Terkirim | Nonce: {nonce} | Hash: {w3.to_hex(tx_hash)}")

            nonce += 1
            hitungan += 1

        except Exception as e:
            print(f"[!] Simulasi Gagal (Transaksi dibatalkan agar tidak Failed di explorer): {e}")
            nonce = w3.eth.get_transaction_count(account.address, "pending")

        time.sleep(10)

if __name__ == "__main__":
    jalankan_raw_swap()
