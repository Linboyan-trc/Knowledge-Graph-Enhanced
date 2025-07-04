import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        # 1. disease + symptom + check
        # 2. food + drug + producer + department
        # 3. deny
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.disease_path = os.path.join(cur_dir, 'dict/disease.txt')
        self.symptom_path = os.path.join(cur_dir, 'dict/symptom.txt')
        self.check_path = os.path.join(cur_dir, 'dict/check.txt')
        self.food_path = os.path.join(cur_dir, 'dict/food.txt')
        self.drug_path = os.path.join(cur_dir, 'dict/drug.txt')
        self.producer_path = os.path.join(cur_dir, 'dict/producer.txt')
        self.department_path = os.path.join(cur_dir, 'dict/department.txt')
        self.deny_path = os.path.join(cur_dir, 'dict/deny.txt')

        # 2. 词条列表
        # 2.1 region_words具有所有词条
        self.disease_wds= [i.strip() for i in open(self.disease_path) if i.strip()]
        self.symptom_wds= [i.strip() for i in open(self.symptom_path) if i.strip()]
        self.check_wds= [i.strip() for i in open(self.check_path) if i.strip()]
        self.food_wds= [i.strip() for i in open(self.food_path) if i.strip()]
        self.drug_wds= [i.strip() for i in open(self.drug_path) if i.strip()]
        self.producer_wds= [i.strip() for i in open(self.producer_path) if i.strip()]
        self.department_wds= [i.strip() for i in open(self.department_path) if i.strip()]
        self.deny_words = [i.strip() for i in open(self.deny_path) if i.strip()]
        self.region_words = set(self.department_wds + self.disease_wds + self.check_wds + self.drug_wds + self.food_wds + self.producer_wds + self.symptom_wds)
        
        # 3. 构建词典: 词 -> 类型
        # 3. 构造领域actree: 从问句中找关键词
        self.wdtype_dict = self.build_wdtype_dict()
        self.region_tree = self.build_actree(list(self.region_words))
        
        # 4. 问句疑问词
        # 4.1 disease attribution
        self.cause_qwds = ['原因','成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致', '会造成']
        self.prevent_qwds = ['预防', '防范', '抵制', '抵御', '防止','躲避','逃避','避开','免得','逃开','避开','避掉','躲开','躲掉','绕开','怎样才能不', '怎么才能不', '咋样才能不','咋才能不', '如何才能不','怎样才不', '怎么才不', '咋样才不','咋才不', '如何才不','怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不','怎样才可不', '怎么才可不', '咋样才可不', '咋才可不', '如何可不']
        self.easyget_qwds = ['易感人群', '容易感染', '易发人群', '什么人', '哪些人', '感染', '染上', '得上']
        self.lasttime_qwds = ['周期', '多久', '多长时间', '多少时间', '几天', '几年', '多少天', '多少小时', '几个小时', '多少年']
        self.cureprob_qwds = ['多大概率能治好', '多大几率能治好', '治好希望大么', '几率', '几成', '比例', '可能性', '能治', '可治', '可以治', '可以医']
        self.cureway_qwds = ['怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治', '医治方式', '疗法', '咋治', '怎么办', '咋办', '咋治']

        # 4.2 kinds
        self.symptom_qwds = ['症状', '表征', '现象', '症候', '表现']
        self.check_qwds = ['检查', '检查项目', '查出', '检查', '测出', '试出']
        self.food_qwds = ['饮食', '饮用', '吃', '食', '伙食', '膳食', '喝', '菜' ,'忌口', '补品', '保健品', '食谱', '菜谱', '食用', '食物','补品']
        self.drug_qwds = ['药', '药品', '用药', '胶囊', '口服液', '炎片']
        
        # 4.3 addition
        self.acompany_qwds = ['并发症', '并发', '一起发生', '一并发生', '一起出现', '一并出现', '一同发生', '一同出现', '伴随发生', '伴随', '共现']
        self.belong_qwds = ['属于什么科', '属于', '什么科', '科室']
        self.cure_qwds = ['治疗什么', '治啥', '治疗啥', '医治啥', '治愈啥', '主治啥', '主治什么', '有什么用', '有何用', '用处', '用途','有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚', '需要', '要']
        
        # 4.4 
        # 4.4.2 question2: 新增生产商相关的问题词
        self.producer_qwds = ['生产商', '生产企业', '生产厂家', '药企', '制造商', '产商', '厂商', '哪里产的', '谁生产的', '哪个公司']
        # 4.4.3 question3: 新增能否吃某类食物
        self.can_eat_specific_food = ['能否吃']
        # 4.4.4 question4: 两种食物比较
        self.disease_kinds_of_food_compare = ['还是']
        # 4.4.5 question5: 两种药生厂商数量比较
        self.two_drugs_producers_compare = ['哪个的生产商数量更多']
        # 4.4.6 question6: 指定人群检查
        self.specific_people_check = ['是否得了易感的疾病']
        # 4.4.7 question7: 指定人群避免
        self.specific_people_prevent = ['儿童需要做哪些预防措施以避免']
        # 4.4.8 question8: 指定人群避免
        self.specific_people_prevent_2 = ['高度近视人群应当做哪些预防措施以避免']
        # 4.4.9 question9: 生成商还会生产
        self.produer_other_drugs = ['生产商还会生产']
        # 4.4.10 question10: 并发症属于哪个科室
        self.accompany_department = ['并发症属于哪个科室']

        # 5. 返回
        print('model init finished ......')
        return

    def classify(self, question):
        # 1. 获取{词条 -> 类型}，一定能获取到词条
        data = {}
        medical_dict = self.check_medical(question)
        if (not medical_dict) and ('预防措施以避免' not in question):
            return {}
        
        # 2. {词条 -> 类型}注入
        data['args'] = medical_dict

        # 3. 获取词条对应的类型
        types = []
        for type_ in medical_dict.values():
            types += type_

        # 4. 设置问题类型
        question_type = 'others'
        question_types = []

        # 5. 分支判断，得到此问题所属于的所有问题类型
        # 症状
        if self.check_words(self.symptom_qwds, question) and ('disease' in types):
            question_type = 'disease_symptom'
            question_types.append(question_type)

        if self.check_words(self.symptom_qwds, question) and ('symptom' in types):
            question_type = 'symptom_disease'
            question_types.append(question_type)

        # 原因
        if self.check_words(self.cause_qwds, question) and ('disease' in types):
            question_type = 'disease_cause'
            question_types.append(question_type)

        # 并发症
        if self.check_words(self.acompany_qwds, question) and ('disease' in types):
            question_type = 'disease_acompany'
            question_types.append(question_type)

        # 推荐食品
        if self.check_words(self.food_qwds, question) and 'disease' in types:
            deny_status = self.check_words(self.deny_words, question)
            if deny_status:
                question_type = 'disease_not_food'
            else:
                question_type = 'disease_do_food'
            question_types.append(question_type)

        #已知食物找疾病
        if self.check_words(self.food_qwds+self.cure_qwds, question) and 'food' in types:
            deny_status = self.check_words(self.deny_words, question)
            if deny_status:
                question_type = 'food_not_disease'
            else:
                question_type = 'food_do_disease'
            question_types.append(question_type)

        # 推荐药品
        if self.check_words(self.drug_qwds, question) and 'disease' in types:
            question_type = 'disease_drug'
            question_types.append(question_type)

        # 药品治啥病
        if self.check_words(self.cure_qwds, question) and 'drug' in types:
            question_type = 'drug_disease'
            question_types.append(question_type)

        # 疾病接受检查项目
        if self.check_words(self.check_qwds, question) and 'disease' in types:
            question_type = 'disease_check'
            question_types.append(question_type)

        # 已知检查项目查相应疾病
        if self.check_words(self.check_qwds+self.cure_qwds, question) and 'check' in types:
            question_type = 'check_disease'
            question_types.append(question_type)

        #　症状防御
        if self.check_words(self.prevent_qwds, question) and 'disease' in types:
            question_type = 'disease_prevent'
            question_types.append(question_type)

        # 疾病医疗周期
        if self.check_words(self.lasttime_qwds, question) and 'disease' in types:
            question_type = 'disease_lasttime'
            question_types.append(question_type)

        # 疾病治疗方式
        if self.check_words(self.cureway_qwds, question) and 'disease' in types:
            question_type = 'disease_cureway'
            question_types.append(question_type)

        # 疾病治愈可能性
        if self.check_words(self.cureprob_qwds, question) and 'disease' in types:
            question_type = 'disease_cureprob'
            question_types.append(question_type)

        # 疾病易感染人群
        if self.check_words(self.easyget_qwds, question) and 'disease' in types :
            question_type = 'disease_easyget'
            question_types.append(question_type)

        # 5.2 question2: 新增查询药品的生产商
        if self.check_words(self.producer_qwds, question) and 'drug' in types:
            question_type = 'drug_producer'
            question_types.append(question_type)

        # 5.3 question3: 能否吃某类食物，直接赋值question_types以清除之前的question_types
        if self.check_words(self.can_eat_specific_food, question) and 'food' in types and 'disease' in types:
            question_type = 'can_eat_specific_food'
            question_types = [question_type]

        # 5.4 question4: 两种食物比较
        if self.check_words(self.disease_kinds_of_food_compare, question) and 'food' in types:
            question_type = 'disease_kinds_of_food_compare'
            question_types = [question_type]

        # 5.5 question5: 两种药生厂商数量比较
        if self.check_words(self.two_drugs_producers_compare, question) and 'drug' in types:
            question_type = 'two_drugs_producers_compare'
            question_types = [question_type]

        # 5.6 question6: 指定人群检查
        if self.check_words(self.specific_people_check, question) and 'disease' in types:
            question_type = 'specific_people_check'
            question_types = [question_type]

        # 5.7 question7: 指定人群避免
        if self.check_words(self.specific_people_prevent, question):
            question_type = 'specific_people_prevent'
            question_types = [question_type]

        # 5.8 question8: 指定人群避免
        if self.check_words(self.specific_people_prevent_2, question) and 'disease' in types:
            question_type = 'specific_people_prevent_2'
            question_types = [question_type]

        # 5.9 question9: 生成商还会生产
        if self.check_words(self.produer_other_drugs, question) and 'drug' in types:
            question_type = 'produer_other_drugs'
            question_types = [question_type]

        # 5.10 question10: 并发症属于哪个科室
        if self.check_words(self.accompany_department, question) and 'disease' in types:
            question_type = 'accompany_department'
            question_types = [question_type]

        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'disease' in types:
            question_types = ['disease_desc']

        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'symptom' in types:
            question_types = ['symptom_disease']

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data

    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.disease_wds:
                wd_dict[wd].append('disease')
            if wd in self.department_wds:
                wd_dict[wd].append('department')
            if wd in self.check_wds:
                wd_dict[wd].append('check')
            if wd in self.drug_wds:
                wd_dict[wd].append('drug')
            if wd in self.food_wds:
                wd_dict[wd].append('food')
            if wd in self.symptom_wds:
                wd_dict[wd].append('symptom')
            if wd in self.producer_wds:
                wd_dict[wd].append('producer')
        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''
    def check_medical(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)