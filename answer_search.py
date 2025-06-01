from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        self.g = Graph("bolt://localhost:7687", auth=("neo4j", "1584340372"))
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls):
        # 1. 最终回答
        final_answers = []

        # 2. 遍历每个问题类型对应的多条查询语句
        for sql_ in sqls:
            # 2.1 获取当前问题类型
            question_type = sql_['question_type']

            # 2.2 获取当前对应的多条查询语句
            queries = sql_['sql']

            # 2.3 存储查询结果
            answers = []

            # 2.4 遍历每个查询语句
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress

            # 2.5 根据问题类型，和多条查询语句的多个查询结果，组成当前问题类型的最终回答
            final_answer = self.answer_prettify(question_type, answers)

            # 2.6 当前问题类型回答不为空，加入最终回答列表
            if final_answer:
                final_answers.append(final_answer)

        # 3. 返回最终回答列表
        return final_answers

    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'disease_symptom':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'symptom_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '症状{0}可能染上的疾病有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cause':
            desc = [i['m.cause'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}可能的成因有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_prevent':
            desc = [i['m.prevent'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的预防措施包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_lasttime':
            desc = [i['m.cure_lasttime'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}治疗可能持续的周期为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cureway':
            desc = [';'.join(i['m.cure_way']) for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}可以尝试如下治疗：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cureprob':
            desc = [i['m.cured_prob'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}治愈的概率为（仅供参考）：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_easyget':
            desc = [i['m.easy_get'] for i in answers]
            subject = answers[0]['m.name']

            final_answer = '{0}的易感人群包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_desc':
            desc = [i['m.desc'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0},熟悉一下：{1}'.format(subject,  '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_acompany':
            desc1 = [i['n.name'] for i in answers]
            desc2 = [i['m.name'] for i in answers]
            subject = answers[0]['m.name']
            desc = [i for i in desc1 + desc2 if i != subject]
            final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_not_food':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}忌食的食物包括有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_do_food':
            do_desc = [i['n.name'] for i in answers if i['r.name'] == '宜吃']
            recommand_desc = [i['n.name'] for i in answers if i['r.name'] == '推荐食谱']
            subject = answers[0]['m.name']
            final_answer = '{0}宜食的食物包括有：{1}\n推荐食谱包括有：{2}'.format(subject, ';'.join(list(set(do_desc))[:self.num_limit]), ';'.join(list(set(recommand_desc))[:self.num_limit]))

        elif question_type == 'food_not_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '患有{0}的人最好不要吃{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

        elif question_type == 'food_do_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '患有{0}的人建议多试试{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

        elif question_type == 'disease_drug':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}通常的使用的药品包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'drug_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '{0}主治的疾病有{1},可以试试'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_check':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}通常可以通过以下方式检查出来：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'check_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '通常可以通过{0}检查出来的疾病有{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        # 1.2 question2: 查询药品的生产商
        elif question_type == 'drug_producer':
            # 1.2.1 获取所有生产商名称
            if not answers:
                return '未找到该药品的生产商信息'
            producers = [i['producer_name'] for i in answers]  

            # 1.2.2 获取药品名称
            drug = answers[0]['drug_name']  

            # 1.2.3 返回单个问题类型的回答
            final_answer = '{0}的生产商包括：{1}'.format(drug, '；'.join(list(set(producers))[:self.num_limit]))

        # 1.3 question3: 能否吃某类食物
        elif question_type == 'can_eat_specific_food':
            if answers[0]['cnt'] == 0:
                final_answer = "可以吃"
            else:
                final_answer = "不可以吃"

        # 1.4 question4: 两种食物比较
        elif question_type == 'disease_kinds_of_food_compare':
            food1 = answers[0]['food_name']
            cnt1 = answers[0]['cnt']
            food2 = answers[1]['food_name']
            cnt2 = answers[1]['cnt']
            if cnt1 < cnt2:
                final_answer = "需要忌吃{0}的病有{1}种，需要忌吃{2}的病有{3}种，所以需要忌吃{2}的病多".format(food1, cnt1, food2, cnt2)
            elif cnt1 == cnt2:
                final_answer = "需要忌吃{0}的病有{1}种，需要忌吃{2}的病有{3}种，两者一样多".format(food1, cnt1, food2, cnt2)
            else:
                final_answer = "需要忌吃{0}的病有{1}种，需要忌吃{2}的病有{3}种，所以需要忌吃{0}的病多".format(food1, cnt1, food2, cnt2)

        # 1.5 question5: 两种药生厂商数量比较
        elif question_type == 'two_drugs_producers_compare':
            drug1 =  answers[0]['drug_name']
            cnt1 = answers[0]['cnt']
            drug2 =  answers[1]['drug_name']
            cnt2 = answers[1]['cnt']
            if cnt1 < cnt2:
                final_answer = "{0}的生产商数量为{1}家，{2}的生产商数量为{3}家，所以{2}的生产商数量更多".format(drug1, cnt1, drug2, cnt2)
            elif cnt1 == cnt2:
                final_answer = "{0}的生产商数量为{1}家，{2}的生产商数量为{3}家，两者一样多".format(drug1, cnt1, drug2, cnt2)
            else:
                final_answer = "{0}的生产商数量为{1}家，{2}的生产商数量为{3}家，所以{0}的生产商数量更多".format(drug1, cnt1, drug2, cnt2)

        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()