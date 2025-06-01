# Knowledge-Graph-Enhanced
### 1. 项目说明
- 本项目基于[QASystemOnMedicalKG](https://github.com/liuhuanyong/QASystemOnMedicalKG)进一步开发
- 增加了10类可回答的问题类型
    | 序号 | 问题 |
    |:-:|:-:|
    | 1 | 奶油在得什么病的时候不能吃？ |
    | 2 | 己烯雌酚片的生产商有哪些？ |
    | 3 | 得百日咳的时候能否吃韭菜？ |
    | 4 | 需要忌吃螃蟹的病多还是需要忌吃洋葱的病多？ |
    | 5 | 盐酸环丙沙星片与盐酸阿普林定片哪个的生产商数量更多？ |
    | 6 | 为判断是否得了易感的疾病，高度近视人群需要做哪些检查？ |
    | 7 | 一名7岁儿童需要做哪些预防措施以避免易感的疾病？ |
    | 8 | 高度近视人群应当做哪些预防措施以避免易感的疾病？ |
    | 9 | 妥布霉素地塞米松滴眼液的生产商还会生产哪些药物？ |
    | 10 | 阑尾寄生虫病的并发症属于哪个科室？ |

### 2. Neo4j & 项目运行
- 本项目:
    - 前端: 命令行
    - 后端: 本项目
    - 数据库: `Neo4j`
- 在运行项目之前，需要
    - 下载并安装[Neo4j](https://neo4j.com/download/)
    - 运行数据库:
        - 打开`Neo4j Desktop`
        - 点击`+New`新建项目
        - 点击`Add`添加`Local DBMS`
        - 设置`Name, Password`
        - 点击`Run`运行数据库
        - 修改`build_medicalgraph.py, answer_search.py`中的代码, 连接到数据库:
            ```python
            self.g = Graph("bolt://localhost:xxxx", auth=("neo4j", "xxx"))
            ```
    - 安装依赖: `pip install neo4j pandas jieba py2neo`
    - 运行脚本, 将数据导入进数据库:`python build_medicalgraph.py`
- 启动项目:
    - 运行脚本, 进入命令行交互, 开始问答: `python chatbot_graph.py`:

### 3. 代码修改
#### 3.1 新增一个问题种类，需要修改5处代码:
- `question_classifier.py`:
    - 对问题提取关键词，并进行分类
    - `question_classifier.__init__()`: 增加词条种类
    - `question_classifier.classify()`: 增加问题类型分支
- `question_parser.py`:
    - 根据问题类型和关键词，构造`Cypher`查询语句
	- `question_parser.parser_main()`: 增加问题类型分支
	- `question_parser.sql_transfer()`: 增加问题类型分支 + 构造`Cypher`查询语句
- `answer_search.py`:
    - 根据`Cypher`查询语句查询数据库，获取结果并回答
	- `answer_search.answer_prettify()`: 增加问题类型回答模板
    
#### 3.2 每个问题的思路如下:
1. 什么疾病，不能吃奶油
    找疾病 -不能吃-> 是奶油
    返回疾病
    ```Cypher
    (m:Disease)
    -[r:no_eat]->
    (f:Food)
    where f.name = 奶油
    ```

2. 指定drug的生产商
    这里是Producer drugs_of Drug
    因为不同的生产商可以生成同一种Drug
    ```Cypher
    (m:Drug)
    <-[r:drugs_of]-
    (n:Producer)
    where m.name = “xxx”
    return n.name
    ```

3. 指定疾病，找不能吃的菜，看里面有没有指定菜
    ```Cypher
    (m:Disease)
    -[r:no_eat]->
    (f:Food)
    where m.name = “xxx” and f.name = “xxx”
    return count(*)
    等于0就是没有韭菜，就是可以吃
    ```

4. 找到不能吃指定菜的病，计数，比较结果
    ```Cypher
    (m:Disease)
    -[r:no_eat]->
    (f:Food)
    where f.name = “xxx”
    return count(distinct m.name)
    ```

5. 就是问题2，加上一个计数和比较
    
6. 找病的easy_get包含指定人群，然后找这个病的need check
    返回disease的名字，check的名字

7. 7岁儿童/儿童的易感疾病，找到对应的措施

8. 病的易感人群是高度近视，返回病的名称，病的预防

9. 找这个drug的producers，在找这个

10. 病的并发关系，然后找对应科室
