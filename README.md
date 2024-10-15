# IGVF MPRA seqspec generator


This little helper usues jinja2 and igvf_utils to generate seqspec files for mpra count and association data. It is very flexible because many templates can be defined. It loads all necessary infomation from the IGVF data portal, like file-size, md5sums, sequencing platform, etc.


## Installation

You need to have jinja2 and click. I install it via mamba:

```bash
mamba install jinja2 click
```

Please install the actual seqspec development:

```bash
pip install git+https://github.com/pachterlab/seqspec@devel
```

Then install the igvf_utils ([install documentation](https://github.com/IGVF-DACC/igvf_utils/wiki/Installation)):
```bash
pip install https://github.com/IGVF-DACC/igvf_utils/archive/master.zip
```


Set the IGVF_API_KEY environment variable to your API key as well as the IGVF_SECRET_KEY to your secret key. See [configuration documentation](https://github.com/IGVF-DACC/igvf_utils/wiki/Configuration).


## Quickstart

```bash
python generate_seqspec.py --help
```

### Shendure grant

#### Assignment data

DNA assignment seqspec of lenti virus MPRA from Shendure (UW) grant:

```bash
python generate_seqspec.py --template templates/igvf_mpra_lenti_assignment.v0.3.0.yml \
--name mpra_shendure_80K --modality dna \
--r1-id IGVFFI9931MZQI --r2-id IGVFFI9154RAYY --r3-id IGVFFI7509PYSL \
--r1-primer GGCCCGCTCTAGACCTGCAGGAGGACCGGATCAACT --r2-primer GCAAAGTGAACACATCGCTAAGCGAAAGCTAAG --r3-primer CATTGCGTGAACCGACACTAGAGGGTATATAATG \
--bc-length 15 --oligo-length 270 \
--output test.yaml
```


```bash	
seqspec print -f seqspec-ascii test.yaml
```

returns:

```text
dna
---
                                                                                             |------------------------------------------------------------------------------------------------------------------------------------------------->(1) Oligo fwd
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |-------------->(3) BC
AATGATACGGCGACCACCGAGATCTACACXXXXXXXXXXCAGCCTGCATTTCTGCCAGGGCCCGCTCTAGACCTGCAGGAGGACCGGATCAACTNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNGCAAAGTGAACACATCGCTAAGCGAAAGCTAAGGAAGCTCGACTTCCAGCTTGGCAATCCGGTACTGTCATTGCGTGAACCGACACTAGAGGGTATATAATGXXXXXXXXXXXXXXXACCGGTCGCCACCATGGTGAGCAAGGGCGAGGAGCATCTCGTATGCCGTCTTCTGCTTG
TTACTATGCCGCTGGTGGCTCTAGATGTGXXXXXXXXXXGTCGGACGTAAAGACGGTCCCGGGCGAGATCTGGACGTCCTCCTGGCCTAGTTGANNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNCGTTTCACTTGTGTAGCGATTCGCTTTCGATTCCTTCGAGCTGAAGGTCGAACCGTTAGGCCATGACAGTAACGCACTTGGCTGTGATCTCCCATATATTACXXXXXXXXXXXXXXXTGGCCAGCGGTGGTACCACTCGTTCCCGCTCCTCGTAGAGCATACGGCAGAAGACGAAC
                                                                                                                                                                                                                          <-------------------------------------------------------------------------------------------------------------------------------------------------|(2) Oligo rev
```

#### Count data

RNA count seqspec of lenti virus MPRA from shendure (UW) grant:

```bash
python generate_seqspec.py --template templates/igvf_mpra_lenti_counts.v0.3.0.yml \
--name mpra_shendure_80K --modality rna \
--r1-id IGVFFI8223UESF --r1-id IGVFFI9990NOMV --r1-id IGVFFI3050NXPU \
--r2-id IGVFFI9560VIAN --r2-id IGVFFI5074MDCR --r2-id IGVFFI4713QQLG \
--r3-id IGVFFI1814DAMK --r3-id IGVFFI0172AZKE --r3-id IGVFFI2509VPWV \
--r1-primer GCAAAGTGAACACATCGCTAAGCGAAAGCTAAG --r2-primer ACCGGTCGCCACCATGGTGAGCAAGGGCGAGGAGC \
--bc-length 15 \
--output test.yaml
```

```bash	
seqspec print -f seqspec-ascii test.yaml
```

returns:

```text
rna
---
                                                                       |-------------->(1) RNA BC count fwd
                                                                                                                         |--------------->(3) RNA BC count id
AATGATACGGCGACCACCGAGATCTACACXXXXXXXXXXGCAAAGTGAACACATCGCTAAGCGAAAGCTAAGNNNNNNNNNNNNNNNACCGGTCGCCACCATGGTGAGCAAGGGCGAGGAGCXXXXXXXXXXXXXXXXATCTCGTATGCCGTCTTCTGCTTG
TTACTATGCCGCTGGTGGCTCTAGATGTGXXXXXXXXXXCGTTTCACTTGTGTAGCGATTCGCTTTCGATTCNNNNNNNNNNNNNNNTGGCCAGCGGTGGTACCACTCGTTCCCGCTCCTCGXXXXXXXXXXXXXXXXTAGAGCATACGGCAGAAGACGAAC
                                                                        <--------------|(2) RNA BC count rev
```

### Mohlke grant

RNA count seqspec of plasmid MPRA from Mohlke (UNC) grant:

```bash
python generate_seqspec.py --template templates/igvf_mpra_unc_counts.v0.3.0.yml \
--name mpra_unc_hepg2 --modality rna \
--r1-id  IGVFFI1586GLDT --r1-id IGVFFI1618FFIN \
--r1-primer CCAAGAAGGGCGGCAAGATCGCCGTGTAATAATTCTAGA --bc-length 20 --onlist-id IGVFFI9520JZQK \
--output test.yaml
```

```bash	
seqspec print -f seqspec-ascii test.yaml
```

returns:

```text
rna
---
                                                                                                                                                                              |-------------------------------------------------->(1) RNA BC count fw
AATGATACGGCGACCACCGAGATCTACACTACAACCGCCAAGAAGCTGCGCGGTGGTGTTGTGTTCGTGGACGAGGTGCCTAAAGGACTGACCGGCAAGTTGGACGCCCGCAAGATCCGCGAGATTCTCATTAAGGCCAAGAAGGGCGGCAAGATCGCCGTGTAATAATTCTAGANNNNNNNNNNNNNNNNNNNNACTAGTACACTCCCCGTCGGCAGTTGGGAAGAGCATAGTCGTAGAGCACGCGGACTCCTATCTCGTATGCCGTCTTCTGGTTG
TTACTATGCCGCTGGTGGCTCTAGATGTGATGTTGGCGGTTCTTCGACGCGCCACCACAACACAAGCACCTGCTCCACGGATTTCCTGACTGGCCGTTCAACCTGCGGGCGTTCTAGGCGCTCTAAGAGTAATTCCGGTTCTTCCCGCCGTTCTAGCGGCACATTATTAAGATCTNNNNNNNNNNNNNNNNNNNNTGATCATGTGAGGGGCAGCCGTCAACCCTTCTCGTATCAGCATCTCGTGCGCCTGAGGATAGAGCATACGGCAGAAGACCAAC
```