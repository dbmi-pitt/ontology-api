#!/usr/bin/env python

import argparse
import os
import pkt_kg as pkt
import psutil
import re
from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import OWL, RDF, RDFS
from tqdm import tqdm
import glob
import logging.config
import time
from datetime import timedelta

# Code taken from:
# https://github.com/callahantiff/PheKnowLator/blob/master/notebooks/OWLNETS_Example_Application.ipynb

# Setup and running the script...
#
# $ cd scripts
# $ python3 -m venv venv
# $ source venv/bin/activate
# $ python --version
# Python 3.9.5
# $ pip install -r requirements.txt
# $ brew install wget
# $ ./owl_nets_script/__main__.py owl_url

# https://docs.python.org/3/howto/argparse.html
parser = argparse.ArgumentParser(description='Run PheKnowLator on OWL file')
parser.add_argument('owl_url', type=str, help='url for the OWL file to process')
parser.add_argument("-c", "--clean", action="store_true",
                    help='clean the owlnets_output directory of previous output files before run')
args = parser.parse_args()

log_dir, log, log_config = 'builds/logs', 'pkt_build_log.log', glob.glob('**/logging.ini', recursive=True)
logger = logging.getLogger(__name__)
logging.config.fileConfig(log_config[0], disable_existing_loggers=False, defaults={'log_file': log_dir + '/' + log})

uri = args.owl_url
print(f"Processing '{uri}'")
logger.info(f"Processing '{uri}'")

# Both of these directories are found in the .gitignore file...
base_working_dir = './owlnets_output'
owltools_location = './pkt_kg/libs'


def file_from_uri(uri_str: str) -> str:
    if uri_str.find('/'):
        return uri_str.rsplit('/', 1)[1]


def download_owltools(loc: str):
    cmd = os.system(f"ls {loc}/owltools")
    if os.WEXITSTATUS(cmd) != 0:
        logger.info('Download owltools and update permissions')
        # move into pkt_kg/libs/ directory
        cwd = os.getcwd()
        os.system(f"mkdir -p {loc}")
        os.chdir(loc)

        os.system('wget https://github.com/callahantiff/PheKnowLator/raw/master/pkt_kg/libs/owltools')
        os.system('chmod +x owltools')

        # move back to the working directory
        os.chdir(cwd)


def log_files_and_sizes(dir: str) -> None:
    for f in os.listdir(dir):
        fp: str = os.path.join(dir, f)
        size: int = os.path.getsize(fp)
        logger.info(f"Generated file '{fp}' size {size:,}")


start_time = time.time()

download_owltools(owltools_location)

working_file = file_from_uri(uri)
working_dir = base_working_dir + os.path.sep + working_file.rsplit('.', 1)[0]
logger.info("Make sure working directory '%s' exists", working_dir)
os.system(f"mkdir -p {working_dir}")

if args.clean is True:
    logger.info(f"Deleting files in working directory {working_dir} because of --clean option")
    os.system(f"cd {working_dir}; rm -f *")
    working_dir_file_list = os.listdir(working_dir)
    if len(working_dir_file_list) == 0:
        logger.info(f"Working directory {working_dir} is empty")
    else:
        logger.error(f"Working directory {working_dir} is NOT empty")

# cpus
cpus = psutil.cpu_count(logical=True)

logger.info('Loading ontology')
graph = Graph().parse(uri, format='xml')

logger.info('Extract Node Metadata')
ont_classes = pkt.utils.gets_ontology_classes(graph)
ont_labels = {str(x[0]): str(x[2]) for x in list(graph.triples((None, RDFS.label, None)))}
ont_synonyms = pkt.utils.gets_ontology_class_synonyms(graph)
ont_dbxrefs = pkt.utils.gets_ontology_class_dbxrefs(graph)
ont_objects = pkt.utils.gets_object_properties(graph)

logger.info('Add the class metadata to the master metadata dictionary')
entity_metadata = {'nodes': {}, 'relations': {}}
for cls in tqdm(ont_classes):
    # get class metadata - synonyms and dbxrefs
    syns = '|'.join([k for k, v in ont_synonyms[0].items() if v == str(cls)])
    dbxrefs = '|'.join([k for k, v in ont_dbxrefs[0].items() if v == str(cls)])

    # extract metadata
    if '_' in str(cls):
        namespace = re.findall(r'^(.*?)(?=\W|_)', str(cls).split('/')[-1])[0].upper()
    else:
        namespace = str(cls).split('/')[2]

    # update dict
    entity_metadata['nodes'][str(cls)] = {
        'label': ont_labels[str(cls)] if str(cls) in ont_labels.keys() else 'None',
        'synonyms': syns if syns != '' else 'None',
        'dbxrefs': dbxrefs if dbxrefs != '' else 'None',
        'namespace': namespace
    }

logger.info('Add the object metadata to the master metadata dictionary')
for obj in tqdm(ont_objects):
    # get object label
    label_hits = list(graph.objects(obj, RDFS.label))
    label = str(label_hits[0]) if len(label_hits) > 0 else 'None'

    # get object namespace
    if 'obo' in str(obj) and len(str(obj).split('/')) > 5:
        namespace = str(obj).split('/')[-2].upper()
    else:
        if '_' in str(obj):
            namespace = re.findall(r'^(.*?)(?=\W|_)', str(obj).split('/')[-1])[0].upper()
        else:
            namespace = str(obj).split('/')[2]

    # update dict
    entity_metadata['relations'][str(obj)] = {'label': label, 'namespace': namespace}

logger.info('Add RDF:type and RDFS:subclassOf')
entity_metadata['relations']['http://www.w3.org/2000/01/rdf-schema#subClassOf'] =\
    {'label': 'subClassOf', 'namespace': 'www.w3.org'}
entity_metadata['relations']['https://www.w3.org/1999/02/22-rdf-syntax-ns#type'] =\
    {'label': 'type', 'namespace': 'www.w3.org'}

logger.info('Stats for original graph before running OWL-NETS')
pkt.utils.derives_graph_statistics(graph)

logger.info('Initialize owlnets class')
owlnets = pkt.OwlNets(graph=graph,
                      write_location=working_dir + '/',
                      filename=file_from_uri(uri),
                      kg_construct_approach=None,
                      owl_tools=owltools_location + '/owltools')

logger.info('Remove disjointness with Axioms')
owlnets.removes_disjoint_with_axioms()

logger.info('Remove triples used only to support semantics')
cleaned_graph = owlnets.removes_edges_with_owl_semantics()
filtered_triple_count = len(owlnets.owl_nets_dict['filtered_triples'])
logger.info('removed {} triples that were not biologically meaningful'.format(filtered_triple_count))

logger.info('Gather list of owl:class and owl:axiom entities')
owl_classes = list(pkt.utils.gets_ontology_classes(owlnets.graph))
owl_axioms: list = []
for x in tqdm(set(owlnets.graph.subjects(RDF.type, OWL.Axiom))):
    src = set(owlnets.graph.objects(list(owlnets.graph.objects(x, OWL.annotatedSource))[0], RDF.type))
    tgt = set(owlnets.graph.objects(list(owlnets.graph.objects(x, OWL.annotatedTarget))[0], RDF.type))
    if OWL.Class in src and OWL.Class in tgt:
        owl_axioms += [x]
    elif (OWL.Class in src and len(tgt) == 0) or (OWL.Class in tgt and len(src) == 0):
        owl_axioms += [x]
    else:
        pass
node_list = list(set(owl_classes) | set(owl_axioms))
logger.info('There are:\n-{} OWL:Class objects\n-{} OWL:Axiom Objects'. format(len(owl_classes), len(owl_axioms)))

logger.info('Decode owl semantics')
decoded_graph = owlnets.cleans_owl_encoded_entities(node_list)
decoded_graph = owlnets.gets_owlnets_graph()

logger.info('Update graph to get all cleaned edges')
owlnets.graph = cleaned_graph + decoded_graph

logger.info('Owlnets results')
str1 = 'Decoded {} owl-encoded classes and axioms. Note the following:\nPartially processed {} cardinality ' \
               'elements\nRemoved {} owl:disjointWith axioms\nIgnored:\n  -{} misc classes;\n  -{} classes constructed with ' \
               'owl:complementOf;\n  -{} classes containing negation (e.g. pr#lacks_part, cl#has_not_completed)\n' \
               'Filtering removed {} semantic support triples'
stats_str = str1.format(
    len(owlnets.owl_nets_dict['decoded_entities'].keys()), len(owlnets.owl_nets_dict['cardinality'].keys()),
    len(owlnets.owl_nets_dict['disjointWith']), len(owlnets.owl_nets_dict['misc'].keys()),
    len(owlnets.owl_nets_dict['complementOf'].keys()), len(owlnets.owl_nets_dict['negation'].keys()),
    len(owlnets.owl_nets_dict['filtered_triples']))
logger.info('=' * 80 + '\n' + stats_str + '\n' + '=' * 80)

# common_ancestor = 'http://purl.obolibrary.org/obo/BFO_0000001'
# owlnets.graph = owlnets.makes_graph_connected(owlnets.graph, common_ancestor)

logger.info(f"Writing owl-nets results files to directory '{working_dir}'")
owlnets.write_location = working_dir
owlnets.write_out_results(owlnets.graph)

edge_list_filename = working_dir + '/' + 'OWLNETS_edgelist.txt'
logger.info(f"Write edge list results to '{edge_list_filename}'")
with open(edge_list_filename, 'w') as out:
    out.write('subject' + '\t' + 'predicate' + '\t' + 'object' + '\n')
    for row in tqdm(owlnets.graph):
        out.write(str(row[0]) + '\t' + str(row[1]) + '\t' + str(row[2]) + '\n')

logger.info('Get all unique nodes in OWL-NETS graph')
nodes = set([x for y in [[str(x[0]), str(x[2])] for x in owlnets.graph] for x in y])

node_metadata_filename = working_dir + '/' + 'OWLNETS_node_metadata.txt'
logger.info(f"Write node metadata results to '{node_metadata_filename}'")
with open(node_metadata_filename, 'w') as out:
    out.write('node_id' + '\t' + 'node_namespace' + '\t' + 'node_label' + '\t' + 'node_synonyms' + '\t' + 'node_dbxrefs' + '\n')
    for x in tqdm(nodes):
        if x in entity_metadata['nodes'].keys():
            namespace = entity_metadata['nodes'][x]['namespace']
            labels = entity_metadata['nodes'][x]['label']
            synonyms = entity_metadata['nodes'][x]['synonyms']
            dbxrefs = entity_metadata['nodes'][x]['dbxrefs']
            out.write(x + '\t' + namespace + '\t' + labels + '\t' + synonyms + '\t' + dbxrefs + '\n')

logger.info('Get all unique nodes in OWL-NETS graph')
relations = set([str(x[1]) for x in owlnets.graph])

relation_filename = working_dir + '/' + 'OWLNETS_relations.txt'
logger.info(f"Writing relation metadata results to '{relation_filename}'")
with open(relation_filename, 'w') as out:
    out.write('relation_id' + '\t' + 'relation_namespace' + '\t' + 'relation_label' + '\n')
    for x in tqdm(relations):
        if x in entity_metadata['relations']:
            if 'namespace' in entity_metadata['relations'][x]:
                namespace = entity_metadata['relations'][x]['namespace']
                if 'label' in entity_metadata['relations'][x]:
                    label = entity_metadata['relations'][x]['label']
                    out.write(x + '\t' + namespace + '\t' + label + '\n')
                else:
                    logger.error(f"entity_metadata['relations'][{x}]['label'] not found in: {entity_metadata['relations'][x]}")
            else:
                logger.error(f"entity_metadata['relations'][{x}]['namespace'] not found in: {entity_metadata['relations'][x]}")
        else:
            logger.error(f"entity_metadata['relations'][{x}] not found in: {entity_metadata['relations']}")

log_files_and_sizes(working_dir)

# Add log entry for how long it took to do the processing...
elapsed_time = time.time() - start_time
logger.info('Done! Elapsed time %s', "{:0>8}".format(str(timedelta(seconds=elapsed_time))))
