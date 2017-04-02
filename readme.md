#docker run -v /home/nate/dropbox/Classes/FundDataScience_COMP8150/assignments/hw4:/data -it neighdough/spark /bin/bash
#PYSPARK_DRIVER_PYTHON=ipython ./bin/pyspark
#docker run -P --net=host --add-host=moby:127.0.0.1 -it neighdough/spark /bin/bash

text = sc.textFile('/data/data/sample-text.txt').map(lambda line: re.sub(exp, '', line).split(' ')).zipWithIndex()
text.flatMap(lambda x: [[i, x[1]] for i in x[0]]).collect()
