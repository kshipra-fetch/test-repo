import pandas as pd
import numpy as np
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
        data = pd.read_csv('/data/dataset.txt')
        
        # Convert Age to numeric, handling any potential issues
        data['Age'] = pd.to_numeric(data['Age'], errors='coerce')
        
        # Remove any rows with invalid ages
        data = data.dropna(subset=['Age'])
        
        print(f"Total individuals in dataset: {len(data)}")
        
        # Define age groups based on UK voting laws
        def categorize_voting_status(age):
            if age < 16:
                return "Ineligible (0-15)"
            elif age >= 18:
                return "Eligible (18+)"
            else:
                return "Soon Eligible (16-17)"
        
        # Add voting status category
        data['Voting_Status'] = data['Age'].apply(categorize_voting_status)
        
        # Count individuals in each category
        voting_counts = data['Voting_Status'].value_counts()
        
        # Calculate percentages
        total_individuals = len(data)
        voting_percentages = (voting_counts / total_individuals * 100).round(2)
        
        # Get age distribution details
        age_stats = {
            'Average Age': round(data['Age'].mean(), 2),
            'Median Age': round(data['Age'].median(), 2),
            'Youngest': int(data['Age'].min()),
            'Oldest': int(data['Age'].max()),
            'Age Range': int(data['Age'].max() - data['Age'].min())
        }
        
        # City-wise analysis
        city_counts = data['City'].value_counts().head(10)
        
        # Generate detailed report
        report = f"""
UK VOTING DEMOGRAPHICS ANALYSIS
===============================
Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

DATASET OVERVIEW:
----------------
Total Individuals: {total_individuals}
Cities Represented: {data['City'].nunique()}

VOTING ELIGIBILITY BREAKDOWN:
----------------------------
"""
        
        for status, count in voting_counts.items():
            percentage = voting_percentages[status]
            report += f"{status}: {count} individuals ({percentage}%)\n"
        
        report += f"""
AGE STATISTICS:
--------------
Average Age: {age_stats['Average Age']} years
Median Age: {age_stats['Median Age']} years
Youngest Individual: {age_stats['Youngest']} years
Oldest Individual: {age_stats['Oldest']} years
Age Range: {age_stats['Age Range']} years

TOP 10 CITIES BY POPULATION:
---------------------------
"""
        
        for city, count in city_counts.items():
            report += f"{city}: {count} individuals\n"
        
        report += f"""
DETAILED AGE GROUP ANALYSIS:
---------------------------
"""
        
        # Detailed age group analysis
        age_groups = {
            'Children (0-15)': len(data[data['Age'] < 16]),
            'New Voters (16-17)': len(data[(data['Age'] >= 16) & (data['Age'] < 18)]),
            'Young Adults (18-25)': len(data[(data['Age'] >= 18) & (data['Age'] <= 25)]),
            'Adults (26-65)': len(data[(data['Age'] > 25) & (data['Age'] <= 65)]),
            'Seniors (65+)': len(data[data['Age'] > 65])
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
