import io
import sys
import json, os, re
import token
import numpy as np
import editdistance
from collections import defaultdict, OrderedDict, Counter
from copy import deepcopy

sys.path.insert(0, 'utils')
from code_tokenizer import tokenize


vocab_file = 'data/token_vocab.txt' # File containing vocabulary of tokens
vocab = set([line.split()[0] for line in open(vocab_file)])

def toks2lines(code_toks_raw):
    #Convert a list of tokens to a list of lines, where each line is a list of tokens
    lines = []
    line = []
    for tok in code_toks_raw:
        if tok in {'<NL>', '<NEWLINE>'}:# Append newline token to current line and append line to lines
            line.append(tok)
            lines.append(line); line = []
        else:
            line.append(tok)
    if line:# If there is any remaining token in the current line, append it to lines
        lines.append(line)
    return lines

def preprocess_unk(code_toks_raw):
    ret = []
    unk_dict = []
    for tok in code_toks_raw:
        if tok not in vocab:
            ret.append('<unk>') # If the token is not in the vocabulary, replace it with the <unk> token
            unk_dict.append(tok)# Keep track of the original token for later use
        else:
            ret.append(tok)# If the token is in the vocabulary, keep it as is
                           #return ret, unk_dict # Return the modified list of tokens and the list of original tokens that were replaced with <unk>
    return ret, unk_dict

def code_toks_to_code_string(code_toks_joined, anonymize_dict=None):
    # If anonymize_dict is not None, make a deep copy of it
    if anonymize_dict is not None:
        anonymize_dict = deepcopy(anonymize_dict)
    # Default replace map for different tokens
    default_replace_map = {'<unk>': 'unk',
                          '<COMMENT>': '##',
                          '<NUMBER>' : '1',
                          '<STRING>' : '"str"'}
    # Initialize indentation                      
    cur_indent  = 0
    indent_unit = '    '
    toks = code_toks_joined.split()
    final_toks = []
    startline = True
    for tok in toks:
        tok_post = None
        if tok == '<INDENT>':
            cur_indent += 1
            continue
        elif tok == '<DEDENT>':
            cur_indent -= 1
            continue
        elif tok in ('<NEWLINE>', '<NL>'):
            final_toks.append('\n')
            startline = True
            continue
        if startline:
            cur_indent = max(0, cur_indent)
            final_toks.append(indent_unit * cur_indent)
            startline = False
        else:
            final_toks.append(' ')
        if (anonymize_dict is not None) and (tok in anonymize_dict) and (len(anonymize_dict[tok]) > 0): # If anonymize_dict is not None and the token exists in it, use the first value in the list
            tok_post = anonymize_dict[tok].pop(0)
        else:
            # If token is not in the anonymize_dict or the list is empty, use the default replace map
            tok_post = default_replace_map[tok] if tok in default_replace_map else tok
        final_toks.append(tok_post)
    code = "".join(final_toks)
    return code

def get_diff_metric(src, pred):
    src_toks  = src.split()
    pred_toks = pred.split()
    diff_metric = editdistance.eval(src_toks, pred_toks)
    return diff_metric



def tokenize_python_code(code_string):
    # This function takes in a string of python code, 
    # tokenize it using the tokenize function imported from code_tokenizer, 
    # filters out the tokens that are not needed, and returns the tokenized code and the anonymize_dict.
    try:
        # Tokenize the code using the tokenize function imported from code_tokenizer
        tokens = tokenize(io.BytesIO(code_string.encode('utf8')).readline)
        toks = [t for t in tokens]
    except Exception as e:
        print (e)
        return 1
        # Define the set of special tokens that we will be keeping in the tokenized code
    SPECIAL = {'STRING', 'COMMENT', 'INDENT', 'DEDENT', 'NEWLINE', 'NL'}
    # Define the set of tokens that we will be ignoring
    IGNORE = {'ENCODING', 'ENDMARKER'}
    # Initialize the tokenized code list
    toks_raw = []
    # Initialize the anonymize_dict which will store the original strings of special tokens
    anonymize_dict = defaultdict(list)
    for tok in toks:
        tok_type_name = token.tok_name[tok.type]
        if tok_type_name in IGNORE:
            continue
        # If the token is in SPECIAL set, add the token type to the tokenized code list, and add the original string to the anonymize_dict
        elif tok_type_name in SPECIAL:
            toks_raw.append(f'<{tok_type_name}>')
            if tok_type_name in {'STRING', 'COMMENT'}:
                anonymize_dict[f'<{tok_type_name}>'].append(tok.string)
                # If the token is not in special set, add the token string to the tokenized code list
        else:
            toks_raw.append(tok.string)
    assert len(toks_raw) == len(toks)-2
    # Return the tokenized code and anonymize_dict
    return toks_raw, anonymize_dict
