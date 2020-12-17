testnet name: rinkeby -do not use
testnet name: ropsten
to get config file: geth --testnet dumpconfig > geth.conf
run with config: geth --config geth.conf

working nodes:
geth --testnet --syncmode "fast" --bootnodes "enode://6332792c4a00e3e4ee0926ed89e0d27ef985424d97b6a45bf0f23e51f0dcb5e66b875777506458aea7af6f9e4ffb69f43f3778ee73c81ed9d34c51c4b16b0b0f@52.232.243.152:30303,enode://94c15d1b9e2fe7ce56e458b9a3b672ef11894ddedd0c6f247e0f1d3487f52b66208fb4aeb8179fce6e3a749ea93ed147c37976d67af557508d199d9594c35f09@192.81.208.223:30303" dumpconfig > geth.conf

then:
geth --config geth.conf

to remove database:
geth --testnet removedb

geth wont synchronize - needs SSD HDD -> use INFURA / ETHERSCAN

INFURA:
EMAIL:jan.gajdica@gmail.com
PASSWORD:jngjdc676In3ff1c4c10u5n355
PROJECT:xbtzmenaren
