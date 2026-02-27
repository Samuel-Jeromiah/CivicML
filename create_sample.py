import json
import os

def main():
    print("Loading datasets...")
    with open('data/raw.json', 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    with open('data/X.json', 'r', encoding='utf-8') as f:
        X_data = json.load(f)

    # Let's pick diverse bills 
    # Just picking a range to represent various outcomes
    sample_indices = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 100, 200, 300, 400]
    sample_bills = []

    for i in sample_indices:
        if i < len(raw_data) and i < len(X_data):
            bill = raw_data[i]
            embedding = X_data[i]['text_embedding']
            sample_bills.append({
                'id': bill.get('ld_number', str(i)),
                'title': bill.get('title', 'Unknown Title'),
                'text_snippet': bill.get('text', '')[:300] + '...',
                'actual_committee': bill.get('committee', 'Unknown'),
                'embedding': embedding
            })

    # Save to the public folder
    os.makedirs('public', exist_ok=True)
    with open('public/sample_bills.json', 'w', encoding='utf-8') as f:
        json.dump(sample_bills, f)

    print(f"Created public/sample_bills.json with {len(sample_bills)} bills.")

if __name__ == '__main__':
    main()
