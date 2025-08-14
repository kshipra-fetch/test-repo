import csv

def analyze_voting_demographics():
    """
    Analyze UK voting demographics based on age groups.
    Old voting age: 18+
    New voting age: 16+
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
                        'Age': age,
                        'City': row['City']
                    })
                except (ValueError, KeyError):
                    continue  # Skip invalid rows
        
        print(f"Total individuals in dataset: {len(data)}")
        
        if len(data) == 0:
            return "Error: No valid data found in the dataset"
        
        # Count individuals in each voting category
        ineligible = 0  # 0-15
        soon_eligible = 0  # 16-17
        eligible = 0  # 18+
        
        for person in data:
            age = person['Age']
            if age < 16:
                ineligible += 1
            elif age < 18:
                soon_eligible += 1
            else:
                eligible += 1
        
        total = len(data)
        
        # Generate simple report
        report = f"""
UK VOTING DEMOGRAPHICS ANALYSIS
===============================

DATASET OVERVIEW:
----------------
Total Individuals: {total}

VOTING ELIGIBILITY BREAKDOWN:
----------------------------
Ineligible (0-15): {ineligible} individuals ({round((ineligible/total)*100, 1)}%)
Soon Eligible (16-17): {soon_eligible} individuals ({round((soon_eligible/total)*100, 1)}%)
Eligible (18+): {eligible} individuals ({round((eligible/total)*100, 1)}%)

AGE STATISTICS:
--------------
Average Age: {round(sum(p['Age'] for p in data) / total, 1)} years
Youngest: {min(p['Age'] for p in data)} years
Oldest: {max(p['Age'] for p in data)} years

POLICY IMPACT:
-------------
With new voting age of 16+:
- New eligible voters (16-17): {soon_eligible} individuals
- This represents {round((soon_eligible/total)*100, 1)}% increase in eligible voters

CONCLUSION:
----------
This analysis shows the impact of changing UK voting age from 18+ to 16+.
"""
        
        # Save the report
        with open('/data/output/result.txt', 'w') as f:
            f.write(report)
        
        print("Analysis completed successfully!")
        return report
        
    except Exception as e:
        error_msg = f"Error during analysis: {str(e)}"
        print(error_msg)
        
        # Save error report
        with open('/data/output/error.txt', 'w') as f:
            f.write(error_msg)
        
        return error_msg

if __name__ == "__main__":
    analyze_voting_demographics()
