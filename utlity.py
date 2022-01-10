import re
import simplejson as json

import findspark
findspark.init()

def extract_number(value):
    result = ''.join(re.findall(r"[-+]?\d*\.\d+|\d+", value))
    return result

s = "업태명"

# naver_obj = NaverEncoder().encode(naver)
encoded_data = json.dumps(s, ensure_ascii=False, encoding="utf-8")
print(encoded_data)