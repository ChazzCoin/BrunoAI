
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

# Example JSON data structure
json_data = {
    "development": {
        "username": "postgres",
        # Other keys omitted for brevity
    },
    # Other top-level keys omitted for brevity
}

# Flattening the JSON data
flattened_json = flatten_json(json_data)
print(flattened_json)
