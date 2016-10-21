#!/usr/bin/ env python
# coding:utf-8

'''
# 组合特征
def extract_combination_feature(seg):
  list =[]
  if(len(seg) >= 16):
    # str = seg[2] + "_" + seg[15]
    list.append(process_id_feature("gender",seg[15])) 
    
    # str1 = seg[15] + "_" + seg[16]
    list.append(process_id_feature("age",seg[16])) 

    # str2 = seg[10] + "_" + seg[16]
    #list.append(process_id_feature("user_age",str2)) 

    str3 = seg[2] + "_" + seg[6]
    list.append(process_id_feature("query_ad",str3)) 

    str4 = seg[2] + "_" + seg[10]
    list.append(process_id_feature("all_user",str4)) 

    str5 = seg[6] + "_" + seg[10]
    list.append(process_id_feature("query_user",str5)) 
    
    str6 = seg[6] + "_" + seg[9]
    list.append(process_id_feature("query_desc",str6)) 
  return list


def extract_numerical_feature(seg):
  list = []
  num_query = len(seg[11].strip().split("|"))
  num_keywords = len(seg[12].strip().split("|"))
  num_title = len(seg[13].strip().split("|"))
  num_description = len(seg[14].strip().split("|"))
  list.append(str(process_id_feature("num_query"," ")) + ":" + str(num_query)) 
  list.append(str(process_id_feature("num_keywords"," ")) + ":" + str(num_keywords)) 
  list.append(str(process_id_feature("num_title"," ")) + ":" + str(num_title)) 
  list.append(str(process_id_feature("num_description"," ")) + ":" + str(num_description)) 

# extract tfinf feature of all tokens

  #gender = seg[15].strip().split("\t")[1]
  #age = seg[15].strip().split("\t")[2]
  #list.append(str(process_id_feature("gender"," ")) + ":" + str(gender)) 
  #list.append(str(process_id_feature("age"," ")) + ":" + str(age)) 

  corpus = seg[11:15]
  tfidf = tf_idf(corpus)
  
  query_similar_keywords = tfidf_similarity(tfidf[0],tfidf[1])
  query_similar_title = tfidf_similarity(tfidf[0],tfidf[2])
  query_similar_description = tfidf_similarity(tfidf[0],tfidf[3])
  keyword_similar_title = tfidf_similarity(tfidf[1],tfidf[3])
  keyword_similar_description = tfidf_similarity(tfidf[1],tfidf[3])
  title_similar_description = tfidf_similarity(tfidf[2],tfidf[3])

  list.append(str(process_id_feature("query_similar_keywords"," ")) + ":" + str(query_similar_keywords)) 
  list.append(str(process_id_feature("query_similar_title"," ")) + ":" + str(query_similar_title)) 
  list.append(str(process_id_feature("query_similar_description"," ")) + ":" + str(query_similar_description)) 
  list.append(str(process_id_feature("keyword_similar_title"," ")) + ":" + str(keyword_similar_title)) 
  list.append(str(process_id_feature("keyword_similar_description"," ")) + ":" + str(keyword_similar_description)) 
  list.append(str(process_id_feature("title_similar_description"," ")) + ":" + str(title_similar_description)) 


  #list.append(str(process_id_feature("sum_idf_query"," ")) + ":" + str(sum(tfidf[0])) 
  #list.append(str(process_id_feature("sum_idf_keyword"," ")) + ":" + str(sum(tfidf[1])) 
  #list.append(str(process_id_feature("sum_idf_title"," ")) + ":" + str(sum(tfidf[2])) 
  #list.append(str(process_id_feature("sum_idf_description"," ")) + ":" + str(sum(tfidf[3])) 

  depth = float(seg[4])
  postion = float(seg[5])
  relative_pos = float((depth-postion)*10.0/depth)

  #list.append(str(process_id_feature("depth_num"," ")) + ":" + str(depth) 
  #list.append(str(process_id_feature("postion_num"," ")) + ":" + str(postion) 
  list.append(str(process_id_feature("relative_pos_num"," ")) + ":" + str(relative_pos) 
  """
  raw_query = int(seg[6])
  raw_user = int(seg[10])
  list.append(str(process_id_feature("raw_query"," ")) + ":" + str(raw_query) 
  list.append(str(process_id_feature("raw_user"," ")) + ":" + str(raw_user) 
  """
  return list

def cate_to_str(label,list):
  line=lable

# 添加前缀标识
def process_id_feature(prefix,id):
  global feature_map
  global feature_index
  str = prefix + "_" + id
  if str in feature_map:
    return feature_map[str]
  else:
    feature_index = feature_index + 1
    feature_map[str] = feature_index
    return feature_index


'''































