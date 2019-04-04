import math
import numpy as np
import networkx as nx

sentence_delimiters = ['…', '……', '?', '!', ';', '？', '！', '；', '。', '\n']
allow_speech_tags = ['an', 'i', 'j', 'l', 'n', 'nr', 'nrfg', 'ns', 'nt', 'nz', 't', 'v', 'vd', 'vn', 'eng']


class AttrDict(dict):
    """Dict that can get attribute by dot"""

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


# 两个句子的相似度
def similarity(word_list1, word_list2):
    words = list(set(word_list1 + word_list2))
    list1 = [float(word_list1.count(w)) for w in words]  # 每个词在句子1出现的次数
    list2 = [float(word_list2.count(w)) for w in words]

    list3 = [list1[i] * list2[i] for i in range(len(list1))]
    list4 = [1 for i in list3 if i > 0]  # 每个词如果均在两个句子中出现，则为1
    all_num = sum(list4)

    if abs(all_num) <= 1e-12:
        return 0

    denominator = math.log(float(len(word_list1))) + math.log(float(len(word_list2)))  # 分母
    if abs(denominator) < 1e-12:
        return 0

    return all_num / denominator


# 根据pr值将句子按关键程度从大到小排序，添加了权值
# sentences: 列表，元素为句子
# words: 二维列表，子列表与sentences列表的元素对应，子列表由对应句子的单词构成
# sim_function: 计算两个句子的相似度，作为句子的权值
# e1、e2为段首、段尾句子PR值的调整阈值
# u、v为段首、段尾句子数
# title为文章标题
# e3为句子与标题相似度比值大于w时PR值的调整阈值（e3*w>=1）
def sort_sentences(sentences, words, title_words, sim_function=similarity, e1=0.5, e2=0.1, u=4, v=4, e3=2, w=0.5):
    num = len(sentences)
    graph = np.zeros((num, num))  # 生成num行num列的零矩阵

    for x in range(num):
        for y in range(x, num):
            sim_value = sim_function(words[x], words[y])  # 句子x与句子y的相似度，即权值
            graph[x, y] = sim_value  # 无向有权图
            graph[y, x] = sim_value

    nx_graph = nx.from_numpy_matrix(graph)  # 从上面的矩阵中得到图
    scores = nx.pagerank(nx_graph)  # 返回pr值，字典类型：key为索引，value为分数

    #  根据句子位置进行PR值调整
    scores_second = []
    for index, score in scores.items():
        if index < u:  # 段首句子权值的递减调整
            adjust_value = 1 + e1 - index * e1 / u
        elif index >= (num - v):  # 段尾句子权值的递增调整
            adjust_value = 1 + (v + index - num + 1) * e2 / v
        else:
            adjust_value = 1
        score = score * adjust_value
        scores_second.append((index, score))

    #  根据文章标题进行PR值调整
    scores_third = []
    sim_percents = []
    if not title_words:
        print('Title not entered')
        scores_third = scores_second
    else:
        sim_denominator = sim_function(title_words, title_words)
        if sim_denominator == 0:
            scores_third = scores_second
        else:
            for index in range(num):
                sim_numerator = sim_function(title_words, words[index])
                sim_percents.append(sim_numerator/sim_denominator)
            for index, score in scores_second:
                if w < sim_percents[index] < 1:  # 比值大于w时，调整PR值
                    adjusted_score = score * sim_percents[index] * e3
                    # print(sim_percents[index], sentences[index])
                    # print('old_score:', score, 'new_score:', adjusted_score)
                else:
                    adjusted_score = score
                scores_third.append((index, adjusted_score))
    # for i, j in scores_third:
    #     print(i, j)

    sorted_scores = sorted(scores_third, key=lambda item: item[1], reverse=True)  # 按分数进行降序输出，列表类型
    sorted_sentences = []
    for index, score in sorted_scores:  # 列表元素为(index, score)
        item = AttrDict(index=index, sentence=sentences[index], weight=score)
        sorted_sentences.append(item)  # 列表元素为字典格式
    # print(sorted_sentences)
    return sorted_sentences


if __name__ == '__main__':
    pass
