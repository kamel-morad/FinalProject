import sys
import argparse
from utils.fairseq_utils import *  


parser = argparse.ArgumentParser()
parser.add_argument('--round_name')
parser.add_argument('--gpu_id', default='0')
parser.add_argument('--continue_from', default='', help='Path of the model to continue from')
parser.add_argument('--max_epoch', type=int, default=3)
args = parser.parse_args()


data_dir = Path('data')
round_dir = data_dir/args.round_name
data_paired_dir = round_dir/'data_paired'
fairseq_dir = data_paired_dir/'fairseq_preprocess'



# This code is a script that uses the Fairseq library to train a fixer model on paired data, it takes
# command-line arguments for the round name, GPU ID, continue_from, and max_epoch. It 
# first sets the path for the data directory, creates a directory for the paired data, preprocesses 
# the paired data by calling fairseq_preprocess function and then trains the fixer model by 
# calling fairseq_train function. The script also allows to continue the training from a 
# checkpoint if it is provided in the continue_from argument.




#Preprocess
fairseq_preprocess(src='bad', tgt='good', workers=20,
                      destdir  = str(data_paired_dir/'fairseq_preprocess'),
                      trainpref= str(data_paired_dir/'train'),
                      validpref= str(data_paired_dir/'dev'),
                      srcdict  = str(data_dir/'token_vocab.txt') )

#Train
save_dir = round_dir/'model-fixer'; save_dir.mkdir(exist_ok=True)
if not args.continue_from:
    fairseq_train(args.gpu_id, str(fairseq_dir), str(save_dir), str(save_dir/'train.log.txt'),
                    src='bad', tgt='good',
                    criterion='label_smoothed_cross_entropy', label_smoothing=0.1,
                    lr=1e-3, warmup_init_lr=1e-4, memory_efficient_fp16=True,
                    encoder_layers=4, decoder_layers=4, encoder_embed_dim=256, decoder_embed_dim=256,
                    encoder_ffn_embed_dim=1024, decoder_ffn_embed_dim=1024,
                    max_tokens=13500, update_freq=2,
                    max_epoch=args.max_epoch, save_interval_updates=10000, num_workers=4,
                )
else:
    fairseq_train(args.gpu_id, str(fairseq_dir), str(save_dir), str(save_dir/'train.log.txt'),
                    src='bad', tgt='good',
                    criterion='label_smoothed_cross_entropy', label_smoothing=0.1,
                    lr=1e-3, warmup_init_lr=1e-4, memory_efficient_fp16=True,
                    encoder_layers=4, decoder_layers=4, encoder_embed_dim=256, decoder_embed_dim=256,
                    encoder_ffn_embed_dim=1024, decoder_ffn_embed_dim=1024,
                    max_tokens=13500, update_freq=2,
                    max_epoch=args.max_epoch, save_interval_updates=10000, num_workers=4,
                    restore_file=args.continue_from, reset=True,
                )
