from donorlib import tools as t
x = 0

try: 
    t.pullcsv()
    t.pullparquet()
    # while x < 3:
    #     t.send2group()
    #     x += 1
    t.nationaltrend_viz()
    t.statetrend_viz()
    t.retention_viz()
    t.donormap_viz()
    
    print("successful")

except Exception as e: print(e)

print("completed")