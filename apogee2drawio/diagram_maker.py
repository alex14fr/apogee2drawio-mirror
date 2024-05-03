from .diagram_writer import makemxfile, drawblock, drawheader, drawlink, write_mxfile, height_block, \
    width_block, HEIGHT_HEADER, ShowOption, make_elp_id, HEADER_ID, width_header
from .apogee_parser import parse_doc
from .data_filter import prepare_graph

LAYER_SPACING=80
HORIZONTAL_SPACING=40
TOP_POS=120
LEFT_POS=120

# Assign positions to the blocks
def make_basic_layout(graph, to_show):
    # Assign a position to the header
    header=graph['header']
    header['pos']=(-width_header(header)//2, 0)
    # Assign codes to levels
    n=graph['num_levels']
    codes=[[] for _ in range(n)]
    blocks=graph['blocks']
    for code in blocks:
        i=blocks[code]['level']
        codes[i].append(code)
    y=TOP_POS
    for c in codes:
        h=0
        # Assign temporary x coordinates and compute the maximal height:
        x=0
        for code in c:
            b=blocks[code]
            b['pos']=(x, y)
            x+=(width_block(b, to_show)+HORIZONTAL_SPACING)
            h=max(h, height_block(b))
        halfwidth=(x-HORIZONTAL_SPACING)//2
        # Make an isoscele pyramid:
        for code in c:
            b=blocks[code]
            (x, y)=b['pos']
            b['pos']=(x-halfwidth, y)
        y+=(h+LAYER_SPACING)

def make_diagram(infile, outfile, to_show=ShowOption.CODE_APOGEE):
    mxfile, root=makemxfile()
    data=parse_doc(infile)
    graph=prepare_graph(data)
    make_basic_layout(graph, to_show)
    # Draw header:
    header=graph['header']
    drawheader(root, header, header['pos'], to_show) 
    # Draw other blocks
    blocks=graph['blocks']
    for code in blocks:
        b=blocks[code]
        drawblock(root, b, b['pos'], to_show)
    # Draw links:
    # Start with the links from the header to the topmost blocks:
    topmost_ids=[code for code in blocks if blocks[code]['level']==0]
    for topmost_id in topmost_ids:
        drawlink(root, id_source=HEADER_ID, id_target=topmost_id, label=None)
    # Draw the remaining links 
    uplinks=graph['uplinks']
    
    active_elps=graph['active_elps']
    for code_uplink in uplinks:
        u=uplinks[code_uplink]
        upper_elps=active_elps[u['parent']]
        for code_list in upper_elps:
            upper_block=blocks[code_list] 
            dst=blocks[u['child']]
            id_target=dst['list']['code']
            n=upper_elps[code_list]
            id_source=make_elp_id(upper_block, upper_block['items'][n])
            # Add a label to the link if necessary
            label=None
            if 'min' in u and 'max' in u:
                if u['min']!=None and u['max']!=None:
                    label=f"{u['min']}-{u['max']}"
            drawlink(root, id_source=id_source, id_target=id_target, label=label)
    write_mxfile(mxfile, outfile)
