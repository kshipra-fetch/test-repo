import csv
import json

def analyze_demographics():
    """
    Simple demographics analysis - count people in each age group
    """
    
    try:
        # Read the dataset
        print("Reading demographic data...")
        
        data = []
        with open('/data/inputs/demographics-data.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                try:
                    age = int(row['Age'])
                    data.append({
                        'Name': row['Name'],
                        'Age': age
                    })
                except (ValueError, KeyError):
                    continue  # Skip invalid rows
        
        print(f"Total individuals in dataset: {len(data)}")
        
        if len(data) == 0:
            print("Error: No valid data found in the dataset")
            return
        
        # Count individuals in each age group
        children = 0      # 0-12
        teens = 0         # 13-17
        adults = 0        # 18-64
        seniors = 0       # 65+
        
        for person in data:
            age = person['Age']
            if age <= 12:
                children += 1
            elif age <= 17:
                teens += 1
            elif age <= 64:
                adults += 1
            else:
                seniors += 1
        
        total = len(data)
        
        # Create JSON result
        result = {
            "total_individuals": total,
            "age_groups": {
                "children": {
                    "count": children,
                    "percentage": round((children/total)*100, 1),
                    "age_range": "0-12"
                },
                "teens": {
                    "count": teens,
                    "percentage": round((teens/total)*100, 1),
                    "age_range": "13-17"
                },
                "adults": {
                    "count": adults,
                    "percentage": round((adults/total)*100, 1),
                    "age_range": "18-64"
                },
                "seniors": {
                    "count": seniors,
                    "percentage": round((seniors/total)*100, 1),
                    "age_range": "65+"
                }
            },
            "summary": f"Analysis of {total} individuals across 4 age groups"
        }
        
        # Save JSON result
        with open('/data/outputs/result.json', 'w') as f:
            json.dump(result, f, indent=2)
        
        # Also save as text for compatibility
        with open('/data/outputs/result.txt', 'w') as f:
            f.write(json.dumps(result, indent=2))
        
        print("Analysis completed successfully!")
        
        # PRINT the JSON result - this is what gets captured
        print("\n=== DEMOGRAPHICS ANALYSIS RESULT ===")
        print(json.dumps(result, indent=2))
        print("=== END RESULT ===")
        
    except Exception as e:
        error_msg = f"Error during analysis: {str(e)}"
        print(error_msg)
        
        # Save error report
        with open('/data/outputs/error.txt', 'w') as f:
            f.write(error_msg)

if __name__ == "__main__":
    analyze_demographics()
