#!/usr/bin/env python3
# coding: utf-8
# File: chatbot_graph.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

from question_classifier import *
from question_parser import *
from answer_search import *

'''问答类'''
class ChatBotGraph:
    # 1. 初始化
    # 1.1 创建分类器、解析器和检索器
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    # 2. 回答
    def chat_main(self, sent):
        # 2.1 对问题分类
        answer = '您好，我是小勇医药智能助理，希望可以帮到您。如果没答上来，可联系https://liuhuanyong.github.io/。祝您身体棒棒！'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer
        
        # 2.2 解析，生成查询语句
        res_sql = self.parser.parser_main(res_classify)

        # 2.3 检索器根据查询语句查找答案
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        question = input('用户:')
        answer = handler.chat_main(question)
        print('小勇:', answer)

