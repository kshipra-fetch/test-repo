import csv
from datetime import datetime

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
        
        # Define age groups based on UK voting laws
        def categorize_voting_status(age):
            if age < 16:
                return "Ineligible (0-15)"
            elif age >= 18:
                return "Eligible (18+)"
            else:
                return "Soon Eligible (16-17)"
        
        # Categorize voting status
        for person in data:
            person['Voting_Status'] = categorize_voting_status(person['Age'])
        
        # Count individuals in each category
        voting_counts = {}
        for person in data:
            status = person['Voting_Status']
            voting_counts[status] = voting_counts.get(status, 0) + 1
        
        # Calculate percentages
        total_individuals = len(data)
        voting_percentages = {}
        for status, count in voting_counts.items():
            voting_percentages[status] = round((count / total_individuals) * 100, 2)
        
        # Get age statistics
        ages = [person['Age'] for person in data]
        avg_age = sum(ages) / len(ages)
        min_age = min(ages)
        max_age = max(ages)
        
        # City-wise analysis
        city_counts = {}
        for person in data:
            city = person['City']
            city_counts[city] = city_counts.get(city, 0) + 1
        
        # Sort cities by count
        sorted_cities = sorted(city_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Generate detailed report
        report = f"""
UK VOTING DEMOGRAPHICS ANALYSIS
===============================
Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

DATASET OVERVIEW:
----------------
Total Individuals: {total_individuals}
Cities Represented: {len(city_counts)}

VOTING ELIGIBILITY BREAKDOWN:
----------------------------
"""
        
        for status, count in voting_counts.items():
            percentage = voting_percentages[status]
            report += f"{status}: {count} individuals ({percentage}%)\n"
        
        report += f"""
AGE STATISTICS:
--------------
Average Age: {round(avg_age, 2)} years
Youngest Individual: {min_age} years
Oldest Individual: {max_age} years
Age Range: {max_age - min_age} years

TOP 10 CITIES BY POPULATION:
---------------------------
"""
        
        for city, count in sorted_cities:
            report += f"{city}: {count} individuals\n"
        
        report += f"""
DETAILED AGE GROUP ANALYSIS:
---------------------------
"""
        
        # Detailed age group analysis
        age_groups = {
            'Children (0-15)': len([p for p in data if p['Age'] < 16]),
            'New Voters (16-17)': len([p for p in data if 16 <= p['Age'] < 18]),
            'Young Adults (18-25)': len([p for p in data if 18 <= p['Age'] <= 25]),
            'Adults (26-65)': len([p for p in data if 25 < p['Age'] <= 65]),
            'Seniors (65+)': len([p for p in data if p['Age'] > 65])
        }
        
        for group, count in age_groups.items():
            percentage = round((count / total_individuals) * 100, 2)
            report += f"{group}: {count} individuals ({percentage}%)\n"
        
        report += f"""
POLICY IMPACT ANALYSIS:
---------------------
With the new voting age of 16+:
- Previously ineligible voters (16-17): {age_groups['New Voters (16-17)']} individuals
- This represents a {round((age_groups['New Voters (16-17)'] / total_individuals) * 100, 2)}% increase in eligible voters

CONCLUSION:
----------
This analysis shows the demographic distribution of voting-eligible individuals
in the UK city sample, highlighting the impact of the recent voting age change
from 18+ to 16+.
"""
        
        # Save the report
        with open('/data/output/result.txt', 'w') as f:
            f.write(report)
        
        print("Analysis completed successfully!")
        print(f"Report saved to /data/output/result.txt")
        
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
