import argparse
import os
import sys
import traceback

from .algorithms.diameter import DiameterAlgorithm


def parse_cli_args():
    parser = argparse.ArgumentParser(
        description="Identify graph's diameter using Floyd Warshall algorithm and Adjacency Matrix structure")
    parser.add_argument("--directed-graph", dest='directed', action='store_true',
                        help="Specify this arg if the graph described at input_file is directed (Defaults to false)")
    io_type = parser.add_subparsers(dest='io_type', help="Selects input and output type")
    io_type.add_parser("stdio", help="Reads from stdin and writes to stdout")
    file_type = io_type.add_parser("file", help="Reads from input_file and writes to output_file")
    file_type.add_argument("input_file", help="Path to file containing a graph description.")
    file_type.add_argument("output_file", help="""Valid path for file to which output will be redirected
(Warning: any file on output path will be overwritten!)""")
    parser.set_defaults(directed=False)
    return parser.parse_args()


def read_input_file(args):
    try:
        if args.io_type == "stdio":
            v, e = map(int, input().split())
            input_ = [f"{v} {e}"]
            for _ in range(e):
                input_.append(input())
            return os.linesep.join(input_)
        else:
            with open(args.input_file) as f:
                return f.read()
    except Exception:
        traceback.print_exc()
        print("Could not read input file!")
        sys.exit(1)


def parse_graph(args, input_):
    try:
        return DiameterAlgorithm.from_str(input_, directed=args.directed)
    except Exception:
        traceback.print_exc()
        print("Failure creating adjacency matrix from input file's content.")
        sys.exit(1)


def start_algorithm(graph):
    try:
        graph.apply()
    except Exception:
        traceback.print_exc()
        print("Could not execute algorithm on built structure.")
        sys.exit(1)


def write_output_file(args, graph):
    try:
        if args.io_type == "stdio":
            print(graph.formatted_result())
        else:
            with open(args.output_file, 'w') as f:
                f.write(graph.formatted_result() + os.linesep)
    except Exception:
        traceback.print_exc()
        print("Could not write to output file!")
        sys.exit(1)


def main():
    args = parse_cli_args()
    input_ = read_input_file(args)
    graph = parse_graph(args, input_)
    start_algorithm(graph)
    write_output_file(args, graph)


if __name__ == '__main__':
    main()
