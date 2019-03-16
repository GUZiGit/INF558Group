import re

content = 'shit shi???t <ab> <Tag> something </Tag> shit shit'
outcomes = re.findall(r'(<Tag>)(.*)(</Tag>)',content)

print(outcomes[0][1])
print(outcomes)
