# pubmed_spider: A spider program for downloading text from pubmed

## Discription

One day, I wanted to add my article collection from Zotero to my LLM knowledge base, but I found it cumbersome to retrieve all PDF files from Zotero.

How can we add these articles to an LLM knowledge base? Since Zotero can export all articles as a CSV file, we can parse this file to extract article titles and then retrieve the corresponding content from PubMed using these titles.

This was the original motivation for creating this project.

## Requirement

You need python3 and following libraries:

-  pandas
-  numpy
-  requests
-  BeautifulSoup

## Usage

```
pubmed_spider.py <zotero_export_csv> [output_dir]
```

+ The first parameter should be your article collection file (CSV format), which must contain a "Title" column with article titles.
+ The second parameter is optional and specifies the output directory path. The default path is `saves`.

## Example

Suppose we have a article collection file named `population genetic.csv` , which contains following information:

| Publication Year | Author | Title | Publication Title | DOI | Date |
|------------------|--------|-------|-------------------|-----|------|
| 2019 | "Speidel, Leo; Forest, Marie; Shi, Sinan; Myers, Simon R." | A method for genome-wide genealogy estimation for thousands of samples | Nature Genetics | 10.1038/s41588-019-0484-x | Sep-19 |
| 2021 | "Song, Weichen; Shi, Yueqi; Wang, Weidi; Pan, Weihao; Qian, Wei; Yu, Shunying; Zhao, Min; Lin, Guan Ning" | A selection pressure landscape for 870 human polygenic traits | Nature Human Behaviour | 10.1038/s41562-021-01231-4 | Dec-21 |
| 2016 | "Field, Yair; Boyle, Evan A; Telis, Natalie; Gao, Ziyue; Gaulton, Kyle J; Golan, David; Yengo, Loic; Rocheleau, Ghislain; Froguel, Philippe; McCarthy, Mark I; Pritchard, Jonathan K" | Detection of human adaptation during the past 2000 years | Science |  | 2016/11/11 |
| 2023 | "Luo, Huaxia; Zhang, Peng; Zhang, Wanyu; Zheng, Yu; Hao, Di; Shi, Yirong; Niu, Yiwei; Song, Tingrui; Li, Yanyan; Zhao, Shilei; Chen, Hua; Xu, Tao; He, Shunmin" | Recent positive selection signatures reveal phenotypic evolution in the Han Chinese population | Science Bulletin | 10.1016/j.scib.2023.08.027 | Aug-23 |

The file content is:

```
Publication Year,Author,Title,Publication Title,DOI,Date
2019,"Speidel, Leo; Forest, Marie; Shi, Sinan; Myers, Simon R.",A method for genome-wide genealogy estimation for thousands of samples,Nature Genetics,10.1038/s41588-019-0484-x,Sep-19
2021,"Song, Weichen; Shi, Yueqi; Wang, Weidi; Pan, Weihao; Qian, Wei; Yu, Shunying; Zhao, Min; Lin, Guan Ning",A selection pressure landscape for 870 human polygenic traits,Nature Human Behaviour,10.1038/s41562-021-01231-4,Dec-21
2016,"Field, Yair; Boyle, Evan A; Telis, Natalie; Gao, Ziyue; Gaulton, Kyle J; Golan, David; Yengo, Loic; Rocheleau, Ghislain; Froguel, Philippe; McCarthy, Mark I; Pritchard, Jonathan K",Detection of human adaptation during the past 2000 years,Science,,2016/11/11
2023,"Luo, Huaxia; Zhang, Peng; Zhang, Wanyu; Zheng, Yu; Hao, Di; Shi, Yirong; Niu, Yiwei; Song, Tingrui; Li, Yanyan; Zhao, Shilei; Chen, Hua; Xu, Tao; He, Shunmin",Recent positive selection signatures reveal phenotypic evolution in the Han Chinese population,Science Bulletin,10.1016/j.scib.2023.08.027,Aug-23
```

We can retrieve all articles' content by running:


```
$> python pubmed_spider.py "population genetic.csv" "population genetic"
input  csv file = population genetic.csv
output dir path = population genetic
[0/4]Processing article: `A method for genome-wide genealogy estimation for thousands of samples`
writing file: autosave-31477933.txt
writing file: autosave-28739658.txt
writing file: autosave-18060068.txt
writing file: autosave-35846115.txt
writing file: autosave-39589398.txt
writing file: autosave-38242694.txt
writing file: autosave-20485442.txt
[1/4]Processing article: `A selection pressure landscape for 870 human polygenic traits`
writing file: autosave-34782732.txt
[2/4]Processing article: `Detection of human adaptation during the past 2000 years`
writing file: autosave-27738015.txt
[3/4]Processing article: `Recent positive selection signatures reveal phenotypic evolution in the Han Chinese population`
writing file: autosave-37661541.txt
$> ls "population genetic"
autosave-18060068.txt  autosave-27738015.txt  autosave-31477933.txt  autosave-35846115.txt  autosave-38242694.txt
autosave-20485442.txt  autosave-28739658.txt  autosave-34782732.txt  autosave-37661541.txt  autosave-39589398.txt
```

Note: Due to fuzzy matching during PubMed queries, some articles may map to multiple PMIDs, resulting in extra downloaded files. 
However, since our goal is to collect all relevant article text for the LLM knowledge base, this isn't a major concern.






