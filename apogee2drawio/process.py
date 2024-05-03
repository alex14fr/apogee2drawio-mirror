import argparse
import platform
import os
from base64 import b64encode
from .diagram_maker import make_diagram
from .diagram_writer import ShowOption

DICT_SHOW={'code_apogee':ShowOption.CODE_APOGEE, 'description':ShowOption.DESCRIPTION, 
           'both':ShowOption.CODE_AND_DESCRIPTION}

def main():
    parser = argparse.ArgumentParser(description='Process Apogée XML to DrawIO diagram')
    parser.add_argument('-in', '--infile', type=str, help='Input apogée XML file path')
    parser.add_argument('-out', '--outfile', type=str, help='Output DrawIO file path')
    parser.add_argument('-s', '--show', type=str, default='code_apogee', 
                        choices=['code_apogee', 'description', 'both'], help='Information to show')
    parser.add_argument('-v', '--view', action='store_true', help='Open the generated DrawIO file in browser')

    args = parser.parse_args()

    if args.infile is None or args.outfile is None:
        parser.error("Please provide both input and output file paths.")
    else:
        make_diagram(args.infile, args.outfile, to_show=DICT_SHOW[args.show])

    if args.view:
        ftmpn = args.outfile + ".html"
        with open(args.outfile, "r") as ff, open(ftmpn, "w+") as ftmp:
            htmlstr = "<!doctype html><style>*{border:0;padding:0;margin:0}</style>  \
            <iframe src='https://embed.diagrams.net/?embed=1&proto=json&spin=1&noSaveBtn=0&noExitBtn=1'></iframe>  \
            <script>\"use strict\";\n   \
            var xmlstr=atob('"+b64encode(bytes(ff.read(), "utf8")).decode("utf8")+"');   \
            var ifrm=document.querySelector('iframe');   \
            window.onmessage=function(ev) {   \
                ifrm.contentWindow.postMessage(JSON.stringify({'action':'load','xml':xmlstr}), '*');    \
                window.onmessage=null;    \
            };    \
            window.onresize=function(ev) {  \
                ifrm.style.width=(ifrm.parentElement.clientWidth-5)+'px';    \
                ifrm.style.height=(window.innerHeight-5)+'px'; \
            }; \
            window.onresize();</script>";
            ftmp.write(htmlstr)
            if "Windows" in platform.platform():
                os.startfile(ftmpn)
            elif "Darwin" in platform.platform():
                os.system("open "+ftmpn)
            else:
                os.system("xdg-open "+ftmpn)

if __name__ == "__main__":
    main()
