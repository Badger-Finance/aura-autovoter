# Used URLs
BALANCER_GQL_URL = "https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-v2"
HIDDEN_HAND_BRIBES_GQL_URL = "https://api.thegraph.com/subgraphs/name/badger-finance/aura-bribes"
SNAPSHOT_VOTE_API = "https://hub.snapshot.org/api/msg"
SNAPSHOT_GQL_API_URL = "https://hub.snapshot.org/graphql"

# Secrets
ETHNODEURL_SECRET_ID = "quiknode/eth-node-url"
ETHNODEURL_SECRET_KEY = "NODE_URL"

DISCORD_WEBHOOK_SECRET_ID = "aura-voter/discord-webhook"
DISCORD_WEBHOOK_SECRET_KEY = "DISCORD_WEBHOOK_URL"

REGION = "us-west-1"
# TODO: Fill in proper assume role once IaC is applied
AURA_VOTER_SECRET_ID = "/cvxvoter/private"
AURA_VOTER_SECRET_KEY = "VOTER"
ASSUME_ROLE_ARN = "arn:aws:iam::747584148381:role/cvxvoter20211004170419945600000002"


# Treasury wallets
VOTER_ADDRESS = "0xA9ed98B5Fb8428d68664f3C5027c62A10d45826b"
IBBTC_ADDRESS = "0x41671BA1abcbA387b9b2B752c205e22e916BE6e3"
TREASURY_VAULT_ADDRESS = "0xd0a7a8b98957b9cd3cfb9c0425abe44551158e9e"
TREASURY_OPS_ADDRESS = "0x042b32ac6b453485e357938bdc38e0340d4b9276"
DEV_MULTISIG_ADDRESS = "0xb65cef03b9b89f99517643226d76e286ee999e77"
TECHOPS_ADDRESS = "0x86cbD0ce0c087b482782c181dA8d191De18C8275"

TREASURY_WALLETS = [
    VOTER_ADDRESS,
    IBBTC_ADDRESS,
    TREASURY_OPS_ADDRESS,
    TREASURY_VAULT_ADDRESS,
    DEV_MULTISIG_ADDRESS,
]


# Balancer Addresses
BALANCER_VAULT_ADDRESS = "0xBA12222222228d8Ba445958a75a0704d566BF2C8"
BALANCER_LIQUIDITY_GAUGE_FACTORY = "0x4E7bBd911cf1EFa442BC1b2e9Ea01ffE785412EC"
# Badger voter voter_address. Delegated
# TODO: Change once known
BADGER_VOTER_ADDRESS = "0x14F83fF95D4Ec5E8812DDf42DA1232b0ba1015e6"

# Tokens
BADGER = "0x3472A5A71965499acd81997a54BBA8D852C6E53d"
AURA = "0xc0c293ce456ff0ed870add98a0828dd4d2903dbf"
GRAVIAURA = "0xBA485b556399123261a5F9c95d413B4f93107407"

# Misc
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
BOT_USERNAME = "Aura Autovoter Bot"
SNAPSHOT_MIN_AMOUNT_POOLS = 10
SNAPSHOT_STATE_ACTIVE = "active"
SNAPSHOT_AURA_OGTEST = "OG test"
CURRENCY_USD = "usd"

CG_ETHEREUM_CHAIN_ID = "ethereum"


# Voting addresses
AURA_LOCKER_ADDRESS = "0x3Fa73f1E5d8A792C80F426fc8F84FBF7Ce9bBCAC"
# Badger graviaura locker address
BADGER_LOCKER_ADDRESS = "0x3c0989ef27e3e3fab87a2d7c38b35880c90e63b5"

# Snapshot pool name mappings
BADGER_WBTC_POOL_NAME = "80/20 BADGER/WBTC"
AURABAL_GRAVIAURA_WETH_POOL_NAME = "33/33/33 graviAURA/auraBAL/WETH"

# Some core pools
META_WSTETH_WETH = "MetaStable wstETH/WETH"
BOOBA_TRI_STABLE = "bb-a-USDT/bb-a-DAI/bb-a-USDC"
WBTC_DIGG_GRAVIAURA = "40/40/20 WBTC/DIGG/graviAURA"
WMATIC_STMATIC = "p-MetaStable WMATIC/stMATIC"

POOL_ID_TO_NAME_MAP = {
    '0x0578292cb20a443ba1cde459c985ce14ca2bdee5000100000000000000000269':
        AURABAL_GRAVIAURA_WETH_POOL_NAME,
    '0xb460daa847c45f1c4a41cb05bfb3b51c92e41b36000200000000000000000194': BADGER_WBTC_POOL_NAME,
    # TODO: Add real name for digg pool once it's out on Snapshot
    '0x8eb6c82c3081bbbd45dcac5afa631aac53478b7c000100000000000000000270': WBTC_DIGG_GRAVIAURA,
    '0x32296969ef14eb0c6d29669c550d4a0449130230000200000000000000000080': META_WSTETH_WETH,
    '0x7b50775383d3d6f0215a8f290f2c9e2eebbeceb20000000000000000000000fe': (
        BOOBA_TRI_STABLE
    ),
}

POOL_NAME_TO_ID_MAP = {v: k for k, v in POOL_ID_TO_NAME_MAP.items()}
