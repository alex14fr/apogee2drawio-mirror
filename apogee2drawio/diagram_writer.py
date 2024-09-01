import xml.etree.ElementTree as etree

from enum import Enum
class ShowOption(Enum):
    CODE_APOGEE = 1
    DESCRIPTION = 2
    CODE_AND_DESCRIPTION = 3

WIDTH_ITEM=100
HIGHT_ITEM=26
WIDTH_LETTER=7 # The width for Courier New 12pt
WIDTH_MARGINS=30
WIDTH_LEFT_MARGIN=10
HEIGHT_HEADER=50
HEADER_ID="VDI_VET_INFO"

# The common style for all lists of ELP
STYLE_LIST="swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;\
    startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;\
        collapsible=0;marginBottom=0;portConstraintRotation=0;rotatable=0;dropTarget=0;resizable=0;fontFamily=monospace;"

# The style for an ELP
STYLE_ITEM="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;\
    overflow=hidden;points=[[0,0.5],[1,0.5]];\
        portConstraint=eastwest;rotatable=0;locked=1;fontFamily=monospace;spacingLeft=10;"

# The style for a suspended ELP
STYLE_SUSPENDED_ITEM="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;\
    overflow=hidden;points=[[0,0.5],[1,0.5]];\
        portConstraint=eastwest;rotatable=0;locked=1;fontStyle=2;fontColor=#CCCCCC;fontFamily=monospace;spacingLeft=10;"

# The stile for a link arrow between blocks
STYLE_LINK="edgeStyle=orthogonalEdgeStyle;endArrow=classic;html=1;curved=0;rounded=1;\
    endSize=8;startSize=8;locked=1;targetPortConstraint=north;sourcePortConstraint=eastwest;"

# Cardinality label for the links towards mandatory lists of options
STYLE_LABEL="edgeLabel;resizable=0;html=1;align=center;verticalAlign=middle;labelBorderColor=default;"

# The style for the header block (for VDI and VET data)
STYLE_HEADER="rounded=1;whiteSpace=wrap;html=1;fontStyle=1;strokeWidth=2;resizable=0;portConstraint=south;fontFamily=monospace;"

# The style for the text in the header block
STYLE_HEADER_TEXT="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;\
    rounded=0;locked=1;fontStyle=1;fontFamily=monospace;"

# These codes are taken from Apogée's "référenciel", and shortened to three symbols 
CODE_ELP={'Semestre':'SEM', 'U.E.':'UE', 'U.F.':'UF', 'Rés. étape':'RET', 'Stage':'STG', 
          'Parcours':'PAR', 'Elt à choi':'ELC', 'BCC':'BCC', 'Année':'AN', 'Bloc':'BLC',
          'Certificat':'CRT', 'C.M.':'CM', 'Compétence':'CMP', 'Cursus':'CUR', 'ECUE':'ECU',
          'Examen':'EXA', 'Filière':'FIL', 'Matière':'MAT', 'Mémoire':'MEM', 'Module':'MOD',
          'Niveau':'NIV', 'option':'OPT', 'Période':'PER', 'Projet':'PRJ', 'Section':'SEC',
          'T.D.':'TD', 'T.P.':'TP', 'UE  nonADD':'UEF', 'UE sansnot':'USN', 'U.V.':'UV'}
CODE_LIST={'Obligatoire':'LO', 'Obligatoire à choix':'LOX', 'Facultative':'LF'}

def make_list_header(dl, to_show:ShowOption):    
    if to_show==ShowOption.CODE_APOGEE:
        return f"{dl['code']} {CODE_LIST[dl['type']]}"
    elif to_show==ShowOption.DESCRIPTION:
        return dl['name']
    elif to_show==ShowOption.CODE_AND_DESCRIPTION:
        return f"{dl['code']} {CODE_LIST[dl['type']]} - {dl['name']}"

def make_label(item, to_show:ShowOption):
    if to_show==ShowOption.CODE_APOGEE:
        return f"{item['code']} {CODE_ELP[item['type']]}"
    elif to_show==ShowOption.DESCRIPTION:
        return item['name']
    elif to_show==ShowOption.CODE_AND_DESCRIPTION:
        return f"{item['code']} {CODE_ELP[item['type']]} - {item['name']}"
    
def make_tip(item, to_show:ShowOption):
    if to_show==ShowOption.CODE_APOGEE:
        return item['name']   
    elif to_show==ShowOption.DESCRIPTION:
        return f"{item['code']} {CODE_ELP[item['type']]}"
    elif to_show==ShowOption.CODE_AND_DESCRIPTION:
        return ""

def make_elp_id(block, item):
    return f"{block['list']['code']}__{item['code']}"

def width_field(s:str):
    return WIDTH_LETTER*len(s)+WIDTH_MARGINS

def header_lines(header):
    line0=f"Diplôme: {header['name_dip']}"
    line1=f"VDI: {header['code_vdi']} {header['vers_vdi']} - {header['name_vdi']}"
    line2=f"VET: {header['vers_vet']} - {header['name_vet']}"  
    return (line0, line1, line2)

def width_header(header):
    return max(width_field(s) for s in header_lines(header))

def height_block(block):
    return (len(block['items'])+1)*HIGHT_ITEM

def width_block(block, to_show:ShowOption):
    dl=block['list']
    header=make_list_header(dl, to_show)
    # Compute the maximal width of all fields of the block:
    maxwidth=width_field(header)
    for item in block['items']:
        label=make_label(item, to_show)
        itemwidth=width_field(label)
        if itemwidth>maxwidth:
            maxwidth=itemwidth
    return maxwidth

def makemxfile():
    mxfile = etree.Element('mxfile', host='apogee2drawio')
    diagram = etree.Element('diagram', name='Page 1')
    mxfile.append(diagram)
    model = etree.Element('mxGraphModel', dx="1358", dy="688", grid="1", gridSize="10", guides="1", tooltips="1", connect="0", arrows="0", fold="1", page="1", pageScale="1", pageWidth="827", pageHeight="1169", math="0", shadow="0")
    diagram.append(model)
    root = etree.Element('root')
    model.append(root)
    zero = etree.Element('mxCell',id='0')
    one = etree.Element('mxCell',id='1', parent='0')
    root.append(zero)
    root.append(one)
    return (mxfile, root)

def drawblock(root, block, pos, to_show:ShowOption):
    (x,y)=pos
    dl=block['list']
    header=make_list_header(dl, to_show)
    w=width_block(block, to_show)
    id_block=dl['code']
    container=etree.Element('mxCell', id=id_block, value=header, style=STYLE_LIST, parent="1", vertex="1")
    h=height_block(block)
    g=etree.Element('mxGeometry', x=str(x), y=str(y), width=str(w), height=str(h))
    g.set('as','geometry')
    container.append(g)
    root.append(container)
    count=0
    for item in block['items']:
        count+=1
        label=make_label(item, to_show)
        id_item=make_elp_id(block, item)
        tip=make_tip(item, to_show)
        uo=etree.Element('UserObject', label=label, tooltip=tip, id=id_item)
        cellstyle=STYLE_SUSPENDED_ITEM if 'suspended' in item else STYLE_ITEM
        cell=etree.Element('mxCell', style=cellstyle, parent=id_block, vertex="1")
        uo.append(cell)
        g=etree.Element('mxGeometry', y=str(HIGHT_ITEM*count), width=str(w), height=str(HIGHT_ITEM))
        g.set('as','geometry')
        cell.append(g)
        root.append(uo)
    

def drawheader(root, header, pos, to_show:ShowOption):
    (x,y)=pos
    (line0, line1, line2)=header_lines(header)
    text=f'{line0}<br>{line1}<br>{line2}' 
    container= etree.Element('mxCell', id=HEADER_ID, value=text, style=STYLE_HEADER, parent="1", vertex="1")
    w=width_header(header)
    g=etree.Element('mxGeometry', x=str(x), y=str(y), width=str(w), height=str(HEIGHT_HEADER))
    g.set('as','geometry')
    container.append(g)
    root.append(container)
    

def drawlink(root, id_source, id_target, label=None):
    #block, n=src
    #id_source=make_id(block, block['items'][n])
    id=f'{id_source}__{id_target}'
    container=etree.Element('mxCell', id=id, value="", style=STYLE_LINK, parent="1", 
                            source=id_source, target=id_target, edge="1")
    g=etree.Element('mxGeometry', width="50", height="50", relative="1")
    g.set('as','geometry')
    container.append(g)
    root.append(container)
    if label==None:
        return
    # Add a label
    container=etree.Element('mxCell', id=f'{id}_L', value=label, style=STYLE_LABEL, 
                            connectable="0", vertex="1", parent=id)
    g=etree.Element('mxGeometry', relative="1", x="-1")
    g.set('as','geometry')
    p=etree.Element('mxPoint')
    p.set('as','offset')
    g.append(p)
    container.append(g)
    root.append(container)

def write_mxfile(mxfile, filename):
    tree=etree.ElementTree(mxfile)
    with open(filename, 'wb') as f:
        etree.indent(tree, space="  ", level=0)
        tree.write(f)
