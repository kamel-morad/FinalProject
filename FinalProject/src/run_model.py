import sys
import argparse
import os
from utils.fairseq_utils import *  


parser = argparse.ArgumentParser()
parser.add_argument('--round_name')
parser.add_argument('--destdir_root', default='')
parser.add_argument('--gpu_ids', default='0', help='Comma separated list')
args = parser.parse_args()
args.gpu_ids = args.gpu_ids.split(",")



#This code uses the Fairseq library to preprocess and generate fixer predictions for original bad code. The script takes in command-line arguments for the round name, the destination root directory, and GPU IDs.
#It first imports necessary modules and parses the command-line arguments. Then, it sets the path for the data directory and the round directory, and initializes the number of splits to 5.
#It then starts a loop to preprocess the inputs, where it calls the fairseq_preprocess function to preprocess the original bad code. The function takes in the source and target files, the number of workers, the destination directory, the test prefix, the source dictionary, and the flag only_source. 
#It then copies the token_vocab.txt file to the destination directory.
#After preprocessing the inputs, the script runs the fixer by calling the fairseq_generate function for each split. This function takes in GPU ID, destination directory, model path, prediction path, source and target files, subset, use_Popen, beam, nbest, max_len_a, max_len_b and max_tokens.
#Finally, the script uses Popen to wait for all the processes to complete, if use_Popen is True.

data_dir = Path('data')
round_dir = data_dir/args.round_name
destdir_root = Path(args.destdir_root) if args.destdir_root else round_dir/'orig_bad'


n_splits = 5  #all the original bad code is split into 5 chunks for faster processing

#Preprocess inputs
for split in range(n_splits):
    destdir    = destdir_root/f'fairseq_preprocess__orig_bad.{split}'
    if os.path.exists(str(destdir)):
        continue
    fairseq_preprocess(src='bad', tgt='good', workers=10,
                          destdir  = str(destdir),
                          testpref = str(data_dir/f'orig_bad_code/orig.{split}'),
                          srcdict  = str(data_dir/'token_vocab.txt'),
                          only_source=True )
    os.system('cp {} {}'.format(data_dir/'token_vocab.txt', destdir/'dict.good.txt'))

#Run fixer
model_dir  = round_dir/'model-fixer'
model_path = model_dir/'checkpoint.pt'
gpus = (args.gpu_ids * (n_splits//len(args.gpu_ids) +1))[:n_splits]
use_Popen = (len(args.gpu_ids) > 1)
ps = []
for split, gpu in zip(range(n_splits), gpus):
    destdir    = destdir_root/f'fairseq_preprocess__orig_bad.{split}'
    pred_path  = destdir/'model-fixer.pred.txt'
    p = fairseq_generate(str(gpu), str(destdir), str(model_path), str(pred_path),
                      src='bad', tgt='good', gen_subset='test', use_Popen=use_Popen,
                      beam=10, nbest=10, max_len_a=1, max_len_b=50, max_tokens=7000)
    ps.append(p)

if use_Popen:
    exit_codes = [p.wait() for p in ps]
