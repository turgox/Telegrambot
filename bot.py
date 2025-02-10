import os
from web3 import Web3
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Telegram Bot API Key (Verdiğiniz Telegram API anahtarını burada kullanıyoruz)
API_KEY = 'Api Key'  # Kendi bot API'nizi buraya ekledim

# Halk erişimine açık RPC Bağlantıları (Mainnet Ağları)
w3_connections = {
    'ethereum': Web3(Web3.HTTPProvider('https://cloudflare-eth.com/')),
    'bsc': Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/')),
    'polygon': Web3(Web3.HTTPProvider('https://polygon-rpc.com/')),
    'avalanche': Web3(Web3.HTTPProvider('https://api.avax.network/ext/bc/C/rpc')),
    'fantom': Web3(Web3.HTTPProvider('https://rpcapi.fantom.network/')),
    'arbitrum': Web3(Web3.HTTPProvider('https://arb1.arbitrum.io/rpc')),
    'optimism': Web3(Web3.HTTPProvider('https://mainnet.optimism.io/')),
    'xdai': Web3(Web3.HTTPProvider('https://xdai.poanetwork.dev/')),
    'cronos': Web3(Web3.HTTPProvider('https://evm-cronos.crypto.org')),
    'moonbeam': Web3(Web3.HTTPProvider('https://rpc.api.moonbeam.network')),
    'celo': Web3(Web3.HTTPProvider('https://forno.celo.org')),
    'heco': Web3(Web3.HTTPProvider('https://http-mainnet.hecochain.com')),
    'base': Web3(Web3.HTTPProvider('https://mainnet.base.org')),
    'mantle': Web3(Web3.HTTPProvider('https://rpc.mantlenetwork.io')),
    'klaytn': Web3(Web3.HTTPProvider('https://public-node-api.klaytn.foundation')),
    'iotex': Web3(Web3.HTTPProvider('https://rpc.iotex.io')),
    'okexchain': Web3(Web3.HTTPProvider('https://exchainrpc.okex.org')),
    'moonriver': Web3(Web3.HTTPProvider('https://rpc.moonbeam.network/moonriver')),
    'shiden': Web3(Web3.HTTPProvider('https://rpc.shiden.network')),
    'opbnb': Web3(Web3.HTTPProvider('https://rpc.opbnb.org')),
    'zksync': Web3(Web3.HTTPProvider('https://zksync2-mainnet.zksync.io/')),
    'scroll': Web3(Web3.HTTPProvider('https://mainnet.scroll.io/')),
    'astar': Web3(Web3.HTTPProvider('https://astar.network/rpc')),
    'evmos': Web3(Web3.HTTPProvider('https://evmos.org/rpc')),
    'oasis': Web3(Web3.HTTPProvider('https://emerald.oasis.dev/')),
    'soneium': Web3(Web3.HTTPProvider('https://rpc.soneium.network/')),
    'ink': Web3(Web3.HTTPProvider('https://rpc.inknetwork.io/')),
    'optimistic_ethereum': Web3(Web3.HTTPProvider('https://mainnet.optimism.io/')),
    'telos': Web3(Web3.HTTPProvider('https://rpc2.telos.net/')),
    'wax': Web3(Web3.HTTPProvider('https://wax.greymass.com/')),
    'ethereum_classic': Web3(Web3.HTTPProvider('https://ethereum-classic.rpcpool.com/')),
    'palm': Web3(Web3.HTTPProvider('https://palm-mainnet-1.publicnode.com/')),
    'boba': Web3(Web3.HTTPProvider('https://mainnet.boba.network/')),
    'fuse': Web3(Web3.HTTPProvider('https://rpc.fuse.io/')),
    'polygon_zkevm': Web3(Web3.HTTPProvider('https://zkevm-rpc.polygon.technology/')),
    'starknet': Web3(Web3.HTTPProvider('https://rpc.starknet.io/')),
    'velas': Web3(Web3.HTTPProvider('https://evmexplorer.velas.com/')),
    'ronin': Web3(Web3.HTTPProvider('https://api.roninchain.com/rpc')),
    'solana': Web3(Web3.HTTPProvider('https://api.mainnet-beta.solana.com/')),
    'harmony': Web3(Web3.HTTPProvider('https://api.s0.t.hmny.io')),
}

# Token İsimleri (Ağların tokenları)
token_names = {
    'ethereum': 'ETH',
    'bsc': 'BNB',
    'polygon': 'MATIC',
    'avalanche': 'AVAX',
    'fantom': 'FTM',
    'arbitrum': 'ETH',
    'optimism': 'ETH',
    'xdai': 'XDAI',
    'cronos': 'CRO',
    'moonbeam': 'GLMR',
    'celo': 'CELO',
    'heco': 'HT',
    'base': 'ETH',
    'mantle': 'ETH',
    'klaytn': 'KLAY',
    'iotex': 'IOTX',
    'okexchain': 'OKT',
    'moonriver': 'MOVR',
    'shiden': 'SDN',
    'opbnb': 'BNB',
    'zksync': 'ETH',
    'scroll': 'ETH',
    'astar': 'ASTR',
    'evmos': 'EVMT',
    'oasis': 'ROSE',
    'soneium': 'SONE',
    'ink': 'INK',
    'optimistic_ethereum': 'ETH',
    'telos': 'TLOS',
    'wax': 'WAXP',
    'ethereum_classic': 'ETC',
    'palm': 'PALM',
    'boba': 'ETH',
    'fuse': 'FUSE',
    'polygon_zkevm': 'MATIC',
    'starknet': 'ETH',
    'velas': 'VLX',
    'ronin': 'RON',
    'solana': 'SOL',
    'harmony': 'ONE',
}

# Cüzdan bakiyesi almak için fonksiyon
def get_balance(address: str):
    total_balance = 0
    balances = {}

    for network, w3 in w3_connections.items():
        try:
            balance = w3.eth.get_balance(address)
            token_balance = w3.fromWei(balance, 'ether')
            balances[network] = f'{token_balance:.4f} {token_names[network]}'
            total_balance += token_balance
        except Exception as e:
            balances[network] = f"Error: {str(e)}"

    return total_balance, balances

# Telegram bot komutları
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Merhaba! Cüzdan bakiyesi öğrenmek için cüzdan adresinizi yazın.'
    )

def balance(update: Update, context: CallbackContext) -> None:
    address = ' '.join(context.args)

    if not Web3.isAddress(address):
        update.message.reply_text("Geçersiz cüzdan adresi.")
        return

    total_balance, balances = get_balance(address)
    balances_msg = "\n".join([f"{network}: {balance}" for network, balance in balances.items()])

    # Revoke linkini kontrol et
    revoke_link = f"https://revoke.cash/{address}"

    # Botun mesajı
    message = f"🌐 **Cüzdan Bakiyesi**\n\n" \
              f"**Cüzdan Adresi**: `{address}`\n" \
              f"**Toplam Bakiye**: {total_balance:.4f} ETH\n\n" \
              f"**Ağlar**:\n" \
              f"{balances_msg}\n\n"

    # Revoke linki ekleme
    message += f"🔒 Eğer izinlerinizi iptal etmek isterseniz, [Revoke.cash](https://revoke.cash/{address}) üzerinden işleminizi yapabilirsiniz."

    update.message.reply_text(message, parse_mode='Markdown')

def main():
    updater = Updater(API_KEY, use_context=True)

    # Komutlar
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("balance", balance))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
