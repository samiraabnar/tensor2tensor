# coding=utf-8
# Copyright 2019 The Tensor2Tensor Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""TREC Question Classification 6"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import zipfile
from tensor2tensor.data_generators import generator_utils
from tensor2tensor.data_generators import problem
from tensor2tensor.data_generators import text_encoder
from tensor2tensor.data_generators import text_problems
from tensor2tensor.utils import registry
import tensorflow as tf
import os

import urllib.request

EOS = text_encoder.EOS


@registry.register_problem
class Trec6(text_problems.Text2ClassProblem):

  URLS = [
    'http://cogcomp.org/Data/QA/QC/train_5500.label',
    'http://cogcomp.org/Data/QA/QC/TREC_10.label'
  ]

  @property
  def is_generate_per_split(self):
    return True

  @property
  def dataset_splits(self):
    return [{
        "split": problem.DatasetSplit.TRAIN,
        "shards": 10,
    }, {
        "split": problem.DatasetSplit.EVAL,
        "shards": 1,
    }]

  @property
  def approx_vocab_size(self):
    return 2**14

  @property
  def num_classes(self):
    return 6

  def class_labels(self, data_dir=None):
    del data_dir
    return ["DESC", "ENTY", "ABBR", "HUM", "LOC", "NUM"]

  def _maybe_download_corpora(self, tmp_dir):
    trec6_train_filename = "train_5500.label"
    trec6_test_filename = "TREC_10.label"
    trec6_finalpath = os.path.join(tmp_dir, "trec6")

    if not os.path.isdir(trec6_finalpath):
        os.makedirs(trec6_finalpath)

    # Download train
    urllib.request.urlretrieve(Trec6.URLS[0], filename=os.path.join(trec6_finalpath,trec6_train_filename))
    # Download test
    urllib.request.urlretrieve(Trec6.URLS[1], filename=os.path.join(trec6_finalpath, trec6_test_filename))

    return trec6_finalpath

  def example_generator(self, filename):
    for idx, line in enumerate(tf.gfile.Open(filename, "rb")):
      line = line.decode("cp437").strip()#text_encoder.to_unicode_utf8(line.strip())
      label, sent = line.split(" ", 1)
      yield {
          "inputs": sent,
          "label": self.class_labels().index(label.split(":")[0])
      }

  def generate_samples(self, data_dir, tmp_dir, dataset_split):
    sst_binary_dir = self._maybe_download_corpora(tmp_dir)
    if dataset_split == problem.DatasetSplit.TRAIN:
      filesplit = "train_5500.label"
    else:
      filesplit = "TREC_10.label"

    filename = os.path.join(sst_binary_dir, filesplit)
    for example in self.example_generator(filename):
      yield example


