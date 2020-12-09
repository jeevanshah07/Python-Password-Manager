originalStr = "('test'),"

print(originalStr)

originalStr = originalStr.replace('(', '') 
print(originalStr)
originalStr = originalStr.replace(')', '') 
print(originalStr)
originalStr = originalStr.replace("'", '') 
print(originalStr)
originalStr = originalStr.replace(",", '') 
print(originalStr)