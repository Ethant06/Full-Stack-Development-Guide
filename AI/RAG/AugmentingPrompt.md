# Example of Augmenting Prompts to be passed to an LLM.


###### Data Structure
Say we have a tiny dataset of houses:
```
house_data = [
    {
        "address": "123 Maple Street",
        "city": "Springfield",
        "state": "IL",
        "zip": "62701",
        "bedrooms": 3,
        "bathrooms": 2,
        "square_feet": 1500,
        "price": 230000,
        "year_built": 1998
    },
    {
        "address": "456 Elm Avenue",
        "city": "Shelbyville",
        "state": "TN",
        "zip": "37160",
        "bedrooms": 4,
        "bathrooms": 3,
        "square_feet": 2500,
        "price": 320000,
        "year_built": 2005
    }
]
```

###### Creating the Layout for the data
We then design a layout for the data:
```
def house_info_layout(houses):
    layout = ''
    # Iterate over the houses
    for house in houses:
        layout += (f"House located at {house['address']}, {house['city']}, {house['state']} {house['zip']} with "
            f"{house['bedrooms']} bedrooms, {house['bathrooms']} bathrooms, "
            f"{house['square_feet']} sq ft area, priced at ${house['price']}, "
            f"built in {house['year_built']}.\n")
    return layout
```
This will format a string for instance:
```
House located at 123 Maple Street, Springfield, IL 62701 with 3 bedrooms, 2 bathrooms, 1500 sq ft area, priced at $230000, built in 1998.
House located at 456 Elm Avenue, Shelbyville, TN 37160 with 4 bedrooms, 3 bathrooms, 2500 sq ft area, priced at $320000, built in 2005.
```

###### Generate prompt to be passed to the LLM.
Takes user's query and available data input
```
def generate_prompt(query, houses):
    houses_layout = house_info_layout(houses)
    PROMPT = f"""
      Use the following houses information to answer users queries.
      {houses_layout}
      Query: {query}
             """
    return PROMPT
```
Which returns something like:
```
Use the following houses information to answer users queries.
House located at 123 Maple Street, Springfield, IL 62701 with 3 bedrooms, 2 bathrooms, 1500 sq ft area, priced at $230000, built in 1998.
House located at 456 Elm Avenue, Shelbyville, TN 37160 with 4 bedrooms, 3 bathrooms, 2500 sq ft area, priced at $320000, built in 2005.

Query: What is the most expensive house?
```