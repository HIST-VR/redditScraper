import re

title = 'Parents and sister of Christa Macauliffe watching the space shuttle Challenger explode at the Kennedy Space Center, January, 1986. [640x723]'
title2 = title

if title[-1] == "]":
    no_res = re.sub(r"\[.*?]", "[]", title)  # strip the resolution
    title = re.sub(r"[[\]]", "", no_res)  # strip the brackets

title2 = re.sub(r"\[.*?]", "", title2)

print(title)
print(title2)
