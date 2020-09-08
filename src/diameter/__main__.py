import argparse, sys, os, traceback

from .algorithms.diameter import DiameterAlgorithm


def parse_cli_args():
    parser = argparse.ArgumentParser(
        description="Identify graph's diameter using Floyd Warshall algorithm and Adjacency Matrix structure")
    parser.add_argument("input_file", help="Path to file containing a graph description.")
    parser.add_argument("output_file", help="""Valid path for file to which output will be redirected 
(Warning: any file on output path will be overwritten!)""")
    parser.add_argument("--directed-graph", dest='directed', action='store_true',
                        help="Specify this arg if the graph described at input_file is directed (Defaults to false)")
    parser.set_defaults(directed=False)
    return parser.parse_args()


def read_input_file(args):
    try:
        with open(args.input_file) as f:
            return f.read()
    except Exception as er:
        traceback.print_exc()
        print("Could not read input file!")
        sys.exit(1)


def parse_graph(args):
    try:
        return DiameterAlgorithm.from_str(input_, directed=args.directed)
    except Exception as er:
        traceback.print_exc()
        print("Failure creating adjacency matrix from input file's content.")
        sys.exit(1)


def start_algorithm():
    try:
        graph.apply()
    except Exception as er:
        traceback.print_exc()
        print("Could not execute algorithm on built structure.")
        sys.exit(1)


def write_output_file(args):
    try:
        with open(args.output_file, 'w') as f:
            f.write(graph.formatted_result()+os.linesep)
    except Exception as er:
        traceback.print_exc()
        print("Could not write to output file!")
        sys.exit(1)


if __name__ == '__main__':
    args = parse_cli_args()
    input_ = read_input_file(args)
    graph = parse_graph(args)
    start_algorithm()
    write_output_file(args)
