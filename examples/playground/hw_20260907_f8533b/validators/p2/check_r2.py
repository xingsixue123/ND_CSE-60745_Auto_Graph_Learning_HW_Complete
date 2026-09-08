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

# Independent cross-check: the entry count must equal the number of virtual pages.
pages = 2**VA_BITS // PAGE
assert pages == ptes, "PTE count must equal (virtual address space / page size)"
print(f"cross-check: 2^{VA_BITS} B / {PAGE} B = {pages} virtual pages == {ptes} PTEs")

# Question C, pro 1: doubling the page size to 128 KB halves the page table.
PAGE_C   = 128 * 2**10
offset_c = int(math.log2(PAGE_C))
vpn_c    = VA_BITS - offset_c
size_c   = 2**vpn_c * PTE
assert size_c * 2 == size, "doubling the page size must halve the page table"
print(f"C: {PAGE_C // 2**10} KB page -> offset {offset_c}, VPN {vpn_c} bits, "
      f"table = 2^{vpn_c} x {PTE} B = {size_c // 2**10} KB "
      f"(half of {size // 2**10} KB)")
