import requests
from rdflib import Graph
from pyld import jsonld

# List of URLs to fetch data from
urls = [
    'http://investing.com',
    'http://tradingview.com',
]

# Function to fetch RDF data from a URL and convert it to JSON-LD
def fetch_and_convert_data(url):
    # Fetch RDF data from URL
    response = requests.get(url)
    data = response.text

    # Parse RDF data into an rdflib graph
    g = Graph()
    g.parse(data=data, format='xml')

    # Convert rdflib graph to JSON-LD
    context = {
        "@vocab": "http://investing.com/",
    }
    data_jsonld = jsonld.from_rdf(str(g.serialize(format='nt')), {'format': 'application/n-quads'})
    compacted = jsonld.compact(data_jsonld, context)
    
    return compacted

# Fetch and convert data from all URLs and store it in a dictionary
data = {}
for url in urls:
    data[url] = fetch_and_convert_data(url)

# Save the data to a JSON file
with open('data.json', 'w') as f:
    json.dump(data, f)
