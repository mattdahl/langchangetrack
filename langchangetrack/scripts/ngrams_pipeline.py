#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Pipeline to train a corpus of ngrams"""

from argparse import ArgumentParser
import logging
import sys
from io import open
from os import path
from time import time
from glob import glob
import subprocess

__author__ = "Vivek Kulkarni"
__email__ = "viveksck@gmail.com"

LOGFORMAT = "%(asctime).19s %(levelname)s %(filename)s: %(lineno)s %(message)s"


def main(args):
    train_cmd = "/code/langchangetrack/langchangetrack/utils/scripts/train_models.sh {} {} {} {} {} {}".format(args.corpus_dir, args.working_dir, args.ext, args.window, args.epochs, args.workers)
    subprocess.check_call(train_cmd, shell=True)

    cmd = "detect_cp_distributional.sh {} {} {} {} {} {} {} {} {} {} {} {}"
    input_dir = path.join(args.working_dir, 'models')
    cmd = cmd.format(input_dir, args.working_dir, args.output_dir, args.start, args.end, args.step, args.model_family, args.knn, args.vocab_file, args.bootstrap, args.threshold, args.workers)
    subprocess.check_call(cmd, shell=True)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--corpus-dir", dest="corpus_dir", help="Corpus directory")
    parser.add_argument("--file-extension", dest="ext", help="Corpus file extension")
    parser.add_argument("--working-dir", dest="working_dir", help="Working directory")
    parser.add_argument("--output-dir", dest="output_dir", help="Output directory")
    parser.add_argument("--context-size", dest="window", default=5, type=int, help="Context size to use for training embeddings")
    parser.add_argument("--epochs", dest="epochs", default=3, type=int, help="Number of epochs to training embeddings")
    parser.add_argument("--start-time-point", dest="start", help="Start time point")
    parser.add_argument("--end-time-point", dest="end", help="End time point")
    parser.add_argument("--step-size", dest="step", help="Step size for timepoints")
    parser.add_argument("--model-family", dest="model_family", default="locallinear", help="Model family default (locallinear)")
    parser.add_argument("--number-nearest-neighbors", dest="knn", default=1000,
                        type=int, help="Number of nearest neighbors to use for mapping to joint space (default:1000)")
    parser.add_argument("--vocabulary-file", dest="vocab_file", help="Common vocabulary file")
    parser.add_argument("--threshold", dest="threshold", default=1.75, type=float, help="Threshold for mean shift model for change point detection")
    parser.add_argument("--bootstrap-samples", dest="bootstrap", default=1000, type=int, help="Number of bootstrap samples to draw")
    parser.add_argument("--workers", dest="workers", default=1, type=int, help="Maximum number of workers")
    parser.add_argument("-l", "--log", dest="log", help="log verbosity level",
                        default="INFO")
    args = parser.parse_args()
    if args.log == 'DEBUG':
        sys.excepthook = debug
    numeric_level = getattr(logging, args.log.upper(), None)
    logging.basicConfig(level=numeric_level, format=LOGFORMAT)
    main(args)
