开发中使用的sql 语句（已经过验证）

#选择词库中的词，按照priority ,searchCount 排序，并显示前100记录
select * from wordSelectFeature order by priority desc , searchCount desc group by cluster limit 100;

select * from wordSelectFeature where searchCount < 5000 order by priority desc , searchCount desc limit 100;

<!-- select * from wordSelectFeature where word like '陌陌'; -->
select * from wordSelectFeature where group by cluster order by priority desc , searchCount desc limit 100;

select word from wordSelectFeature where group  

#创建SOM分析结果表
create table SOMwordSelectFeature (word varchar(255),priority int,searchCount int,relevancy float,cluster int);
