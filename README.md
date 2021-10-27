<p align="center">
<img alt="Movie Score ai" src="assets/icon.png" width="350">
</p>
 
<p align="center">
<img alt="Licence" src=https://img.shields.io/github/license/lironbdolah/moviescoreai>
 <img alt="Issues" src=https://img.shields.io/github/issues/lironbdolah/moviescoreai>
 <img alt="last commit" src=https://img.shields.io/github/last-commit/lironbdolah/moviescoreai>

</p>

This RNN based model predicts movies popularity based on users reviews and scores on Imdb.com and creates an [HTML file](http://htmlpreview.github.io/?https://github.com/lironbdolah/moviescoreai/blob/main/runs/test.html) with relevant statistics. <br />



**Features:**

- Classifies user's reviews with an RNN model.
- Trained on 40,000 movie reviews that were scraped from [imdb.com](https://www.imdb.com).
- Exports an HTML file with statistics about recently published movies.
- Generates a review for the top movie of the week.
- Updates weekly according to [Imdb: movies in theaters](https://www.imdb.com/movies-in-theaters/?ref_=nv_mv_inth).
- Can be applied on custom movie lists 


## Requierments:
- tensorflow 2.0+
- nltk

## Quick start:
Run this command to get the summary in an HTML file:

```shell
python src/moviescoreai.py --name <name for the HTML file>  --output <output path> --start <Optional, if you want to file to open by defult>
--movies-url <url for your movies list >
```

## Example:

Here's an example for summarizing a [custom made_list on Imdb:](https://www.imdb.com/list/ls089653199/?ref_=otl_3)

```shell
python src/moviescoreai.py --name example  --output runs/example --start True
--movies-url https://www.imdb.com/list/ls089653199/?ref_=otl_3
```
That's it!
After running this command, the html file will be saved to the output path.
[Example_result:](http://htmlpreview.github.io/?https://github.com/lironbdolah/moviescoreai/blob/main/runs/test.html)



