import math

class VectorCompare:
  def magnitude(self,concordance):
    if not isinstance(concordance, dict):
      raise ValueError('Supplied Argument should be of type dict')
    total = 0
    for word,count in concordance.items():
      total += count ** 2
    return math.sqrt(total)

  def relation(self,concordance1, concordance2):
    if not isinstance(concordance1, dict):
      raise ValueError('Supplied Argument 1 should be of type dict')
    if not isinstance(concordance2, dict):
      raise ValueError('Supplied Argument 2 should be of type dict')
    relevance = 0
    topvalue = 0
    for word, count in concordance1.items():
      if word in concordance2:
        topvalue += count * concordance2[word]
    if (self.magnitude(concordance1) * self.magnitude(concordance2)) != 0:
      return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))
    else:
      return 0

  def concordance(self,document):
    if not isinstance(document, str):
      raise ValueError('Supplied Argument should be of type string')
    con = {}
    for word in document.split(' '):
      if word in con:
        con[word] = con[word] + 1
      else:
        con[word] = 1
    return con