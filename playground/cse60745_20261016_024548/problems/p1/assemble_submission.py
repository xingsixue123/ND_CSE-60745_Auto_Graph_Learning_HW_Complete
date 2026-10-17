"""Assemble PLAYGROUND/submission.md from its parts."""
head = open("submission_head.md").read().rstrip() + "\n\n"
results = open("results_section.md").read().rstrip() + "\n\n"
tail = open("submission_tail.md").read().rstrip() + "\n"
open("submission.md", "w").write(head + results + tail)
print(f"submission.md: {len(open('submission.md').read().split())} words")
