from donorlib import tools as t

try: 
    # t.pullcsv()
    # t.pullparquet()
    t.send2group()

except Exception as e: print(e)

print("completed")