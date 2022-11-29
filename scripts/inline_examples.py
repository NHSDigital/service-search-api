#!/usr/bin/env python

import json
import os
import sys

from jsonpath_ng import parse

SPEC_DIR = f"{os.path.dirname(os.path.realpath(__file__))}/../specification"


def main(file: str):
    with open(file, 'r') as f:
        spec = json.load(f)

        req_path = parse("$.paths.['/'].get.responses.*.content.['application/json'].examples.*.['$ref']")
        req_examples = req_path.find(spec)
        inline_examples(spec, req_examples)

        req_path = parse(
            "$.paths.['/search-postcode-or-place'].post.responses.*.content.['application/json'].examples.*.['$ref']")
        req_examples = req_path.find(spec)
        inline_examples(spec, req_examples)

        req_path = parse(
            "$.paths.['/organisationtypes'].get.responses.*.content.['application/json'].examples.*.['$ref']")
        req_examples = req_path.find(spec)
        inline_examples(spec, req_examples)

        print(json.dumps(spec))


def inline_examples(spec, examples_path):
    for example in examples_path:
        ref = example.full_path
        example_file_content = read_example_from_component(spec, ref)

        example_path = ref.left
        example_path.update(spec, example_file_content)


def read_example_from_component(spec: dict, path):
    component = path.find(spec)[0].value
    com_path = component.replace("#/", "").replace("/", ".")
    example_path = parse(f"$.{com_path}")
    return example_path.find(spec)[0].value


if __name__ == '__main__':
    main(sys.argv[1])
