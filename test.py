import os
import openai
import re

# openai.api_key = ""

# response = openai.Completion.create(
#   model="text-davinci-003",
#   prompt="Describe Van Gogh's star moon night in 50 words",
#   temperature=0.3,
#   max_tokens=60,
#   top_p=1.0,
#   frequency_penalty=0.0,
#   presence_penalty=0.0
# )

# print(response["choices"][0]["text"])
str1 = "abc"
str2 = "re,abc,npu"
# # 在正规表达式str2中寻找str1是否能匹配到，flag默认设置为0
# print(re.search(str1, str2))
# # 返回匹配到的起止位置
# print(re.search(str1, str2).span())
# # 返回匹配的内容
# print(re.search(str1, str2).group())

rule1 = '(.*) are (.*?) .*'
str3 = "Cats are smarter than dogs";
 
# searchObj = re.search(rule1, str3)
 
# print("searchObj.group() : ", searchObj.group())
# print("searchObj.group(1) : ", searchObj.group(1))
# print("searchObj.group(2) : ", searchObj.group(2))

str4 = "www"
str5 = "cn"
str6 = "www.nwpu.edu.cn"
# print(re.match(str4, str6))
# print(re.match(str4, str6).span())
# print(re.match(str5, str6))
# print(re.match(str5, str6).span())

phone = "114-5141-9198 # 这可能是一个电话号码"
 
# 删除字符串中的 Python注释 
# num = re.sub(r'#.*$', "", phone)
# print("电话号码是: ", num)
 
# # 删除非数字的字符串（e.g. '-'） 
# num = re.sub(r'\D', "", phone)
# print("去掉'-'的电话号码是 : ", num)

str7 = "set width=20 and height=10"
rule2 = "(\w+)=(\d+)"
# findall匹配所有
# print(re.findall(rule2, str7))
# # search匹配一次
# print(re.search(rule2, str7))

str8 = "abcABC"
str1 = "abc"
print(re.findall(str1, str8))
print(re.findall(str1, str8, re.I))
