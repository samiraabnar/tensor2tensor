import random

def reber_prime_bad():
  """ Returns the non-embedded, internal string
  """
  string = "B"
  luck = random.random()

  if luck < 0.5:
      string = reber_phase_a_bad(string)
      luck = random.random()
      if luck < 0.5:
          string += "T"
          string = reber_phase_b_bad(string)
      else:
          string += "SE"

  else:
      string += "P"
      string = reber_phase_b_bad(string)

  return string

def reber_phase_a_bad(string):
  """ Returns a portion of the string corresponding to the top half of the graph
  :param string:
  :return:
  """
  string += "X"
  luck = random.random()

  while luck < 0.5:
      string += "S"
      luck = random.random()

  string += "P"

  return string

def reber_phase_b_bad(string):
  """ Returns a portion of the string corresponding to the bottom half of the graph

  :param string:
  :return:
  """
  string += "T"
  luck = random.random()

  while luck < 0.5:
      string += "T"
      luck = random.random()

  string += "V"

  luck = random.random()
  if luck < 0.5:
      string += "PE"
      luck = random.random()
      if luck < 0.5:
          string += "X"
          string = reber_phase_b_bad(string)
      else:
          string += "SE"

  else:
      string += "VE"

  return string

def embedded_reber_bad():
  """ Returns a complete, false embedded reber grammar string
  :return:
  """
  string = "B"
  luck = random.random()

  if luck < 0.5:
      string += "P"
      string += reber_prime_bad()
      luck = random.random()
      if luck < 0.5:
          string += "PE"
      else:
          string += "TE"

  else:
      string += "T"
      string += reber_prime_bad()
      if luck < 0.5:
          string += "TE"
      else:
          string += "PE"

  return string

def reber_prime():
  """ Returns the non-embedded, internal string

  :return:
  """
  string = "B"
  luck = random.random()

  if luck < 0.5:
      string = reber_phase_a(string)
      luck = random.random()
      if luck < 0.5:
          string += "X"
          string = reber_phase_b(string)
      else:
          string += "SE"

  else:
      string += "P"
      string = reber_phase_b(string)

  return string

def reber_phase_a(string):
  """ Returns a portion of the string corresponding to the top half of the graph

  :param string:
  :return:
  """
  string += "T"
  luck = random.random()

  while luck < 0.5:
      string += "S"
      luck = random.random()

  string += "X"

  return string


def reber_phase_b(string):
  """ Returns a portion of the string corresponding to the bottom half of the graph

  :param string:
  :return:
  """
  string += "T"
  luck = random.random()

  while luck < 0.5:
      string += "T"
      luck = random.random()

  string += "V"

  luck = random.random()
  if luck < 0.5:
      string += "P"
      luck = random.random()
      if luck < 0.5:
          string += "X"
          string = reber_phase_b(string)
      else:
          string += "SE"

  else:
      string += "VE"

  return string


def embedded_reber():
  """ Returns a complete, embedded reber grammar string

  :return:
  """
  string = "B"
  luck = random.random()

  if luck < 0.5:
      string += "P"
      string += reber_prime()
      string += "PE"

  else:
      string += "T"
      string += reber_prime()
      string += "TE"

  return string
