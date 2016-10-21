#!/usr/bin/env python
# coding:utf-8


def tf_idf(corpus):
  lst = []
  voc = {}
  index = 0
  for text in corpus:
    tokens = text.strip().split("|")
    for t in tokens:
      if t in voc:
        continue
      else:
        voc[t] = index
        index += 1
    lst.append(tokens)

  #print lst
  vector = []
  for text in lst:
    vec = [0] * len(voc)
    for t in text:
      # calculate term frequency
      index = voc[t]
      vec[index] += 1

    m = float(max(vec))
    norm_vec = [ x / m for x in vec ]
    vector.append(norm_vec)
  #print vector
  # idf
  idf = [0] * len(voc)
  for v in vector:
    for (i,c) in enumerate(v):
      if c!=0:
        idf[i] += c/c   # 这里应该写错了
      else:
        continue
  N = float(len(vector))
  idf = [ math.log(1 + N/x,2) for x in idf ]
  #print idf


  #tf - idf
  lst_tfidf = []

  for v in vector:
   max_tf = float(max(v))

