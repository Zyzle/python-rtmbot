from __future__ import print_function

outputs = []

def process_message(data):
    if data['channel'].startswith("D"):
        print(data)
        outputs.append([data['channel'],
            "from <@{}> \"{}\" in channel <#{}>".format(data['user'], data['text'], data['channel'])
        ])

class 
