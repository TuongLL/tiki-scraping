import csv 
  
# open input CSV file as source 
# open output CSV file as result 
with open("combined_file.csv", "r") as source: 
    reader = csv.reader(source) 
      
    with open("output.csv", "w") as result: 
        writer = csv.writer(result) 
        for r in reader: 
            
            # Use CSV Index to remove a column from CSV 
            #r[3] = r['year'] 
            writer.writerow((r[0],r[2]))