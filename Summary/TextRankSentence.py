from . import tool
from .Segmentation import Segmentation
from .Segmentation import WordSegmentation


class TextRankSentence(object):
    def __init__(self):
        self.seg = Segmentation()
        self.title_seg = WordSegmentation()
        self.sentences = None
        self.words = None
        self.key_sentences = None
        self.title_words = None

    def analyze(self, text, title):
        self.key_sentences = []
        result = self.seg.segment(text=text)  # 得到分词后的结果
        self.sentences = result.sentences  # 句子列表
        self.words = result.words  # 二维列表
        self.title_words = self.title_seg.segment(text=title, lower=False, use_stop_words=True,
                                                  use_speech_tags_filter=True)  # 对标题进行分词

        # 得到排序后的句子，列表元素为字典格式：包含索引、句子、权重（即PR值）
        self.key_sentences = tool.sort_sentences(sentences=self.sentences,
                                                 words=self.words, title_words=self.title_words)

    # 生成摘要：最重要的num个句子长度>=min_len的句子
    # 将最重要的第一、二句按照句子由低到高的位置拼接形成摘要
    # 如果第一句的句长>= 90，则摘要为第一句
    # 如果拼接的摘要长度 > 160，则摘要为第一句
    def get_key_sentences(self, num=2, min_len=10):
        summary = ''
        result = []
        count = 0
        for i in self.key_sentences:
            if count >= num:
                break
            if len(i['sentence']) >= min_len:
                result.append(i)
                count += 1
        # print('first sentence: ', len(result[0]['sentence']))
        if len(result[0]['sentence']) >= 90:
            summary = result[0]['sentence']
        else:
            sorted_by_index = sorted(result, key=lambda item: item['index'])  # 按照句子的索引进行升序排序
            sentence_by_index = [sentence['sentence'] for sentence in sorted_by_index]
            summary = '。'.join(sentence_by_index)
            if len(summary) > 160:
                summary = result[0]['sentence']
        # print('after: ', len(summary))
        # print('original result: ', result)
        return summary


if __name__ == '__main__':
    pass
