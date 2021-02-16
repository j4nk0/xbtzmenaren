import sys

with open('/run/litecoin_tx', 'w') as f:
    f.write(sys.argv[1] + '*')

