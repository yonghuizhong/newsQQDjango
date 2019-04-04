import jieba.posseg as pseg
import os
import re

from . import tool


# 得到默认的停止词
def get_default_stop_words():
    stop_words = set()
    d = os.path.dirname(os.path.realpath(__file__))  # 得到模块所在的绝对路径
    file = os.path.join(d, 'stopwords.txt')
    with open(file, 'rt', encoding='UTF-8', errors='ignore') as f:
        for line in f:
            stop_words.add(line.strip())
    return stop_words


# 分词
class WordSegmentation(object):
    def __init__(self):
        self.speech_tags_filter = tool.allow_speech_tags
        self.stop_words = get_default_stop_words()

    # 对一段文本进行分词，返回列表类型
    # lower: 是否将英文单词小写
    # use_stop_words: 是否使用停止词集合
    # use_speech_tags_filter: 是否基于词性进行过滤
    def segment(self, text, lower=True, use_stop_words=True, use_speech_tags_filter=False):
        jieba_result = pseg.cut(text)  # 使用jieba分词
        if use_speech_tags_filter:
            jieba_result = [w for w in jieba_result if w.flag in self.speech_tags_filter]
        else:
            jieba_result = [w for w in jieba_result]

        # 去除特殊符号，如非语素字等，然后取word部分
        word_list = [w.word.strip() for w in jieba_result if w.flag != 'x']
        word_list = [word for word in word_list if len(word) > 0]

        if lower:
            word_list = [word.lower() for word in word_list]

        if use_stop_words:
            word_list = [word.strip() for word in word_list if word.strip() not in self.stop_words]

        return word_list

    # 调用上面的segment()对sentences中的句子进行分词
    # sentences: 列表，元素为句子
    # words: 二维列表，子列表与sentences列表的元素对应，子列表由对应句子的单词构成
    def segment_sentences(self, sentences, lower=True, use_stop_words=True, use_speech_tags_filter=False):
        words = []
        for sentence in sentences:
            words.append(self.segment(text=sentence,
                                      lower=lower,
                                      use_stop_words=use_stop_words,
                                      use_speech_tags_filter=use_speech_tags_filter))
        return words


# 分句
class SentenceSegmentation(object):
    def __init__(self, delimiters=tool.sentence_delimiters):
        self.delimiters = set([item for item in delimiters])

    def segment(self, text):
        regex_pattern = '|'.join(map(re.escape, self.delimiters))
        sentences = re.split(regex_pattern, text)  # 使用正则表达式进行分句
        sentences = [i.strip() for i in sentences if len(i.strip()) > 0]
        return sentences


class Segmentation(object):
    def __init__(self):
        self.ws = WordSegmentation()  # 分词
        self.ss = SentenceSegmentation()  # 分句

    def segment(self, text):
        sentences = self.ss.segment(text)
        words = self.ws.segment_sentences(sentences=sentences,
                                          lower=False,
                                          use_stop_words=True,
                                          use_speech_tags_filter=True)
        return tool.AttrDict(
            sentences=sentences,  # 列表，元素为句子
            words=words  # 二维列表
        )


if __name__ == '__main__':
    pass
