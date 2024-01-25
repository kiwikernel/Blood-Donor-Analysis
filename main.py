from donorlib import tools as t

try: t.pullcsv()
except Exception as e: print(e)

print("completed")