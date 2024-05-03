import xml.etree.ElementTree as etree

def parse_doc(filename):
    doc = etree.parse(filename)
    # Parse the VDI and VET data
    gcdip=doc.find('./LIST_G_COD_DIP/G_COD_DIP')
    code_vdi=gcdip.find('COD_DIP')
    vers_vdi=gcdip.find('COD_VRS_VDI')
    name_dip=gcdip.find('LIC_DIP')
    name_vdi=gcdip.find('LIC_VDI')
    vers_vet=gcdip.find('COD_VRS_VET')
    name_vet=gcdip.find('LIC_ETP')
    header={'code_vdi':code_vdi.text, 'vers_vdi':vers_vdi.text, 'name_dip':name_dip.text, 
            'name_vdi':name_vdi.text, 'vers_vet':vers_vet.text, 'name_vet':name_vet.text}
    rv={'levels':[], 'header':header}
    # Parse the topmost lists
    all_topmost=[]
    gclses=doc.findall('./LIST_G_COD_DIP/G_COD_DIP/LIST_G_COD_LSE/G_COD_LSE')
    for gclse in gclses:
        clse=gclse.find('COD_LSE')
        llse=gclse.find('LIC_LSE')
        t=gclse.find('TYP_LSE1')
        topmost={'parent':None, 'list':{'code':clse.text, 'name':llse.text, 'type':t.text}, 'items':[]}
        lgcelp=gclse.find('LIST_G_COD_ELP')
        gcelps=lgcelp.findall('G_COD_ELP')
        for gcelp in gcelps:
            celp=gcelp.find('COD_ELP')
            lnel=gcelp.find('LIC_NEL')
            lelp=gcelp.find('LIC_ELP')
            sus=gcelp.find('TEM_SUS_ELP')
            item={'code':celp.text, 'type':lnel.text, 'name':lelp.text}
            if sus.text == 'O':
                item['suspended']=True
            topmost['items'].append(item)
        all_topmost.append(topmost)
    rv['levels'].append(all_topmost)
    # Parse other lists
    levels = doc.findall('./LIST_G_NIVEAU/G_NIVEAU')
    for g in levels:
        level=g.find('NIVEAU')
        n=int(level.text)
        expected_n=len(rv['levels'])+1
        if n!=expected_n:
            raise ValueError(f'Expecting level {expected_n}, got {n}')
        elements=g.findall('LIST_G_COD_ELP_PERE1/G_COD_ELP_PERE1')
        blocks=[]
        for e in elements:
            parent=e.find('COD_ELP_PERE1')
            l=e.find('COD_LSE2')
            l1=e.find('LIST_G_COD_LSE1/G_COD_LSE1/COD_LSE1')
            if l.text != l1.text:
                raise ValueError("Inconsistent list names")
            llse=e.find('LIST_G_COD_LSE1/G_COD_LSE1/LIC_LSE1')
            y=e.find('LIST_G_COD_LSE1/G_COD_LSE1/TYP_LSE')
            nmin=e.find('LIST_G_COD_LSE1/G_COD_LSE1/NBR_MIN_ELP_OBL_CHX')
            nmax=e.find('LIST_G_COD_LSE1/G_COD_LSE1/NBR_MAX_ELP_OBL_CHX')
            block={'parent':parent.text, 'list':{'code':l.text, 'name':llse.text, 'type':y.text, 'min':nmin.text, 'max':nmax.text}, 'items':[]}
            children=e.findall('LIST_G_COD_ELP_FILS/G_COD_ELP_FILS')
            for c in children:
                child=c.find('COD_ELP_FILS')
                child_type=c.find('LIST_G_COD_ELP1/G_COD_ELP1/LIC_NEL1')
                child_name=c.find('LIST_G_COD_ELP1/G_COD_ELP1/LIC_ELP1')
                sus=c.find('LIST_G_COD_ELP1/G_COD_ELP1/TEM_SUS_ELP1')
                item={'code':child.text, 'type':child_type.text, 'name':child_name.text}
                if sus.text == 'O':
                    item['suspended']=True
                block['items'].append(item)
            blocks.append(block)
        rv['levels'].append(blocks)
    return rv
