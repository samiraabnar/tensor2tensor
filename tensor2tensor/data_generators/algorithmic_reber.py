from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import shutil
import numpy as np
from six.moves import range  # pylint: disable=redefined-builtin
from tensor2tensor.data_generators import generator_utils as utils, text_problems
from tensor2tensor.data_generators import problem
from tensor2tensor.data_generators import text_encoder
from tensor2tensor.layers import modalities
from tensor2tensor.utils import metrics
from tensor2tensor.utils import registry
import tensorflow as tf
from tensor2tensor.data_generators.algorithmic import AlgorithmicProblem
import tensor2tensor.data_generators.algorithmic_reber_util as reber


@registry.register_problem
class ReberClassification(AlgorithmicProblem):
  """Problem spec classifying good and bad reber strings"""

  @property
  def num_symbols(self):
    return max(self.train_length, self.dev_length)

  @property
  def num_classes(self):
    return self.num_symbols

  def class_labels(self, data_dir=None):
    del data_dir
    return ["False", "True"]

  @property
  def train_length(self):
    return 40

  @property
  def dev_length(self):
    return self.train_length

  @property
  def vocab_type(self):
    return text_problems.VocabType.CHARACTER

  def generator(self, nbr_symbols, max_length, nbr_cases):
    """Generating for counting number of unique symbols in a sequence.
    The length of the sequence is drawn uniformly at random from [1, max_length]
    and then symbols are drawn uniformly at
    random from [0, nbr_symbols) until nbr_cases sequences have been produced.
    Args:
      nbr_symbols: number of symbols to use in each sequence.
      max_length: integer, maximum length of sequences to generate.
      nbr_cases: the number of cases to generate.
    Yields:
      A dictionary {"inputs": input-list, "targets": target-list} where
      target-list is input-list sorted.
    """
    class_labels = np.random.randint(0, 2, size=nbr_cases)
    for i in range(nbr_cases):
      c = class_labels[i]
      if c == 0:
        inputs = reber.embedded_reber_bad()
      else:
        inputs = reber.embedded_reber()

      yield {"inputs": inputs, "targets": self.class_labels[c]}

  def generate_data(self, data_dir, _, task_id=-1):

    utils.generate_dataset_and_shuffle(
      self.generate_encoded_samples(self.num_symbols, self.train_length, self.train_size),
      self.training_filepaths(data_dir, self.num_shards, shuffled=True),
      self.generate_encoded_samples(self.num_symbols, self.dev_length, self.dev_size),
      self.dev_filepaths(data_dir, 1, shuffled=True),
      shuffle=False)

  def generate_encoded_samples(self, nbr_symbols, max_length, nbr_cases):
    generator = self.generate_samples(nbr_symbols, max_length, nbr_cases)
    encoder = text_encoder.ByteTextEncoder()
    for sample in generator:
      inputs = encoder.encode(sample["inputs"])
      inputs.append(text_encoder.EOS_ID)
      label = sample["label"]
      yield {"inputs": inputs, "targets": [label]}

  def feature_encoders(self, data_dir):
    encoder = text_encoder.ByteTextEncoder()

    return {
        "inputs": encoder,
        "targets": text_encoder.ClassLabelEncoder(self.class_labels(data_dir))
    }

  def hparams(self, defaults, unused_model_hparams):
    p = defaults
    p.modality = {"inputs": modalities.ModalityType.SYMBOL,
                  "targets": modalities.ModalityType.CLASS_LABEL}
    p.vocab_size = {"inputs": self._encoders["inputs"].vocab_size,
                    "targets": self.num_classes}

  def example_reading_spec(self):
    data_fields = {
        "inputs": tf.VarLenFeature(tf.int64),
        "targets": tf.FixedLenFeature([1], tf.int64),
    }
    data_items_to_decoders = None
    return (data_fields, data_items_to_decoders)
