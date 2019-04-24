import os
import json

from annotator.offline.datasets import SemEval2010Task8
from annotator.offline.utils import make_path

"""
Converts various datasets into a jsonl format.
The following datasets can be converted:
    Semeval 2010 Task 8:
        Paper: http://www.aclweb.org/anthology/S10-1006
        Download: http://www.kozareva.com/downloads.html
    KBP37:
        Paper: https://arxiv.org/abs/1508.01006
        Download: https://github.com/zhangdongxu/kbp37
    TACRED:
        Paper: https://nlp.stanford.edu/pubs/zhang2017tacred.pdf
        Download: LDC publication pending


Exemplary conversion for the Semeval 2010 Task 8 Format:
9       "The <e1>lawsonite</e1> was contained in a <e2>platinum crucible</e2> and the counter-weight was a plastic crucible with metal pieces."
Content-Container(e1,e2)
Comment: prototypical example

JSONL output Format:
{
  "id": "9",
  "tokens": ["The", "lawsonite", "was", "contained", "in", "a", "platinum", "crucible", "and", "the", "counter-weight", "was", "a", "plastic", "crucible", "with", "metal", "pieces", "."],
  "label": "Content-Container(e1,e2)",
  "entities": [[1, 2], [6, 8]]
}
"""


class DatasetConverter:

    def __init__(self, file_name, input_dir, output_dir):

        # self.input_test_file = os.path.join(dataset_dir, "SemEval2010_task8_testing_keys", "TEST_FILE_FULL.TXT")
        self.input_test_file = os.path.join(input_dir, file_name)

        self.output_dir = output_dir

        self.output_test_file = os.path.join(output_dir, "test.jsonl")

        self.glove_mapping = {
            '-LRB-': '(',
            '-RRB-': ')',
            '-LSB-': '[',
            '-RSB-': ']',
            '-LCB-': '{',
            '-RCB-': '}'
        }
        import pudb
        pudb.set_trace()

    def run(self):
        print("Converting dataset to jsonl")
        os.makedirs(self.output_dir, exist_ok=True)

        self._run_normally()

    def _run_normally(self):
        self._convert_semeval_format_file(self.input_test_file, self.output_test_file)

    def _convert_semeval_format_file(self, input_path, output_path):
        with open(input_path, mode="r") as input_file, \
                open(output_path, mode="w") as output_file:
            while True:
                tokens_line = input_file.readline()
                if not tokens_line:
                    break

                (index, tokens_string) = tokens_line.split('\t', maxsplit=1)  # separate index and tokens
                tokens_string = tokens_string.strip()[1:-1]  # remove quotation marks
                tokens = self._split_tokens(tokens_string)

                tokens, first_args, second_args = self._parse_args(tokens)

                relation_label = input_file.readline().strip()  # Remove trailing newline
                _ = input_file.readline()  # Comment string
                _ = input_file.readline()  # Empty line separator

                example = {
                    "id": index,
                    "tokens": tokens,
                    "label": relation_label,
                    "entities": [first_args, second_args]
                }

                output_file.write(json.dumps(example) + "\n")

    @staticmethod
    def _split_tokens(tokens_string):
        prepared_string = tokens_string \
            .replace(".", " . ") \
            .replace("<e1>", " <e1>") \
            .replace("</e1>", "</e1> ") \
            .replace("<e2>", " <e2>") \
            .replace("</e2>", "</e2> ") \
            .replace(",", " , ") \
            .replace("'", " ' ") \
            .replace("!", " ! ") \
            .replace("?", " ? ")
        return [token.strip() for token in prepared_string.split(" ") if len(token.strip()) > 0]

    @staticmethod
    def split_tokens_and_entities(tokens_string):
        tokens = DatasetConverter._split_tokens(tokens_string.strip())
        tokens, first_args = DatasetConverter._parse_arg(tokens, 'e1')
        tokens, second_args = DatasetConverter._parse_arg(tokens, 'e2')
        return tokens, first_args, second_args

    def _parse_args(self, tokens):
        tokens, first_args = self._parse_arg(tokens, 'e1')
        tokens, second_args = self._parse_arg(tokens, 'e2')
        return tokens, first_args, second_args

    @staticmethod
    def _parse_arg(tokens, arg_label):
        """
        Parses a relation argument with the given xml entity label.
        Returns the tokens without the xml entity label and the token offsets of the argument.
        """
        start_tag = '<' + arg_label + '>'
        end_tag = '</' + arg_label + '>'
        cleaned_tokens = []

        arg_start_idx = None
        arg_end_idx = None

        # track the index difference due to removed empty tokens
        cleaned_tokens_offset = 0

        for index, token in enumerate(tokens):

            if token.startswith(start_tag):
                arg_start_idx = index - cleaned_tokens_offset
                token = token[len(start_tag):]  # clean the tag from the token

            if token.endswith(end_tag):
                token = token[:-len(end_tag)]  # clean the tag from the token

                # If the current token is now empty, it is going to be removed
                # and the end offset will be a token earlier
                if DatasetConverter._is_empty_token(token):
                    arg_end_idx = index - cleaned_tokens_offset
                else:
                    arg_end_idx = index - cleaned_tokens_offset + 1

            if DatasetConverter._is_empty_token(token):
                cleaned_tokens_offset += 1
            else:
                cleaned_tokens.append(token)

        assert arg_start_idx is not None and arg_end_idx is not None, "Argument offsets could not be found"

        return cleaned_tokens, (arg_start_idx, arg_end_idx)

    def _convert_tacred_format_file(self, input_file, output_file):
        with open(output_file, 'w') as output_file:
            for example in self._read_tacred_file(input_file):
                output_file.write(json.dumps(example) + "\n")

    def _read_tacred_file(self, input_file):
        with open(input_file, 'r') as input_file:
            input_examples = json.loads(input_file.readline())
            for input_example in input_examples:
                tokens = input_example['token']
                subj_offsets = (input_example['subj_start'], input_example['subj_end'] + 1)
                obj_offsets = (input_example['obj_start'], input_example['obj_end'] + 1)

                tokens = self.normalize_glove_tokens(tokens)

                output_example = {
                    "id": input_example['id'],
                    "tokens": tokens,
                    "label": input_example['relation'],
                    "entities": (subj_offsets, obj_offsets),
                    "grammar": ('SUBJ', 'OBJ'),
                    "type": (input_example['subj_type'], input_example['obj_type'])
                }

                yield output_example

    def normalize_glove_tokens(self, tokens):
        return [self.glove_mapping[token]
                if token in self.glove_mapping
                else token
                for token in tokens]

    @staticmethod
    def _is_empty_token(token):
        return len(token.strip()) == 0
