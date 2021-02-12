import sys

with open('/run/litecoin_block', 'w') as f:
    f.write(sys.argv[1] + '*')

