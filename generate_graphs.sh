#!/bin/sh


sixteen_files="2016-01.bz2 2016-02.bz2 2016-03.bz2 2016-04.bz2 2016-05.bz2 2016-06.bz2 2016-07.bz2 2016-08.bz2 2016-09.bz2 2016-10.bz2 2016-11.bz2 2016-12.bz2" 

seventeen_files="2017-01.bz2 2017-02.bz2 2017-03.bz2 2017-04.bz2 2017-05.bz2 2017-06.bz2 2017-07.bz2 2017-08.bz2 2017-09.bz2 2017-10.bz2 2017-11.bz2 2017-12.xz"

eighteen_files="2018-01.xz 2018-02.xz 2018-03.xz 2018-04.xz 2018-05.xz 2018-06.xz"

for i in $sixteen_files; do
	echo ${i}
	python generate_bipartite_graph.py ${i}
	python generate_community_relation_graph.py ${i}
done

for i in $seventeen_files; do
	echo ${i}
	python generate_bipartite_graph.py ${i}
	python generate_community_relation_graph.py ${i}
done

for i in $eighteen_files; do
	echo ${i}
	python generate_bipartite_graph.py ${i}
	python generate_community_relation_graph.py ${i}
done

