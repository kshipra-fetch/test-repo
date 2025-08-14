#!/usr/bin/env python3

import json
import sys

def main():
    print("Starting Ocean Protocol compute algorithm...")
    
    # Read input data (the dataset)
    try:
        with open('dataset.txt', 'r') as f:
            data = f.read().strip()
        
        print(f"Input data: {data}")
        
        # Parse the comma-separated numbers
        numbers = [int(x.strip()) for x in data.split(',')]
        print(f"Parsed numbers: {numbers}")
        
        # Calculate the sum
        total = sum(numbers)
        print(f"Sum of numbers: {total}")
        
        # Create result
        result = {
            "input_numbers": numbers,
            "sum": total,
            "count": len(numbers),
            "average": total / len(numbers)
        }
        
        # Write result to output file
        with open('/data/outputs/result.json', 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"Result saved: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
