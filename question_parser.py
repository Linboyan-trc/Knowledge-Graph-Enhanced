class QuestionPaser:
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    def parser_main(self, res_classify):
        # 1. 获取词条 -> 类型
        # 1. 转为类型 -> [词条]
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)

        # 2. 获取此问题对应的所有问题类型
        question_types = res_classify['question_types']

        # 3. 要执行的sqls查询
        sqls = []

        # 4. 遍历每个问题类型，一个问题类型可以对应多条查询语句
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'disease_symptom':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'symptom_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('symptom'))

            elif question_type == 'disease_cause':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_acompany':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_not_food':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_do_food':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'food_not_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('food'))

            elif question_type == 'food_do_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('food'))

            elif question_type == 'disease_drug':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'drug_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))

            elif question_type == 'disease_check':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'check_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('check'))

            elif question_type == 'disease_prevent':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_lasttime':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_cureway':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_cureprob':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_easyget':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            # 4.2 question2: 查询药品的生产商
            elif question_type == 'drug_producer':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))

            # 4.3 question3: 能否吃某类食物
            elif question_type == 'can_eat_specific_food':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'), entity_dict.get('food'))

            # 4.4 question4: 两种食物比较
            elif question_type == 'disease_kinds_of_food_compare':
                sql = self.sql_transfer(question_type, entity_dict.get('food'))

            # 4.5 question5: 两种药生厂商数量比较
            elif question_type == 'two_drugs_producers_compare':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))

            # 4.6 question6: 指定人群检查
            elif question_type == 'specific_people_check':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            # 4.7 question7: 指定人群避免
            elif question_type == 'specific_people_prevent':
                sql = self.sql_transfer(question_type, None)

            # 4.8 question8: 指定人群避免
            elif question_type == 'specific_people_prevent_2':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            # 4.9 question9: 生成商还会生产
            elif question_type == 'produer_other_drugs':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))

            # 5.10 question10: 并发症属于哪个科室
            elif question_type == 'accompany_department':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        # 5. 返回查询语句
        return sqls

    def sql_transfer(self, question_type, entities, vice_entities=None):
        # 1. 必须要有词条
        if (not entities) and (question_type != 'specific_people_prevent'):
            return []

        # 2. 构造一个问题类型对应的多条查询语句
        sql = []

        # 3. 成因
        # 1. 限定节点类型: MATCH (m:Disease)
        # 2. 指定节点属性: where m.name = '{词条}' 
        # 3. 返回属性: return m.name, m.cause
        if question_type == 'disease_cause':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cause".format(i) for i in entities]

        # 4. 预防
        # 1. 限定节点类型: MATCH (m:Disease) 
        # 2. 指定节点属性: where m.name = '{词条}' 
        # 3. 返回属性: return m.name, m.prevent
        elif question_type == 'disease_prevent':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.prevent".format(i) for i in entities]

        # 查询疾病的持续时间
        elif question_type == 'disease_lasttime':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cure_lasttime".format(i) for i in entities]

        # 查询疾病的治愈概率
        elif question_type == 'disease_cureprob':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cured_prob".format(i) for i in entities]

        # 查询疾病的治疗方式
        elif question_type == 'disease_cureway':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cure_way".format(i) for i in entities]

        # 查询疾病的易发人群
        elif question_type == 'disease_easyget':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.easy_get".format(i) for i in entities]

        # 查询疾病的相关介绍
        elif question_type == 'disease_desc':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.desc".format(i) for i in entities]

        # 6. 症状
        # 1. 限定根节点类型: MATCH (m:Disease)
        # 2. 限定关系类型: -[r:has_symptom]->
        # 3. 限定相邻节点类型: (n:Symptom) 
        # 4. 指定根节点属性: where m.name = '{词条}' 
        # 5. 返回: return m.name, r.name, n.name
        elif question_type == 'disease_symptom':
            sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询症状会导致哪些疾病
        elif question_type == 'symptom_disease':
            sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询疾病的并发症
        elif question_type == 'disease_acompany':
            sql1 = ["MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql2 = ["MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1 + sql2
        # 查询疾病的忌口
        elif question_type == 'disease_not_food':
            sql = ["MATCH (m:Disease)-[r:no_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询疾病建议吃的东西
        elif question_type == 'disease_do_food':
            sql1 = ["MATCH (m:Disease)-[r:do_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql2 = ["MATCH (m:Disease)-[r:recommand_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1 + sql2

        # 已知忌口查疾病
        elif question_type == 'food_not_disease':
            sql = ["MATCH (m:Disease)-[r:no_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 已知推荐查疾病
        elif question_type == 'food_do_disease':
            sql1 = ["MATCH (m:Disease)-[r:do_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql2 = ["MATCH (m:Disease)-[r:recommand_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1 + sql2

        # 查询疾病常用药品－药品别名记得扩充
        elif question_type == 'disease_drug':
            sql1 = ["MATCH (m:Disease)-[r:common_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql2 = ["MATCH (m:Disease)-[r:recommand_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1 + sql2

        # 已知药品查询能够治疗的疾病
        elif question_type == 'drug_disease':
            sql1 = ["MATCH (m:Disease)-[r:common_drug]->(n:Drug) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql2 = ["MATCH (m:Disease)-[r:recommand_drug]->(n:Drug) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1 + sql2
        # 查询疾病应该进行的检查
        elif question_type == 'disease_check':
            sql = ["MATCH (m:Disease)-[r:need_check]->(n:Check) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 已知检查查询疾病
        elif question_type == 'check_disease':
            sql = ["MATCH (m:Disease)-[r:need_check]->(n:Check) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 7.2 question2: 查询药品的生产商
        elif question_type == 'drug_producer':
            sql = ["MATCH (m:Drug)<-[r:drugs_of]-(n:Producer) where m.name = '{0}' return distinct m.name as drug_name, n.name as producer_name".format(i) for i in entities]

        # 7.3 question3: 能否吃某类食物
        elif question_type == 'can_eat_specific_food':
            sql = ["MATCH (m:Disease)-[r:no_eat]->(f:Food) where m.name = '{0}' and f.name = '{1}' return count(*) as cnt".format(i, j)for i in entities for j in vice_entities]

        # 7.4 question4: 两种食物比较
        elif question_type == 'disease_kinds_of_food_compare':
            sql = ["MATCH (m:Disease)-[r:no_eat]->(f:Food) where f.name = '{0}' return f.name as food_name, count(distinct m.name) as cnt".format(i) for i in entities]

        # 7.5 question5: 两种药生厂商数量比较
        elif question_type == 'two_drugs_producers_compare':
            sql = ["MATCH (m:Drug)<-[r:drugs_of]-(n:Producer) where m.name = '{0}' return m.name as drug_name, count(distinct n.name) as cnt".format(i) for i in entities]

        # 7.6 question6: 指定人群检查
        elif question_type == 'specific_people_check':
            sql = ["MATCH (m:Disease)-[r:need_check]->(c:Check) where m.easy_get contains '{0}' return distinct m.name as disease_name, c.name as check_name".format(i) for i in entities]

        # 7.7 question7: 指定人群避免
        elif question_type == 'specific_people_prevent':
            sql = ["MATCH (m:Disease) where m.easy_get contains '7岁儿童' or m.easy_get contains '10岁以下儿童' or m.easy_get contains '-8岁儿童' or m.easy_get contains '至15岁儿童' return distinct m.name as disease_name, m.easy_get as easy_get, m.prevent as prevent_name"]

        # 7.8 question8: 指定人群避免
        elif question_type == 'specific_people_prevent_2':
            sql = ["MATCH (m:Disease) where m.easy_get contains '{0}' return distinct m.name as disease_name, m.prevent as prevent_name".format(i) for i in entities]

        # 7.9 question9: 生成商还会生产
        elif question_type == 'produer_other_drugs':
            sql = ["MATCH (d1:Drug)<-[:drugs_of]-(p:Producer)-[:drugs_of]->(d2:Drug) WHERE d1.name = '{0}' AND d2.name <> '{0}' RETURN DISTINCT d1.name as d1_name, p.name as producer_name, d2.name as d2_name".format(i) for i in entities]

        # 7.10 question10: 并发症属于哪个科室
        elif question_type == 'accompany_department':
            sql = ["MATCH (m:Disease)-[r:acompany_with]->(n:Disease)-[s:belongs_to]->(d:Department) where m.name = '{0}' return distinct m.name as d1_name, n.name as d2_name, d.name as department_name".format(i) for i in entities]

        return sql


if __name__ == '__main__':
    handler = QuestionPaser()
