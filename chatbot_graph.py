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
        if not res_sql:
            return answer

        # 2.3 检索器根据查询语句查找答案
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            # 针对食物和疾病的特殊处理
            if '能否吃' in sent or '可以吃' in sent:
                disease = None
                food = None
                
                # 从分类结果中提取疾病和食物
                if 'args' in res_classify:
                    for entity, types in res_classify['args'].items():
                        if 'disease' in types:
                            disease = entity
                        elif 'food' in types:
                            food = entity
                
                if disease and food:
                    return "对于{0}患者是否可以食用{1}，建议您咨询医生意见，因为这可能与病情具体情况有关。".format(disease, food)
            
            return answer
        else:
            return '\n'.join(final_answers)

if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        question = input('用户:')
        answer = handler.chat_main(question)
        print('小勇:', answer)

