"""p2: verify the virtual-memory arithmetic. Run: python3 check.py"""
import math

VA_BITS   = 30
PAGE      = 64 * 2**10   # 64 KB, binary units (page 1, item 4)
PTE       = 4            # bytes
PHYS      = 2 * 2**30    # 2 GB

offset = int(math.log2(PAGE));  assert 2**offset == PAGE
vpn    = VA_BITS - offset
ptes   = 2**vpn
size   = ptes * PTE

assert offset + vpn == VA_BITS, "offset+VPN must equal the stated 30-bit total"
print(f"A: page offset = {offset} bits, VPN = {vpn} bits, total = {offset+vpn} bits")
print(f"B: PTEs = 2^{vpn} = {ptes} entries")
print(f"B: page table = 2^{vpn} x {PTE} B = 2^{int(math.log2(size))} B "
      f"= {size // 2**10} KB")

ppn = int(math.log2(PHYS)) - offset
print(f"sanity: PPN = {ppn} bits, fits in {PTE*8}-bit PTE with flags: {ppn < PTE*8}")
print(f"sanity: page table is exactly one page: {size == PAGE}")
