# this file generates a seqspec file of IGVF data by using a Jinja YAML teemplate file and igvf file ids for forward reverse and umi reads. Inputs are controlled by click.

import click
from datetime import date
import seqspec
from io import StringIO
from seqspec.utils import load_spec_stream
import json
from jsonschema import Draft4Validator
import igvf_utils as iu
from igvf_utils.connection import Connection
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import os


@click.command()
@click.option(
    "--template",
    "template_file",
    required=True,
    type=click.Path(exists=True, readable=True),
    help="Seqspec jinja2 template file.",
)
@click.option(
    "--name",
    "name",
    required=True,
    type=str,
    help="Name in the seqspec file, e.g. mpra_shendure_asd",
)
@click.option(
    "--modality",
    "modality",
    required=False,
    default="dna",
    type=click.Choice(["dna", "rna"]),
    help="Modality of the data",
)
@click.option(
    "--doi",
    "doi",
    required=False,
    type=str,
    help="DOI of the publication",
)
@click.option(
    "--bc-length",
    "bc_length",
    required=True,
    type=int,
    help="Barcode length, if not set mean read length of R1 read is used",
)
@click.option(
    "--oligo-length",
    "oligo_length",
    required=False,
    type=int,
    help="Oligo length, if not set mean read length of R2 read is used",
)
@click.option(
    "--r1-id",
    "r1_ids",
    required=True,
    multiple=True,
    type=str,
    help="IGVF ID of R1 primer",
)
@click.option(
    "--r2-id",
    "r2_ids",
    required=False,
    multiple=True,
    type=str,
    help="IGVF ID of R1 primer",
)
@click.option(
    "--r3-id",
    "r3_ids",
    required=False,
    multiple=True,
    type=str,
    help="IGVF ID of R1 primer",
)
@click.option(
    "--onlist-id",
    "onlist_id",
    required=False,
    type=str,
    help="Using IGVF id of tsv file containing onlist for barcode",
)
@click.option(
    "--r1-primer",
    "r1_primer",
    required=False,
    default="GCAAAGTGAACACATCGCTAAGCGAAAGCTAAG", # "GCTCCTCGCCCTTGCTCACCATGGTGGCGACCGGT",
    type=str,
    help="R1 primer sequence",
)
@click.option(
    "--r2-primer",
    "r2_primer",
    required=False,
    default="ACCGGTCGCCACCATGGTGAGCAAGGGCGAGGAGC",
    type=str,
    help="R2 primer sequence",
)
@click.option(
    "--r3-primer",
    "r3_primer",
    required=False,
    default="CTTAGCTTTCGCTTAGCGATGTGTTCACTTTGC",
    type=str,
    help="R3 primer sequence",
)
@click.option(
    "--output",
    "output_file",
    required=True,
    type=click.Path(writable=True),
    help="Output seqspec file.",
)
def cli(
    template_file,
    name,
    modality,
    doi,
    bc_length,
    oligo_length,
    r1_ids,
    r2_ids,
    r3_ids,
    onlist_id,
    r1_primer,
    r2_primer,
    r3_primer,
    output_file,
):

    click.echo("Generating seqspec file")

    def seqspec_validate(schema, spec):
        """
        Validate a yaml object against a json schema
        """
        validator = Draft4Validator(schema)
        for idx, error in enumerate(validator.iter_errors(spec), 1):
            print(f"[{idx}] {error.message}")

    schema_path = "schema/seqspec.schema.json"
    with open(schema_path, "rt") as instream:
        seqspec_schema = json.load(instream)

    # env = Environment(
    #     loader=PackageLoader("IGVF_MPRA_seqspec_generator"),
    #     autoescape=select_autoescape(),
    # )
    env = Environment(
        loader=FileSystemLoader("templates/"), autoescape=select_autoescape()
    )
    template = env.get_template(os.path.basename(template_file))

    conn = Connection("prod")

    template_vars = {
        "date": date.today(),
        "name": name,
        "modality": modality,
        "r1_primer": r1_primer,
        "r2_primer": r2_primer,
        "r3_primer": r3_primer,
    }

    if doi is not None:
        template_vars["doi"] = doi

    def getReads(read_ids):
        reads = []
        for read_id in read_ids:
            read_file = conn.get(read_id)
            reads.append(read_file)
        return reads

    reads = getReads(r1_ids)
    template_vars["r1_reads"] = reads

    platform_terms = conn.get(reads[0]["sequencing_platform"]["@id"])
    template_vars["platform_terms"] = platform_terms
    template_vars["bc_length"] = bc_length

    reads = getReads(r2_ids)
    template_vars["r2_reads"] = reads
    if oligo_length is None and r2_ids:
        oligo_length = reads[0]["mean_read_length"]
    template_vars["oligo_length"] = oligo_length

    template_vars["r3_reads"] = getReads(r3_ids)

    if onlist_id is not None:
        onlist = conn.get(onlist_id)
        template_vars["onlist"] = onlist

    content = template.render(
        template_vars,
    )

    spec = load_spec_stream(StringIO(content))
    spec.update_spec()
    seqspec_validate(seqspec_schema, spec.to_dict())

    with open(output_file, mode="w", encoding="utf-8") as message:
        message.write(content)


if __name__ == "__main__":
    cli()
