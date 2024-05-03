
# Perform the top-down filtration of Apogee data
# Remove blocks accessible only via suspended items
# Prepare uplinks and their cardinality if applied 
def prepare_graph(data):
    blocks={}
    uplinks={}
    active_elps={}
    for ilevel, level in enumerate(data['levels']):
        for x in level:
            parent=x['parent']
            # If the parent is not active, skip the list
            if parent and parent not in active_elps:
                continue
            l=x['list']
            code=l['code']
            # Always update the block, this way is will be assigned the lowermost level
            blocks[code]={'list':{'code':code, 'name':l['name'], 'type':l['type']}, 'items':x['items'], 'level':ilevel} 
            # Add active elps
            for i, item in enumerate(x['items']):
                if 'suspended' not in item:
                    code_elp=item['code']
                    if code_elp not in active_elps:
                        active_elps[code_elp]={}
                    active_elps[code_elp][code]=i
            # Add an uplink (whether the list is new or already seen):
            if parent:
                code_uplink=f'{parent}__{code}'
                uplinks[code_uplink]={'parent':parent, 'child': code, 'min':l['min'], 'max':l['max']}
    return {'blocks':blocks, 'uplinks':uplinks, 'active_elps':active_elps, 'num_levels':len(data['levels']), 'header':data['header']}


