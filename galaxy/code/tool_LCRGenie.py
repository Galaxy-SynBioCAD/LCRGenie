#!/usr/bin/env python3

"""
Created on March 21 2020

@author: Melchior du Lac
@description: Galaxy implementation of LCRGenie

"""

import argparse
import sys
sys.path.insert(0, '/home/lcr_genie')

import io_utils
import lcr
import sbol_utils
import tempfile
import shutil
import os
import glob
import tarfile
import tempfile

##
#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Python wrapper to call OptBioDes using rpSBML')
    parser.add_argument('-input', type=str)
    parser.add_argument('-input_format', type=str)
    parser.add_argument('-output', type=str)
    parser.add_argument('-melting_temp', type=float, default=60.0)
    params = parser.parse_args()
    
    if params.input_format=='tar':
        with tempfile.TemporaryDirectory() as tmpOutputFolder:
            with tempfile.TemporaryDirectory() as tmpInputFolder:
                tar = tarfile.open(params.input, mode='r')
                tar.extractall(path=tmpInputFolder)
                tar.close()
                for sbol_path in glob.glob(tmpInputFolder+'/*.xml'):
                    with tempfile.TemporaryDirectory() as tmpCopyFolder:
                        tmp_input_path = os.path.join(tmpCopyFolder, 'input.xml')
                        tmp_output_path = os.path.join(tmpOutputFolder, sbol_path.split('/')[-1].replace('.xml', '').replace('.sbol', '').replace('.rpsbol', '')+'.xlsx')
                        shutil.copy(sbol_path, tmp_input_path)
                        # Parse SBOL:
                        part_seqs, construct_parts, construct_seqs = sbol_utils.parse(path=tmp_input_path)

                        # Get bridging oligos:
                        construct_oligos, oligo_seqs = lcr.run(construct_parts, part_seqs, float(params.melting_temp))

                        # Write:
                        io_utils.write(
                            part_seqs=part_seqs,
                            construct_parts=construct_parts,
                            construct_seqs=construct_seqs,
                            oligo_seqs=oligo_seqs,
                            construct_oligos=construct_oligos,
                            out_filename=tmp_output_path,
                        )
            #with tarfile.open(fileobj=params.output, mode='w:gz') as ot:
            with tarfile.open(fileobj=params.output, mode='w:xz') as ot:
                for xlsx_path in glob.glob(tmpOutputFolder+'/*'):
                    fileName = str(xlsx_path.split('/')[-1])
                    info = tarfile.TarInfo(fileName)
                    info.size = os.path.getsize(xlsx_path)
                    ot.addfile(tarinfo=info, fileobj=open(xlsx_path, 'rb'))
    elif params.input_format=='sbol':
        #make the tar.xz 
        with tempfile.TemporaryDirectory() as tmpCopyFolder:
            tmp_input_path = os.path.join(tmpCopyFolder, 'input.xml')
            tmp_output_path = os.path.join(tmpCopyFolder, 'output.xlsx')
            shutil.copy(params.input, tmp_input_path)
            # Parse SBOL:
            part_seqs, construct_parts, construct_seqs = sbol_utils.parse(path=tmp_input_path)

            # Get bridging oligos:
            construct_oligos, oligo_seqs = lcr.run(construct_parts, part_seqs, float(params.melting_temp))

            # Write:
            io_utils.write(
                part_seqs=part_seqs,
                construct_parts=construct_parts,
                construct_seqs=construct_seqs,
                oligo_seqs=oligo_seqs,
                construct_oligos=construct_oligos,
                out_filename=tmp_output_path,
            )
            shutil.copy(tmp_output_path, params.output)
    else:
        logging.error('Cannot interpret input_format: '+str(params.input_format))
        exit(1)

