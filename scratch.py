import re

# Modified regex pattern
pattern = re.compile(r'\(\s*([a-zA-Z]{1,5}\.?\s*\d{4})\s*(?:;?\s*([a-zA-Z]{1,5}\.?\s*\d{4}))?\s*\)')

# Test the pattern with your examples
test_strings = [
    "( m. 1950 ; div. 1951 )",
    "( m. 2012)",
    "( m. 1957; ann. 1962)",	
    "( m. 1964; div. 1969)",
    "( m. 1942)",
    "( m. 1943; died 1951)"
]

for test in test_strings:
    matches = pattern.findall(test)
    print(f"Original: {test}")
    print(f"Matches: {matches}\n")
