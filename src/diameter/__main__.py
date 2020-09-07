from __future__ import with_statement
from __future__ import absolute_import
import argparse
import sys
import codecs
from algorithms.diameter import DiameterAlgorithm
from io import open


def parse_cli_args():
    parser = argparse.ArgumentParser(
        description=u"Identify graph's diameter using Floyd Warshall algorithm and Adjacency Matrix structure")
    parser.add_argument(u"input_file", help=u"Path to file containing a graph description.")
    parser.add_argument(u"output_file", help=u"""Valid path for file to which output will be redirected 
(Warning: any file on output path will be overwritten!)""")
    parser.add_argument(u"--directed-graph", dest=u'directed', action=u'store_true',
                        help=u"Specify this arg if the graph described at input_file is directed (Defaults to false)")
    parser.set_defaults(directed=False)
    return parser.parse_args()


def read_input_file(args):
    try:
        with open(args.input_file) as f:
            return f.read()
    except Exception, er:
        print er
        print u"Could not read input file!"
        sys.exit(1)


def parse_graph(args):
    try:
        return DiameterAlgorithm.from_str(input_, directed=args.directed)
    except Exception, er:
        print er
        print u"Failure creating adjacency matrix from input file's content."
        sys.exit(1)


def start_algorithm():
    try:
        graph.apply()
    except Exception, er:
        print er
        print u"Could not execute algorithm on built structure."
        sys.exit(1)


def write_output_file(args):
    try:
        with codecs.open(args.output_file, u'w', "utf-8-sig") as f:
            f.write(graph.formatted_result())
    except Exception, er:
        print er
        print u"Could not write to output file!"
        sys.exit(1)


if __name__ == u'__main__':
    args = parse_cli_args()
    input_ = read_input_file(args)
    graph = parse_graph(args)
    start_algorithm()
    write_output_file(args)
