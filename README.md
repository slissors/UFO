# UFO
A study on different factors that could effect UFO sightings in the USA.
It is split into two main categories, media and geographical location.
Media explores the relationships between sci-fi films daily gross and UFO sightings from 2009-2022 (ongoing).
Geographical location will explore how the distance from Weather Balloon sites in the USA effect UFO sightings (ongoing).
A report will be made for each factor explored.




#Current findings


![image](https://github.com/slissors/UFO/assets/93544397/a02d2218-7d60-48e4-b7a7-572dd8d4204c)
<video src="https://www.youtube.com/watch?v=T69yo1YTFVw" width="300" />


Null Hypothesis: Daily gross of sci-fi films has no effect on UFO sightings from 2009-2022
Alternative hypothesis: Daily gross of sci-fi films has a positive effect on UFO sightings from 2009-2022




**DATA COLLECTION**

UFO Sightings Data:
One of the most important dataset were the UFO sightings. This data was gathered from a cleaned .csv file from Timothy Renner [https://data.world/timothyrenner/ufo-sightings/workspace/file?filename=nuforc_reports.csv], which was originally published from the National UFO reporting centre [https://nuforc.org/]

List of Top Grossing Films:
To compile a list of the top-grossing science fiction films featuring extraterrestrial life, IMDb’s website was utilised as it provides information on the box office gross of various films. 
[https://www.imdb.com/search/title/?title_type=feature&genres=scifi&sort=boxoffice_gross_us]

Daily Film Gross Data:
To gather daily domestic box office gross data for the top 10 sci-fi films identified above, I designed a Python web scraper using BeautifulSoup to collect the date and daily domestic gross figures from the Box Office Mojo website and save each movie as individual .csv files.
 [https://www.boxofficemojo.com/?ref_=bo_nb_rl_mojologo. ]
The website does not prohibit automated data retrieval, and no sensitive or proprietary data was accessed. 

**DATA ANALYSIS**
Used a cross-correlation function, from numpy, to calculate the cross-correlation coefficient for the time lag between daily gross and daily UFO sightings.
[Working to fix the code]
This is what I currently have plotted, it is showing a positive relationship with each film.
![image](https://github.com/slissors/UFO/assets/93544397/de7ced9d-40e4-4cd5-a922-44fbd4fab764)

