# Assignment 2 - Motor Vehicle Theft in San Francisco: Patterns and Prevention

<div style="text-align: center">
<i>Li, Junrui & Fu, Tongzheng<br>
March 30, 2025</i>
</div>

## Introduction

This analysis examines motor vehicle theft in San Francisco using open crime data from the San Francisco Police Department ([available here](https://datasf.org/opendata/)). The dataset covers 2003 to present, showing how vehicle theft patterns have changed across time and locations in the city.

<h5 align="center">Table 1: SF crime data example</h5>
<figure style="text-align: center;">

| Incident Category | Incident Date | Incident Time | Police District | Longitude | Latitude | Location | Source | Year |
|------------------|--------------|--------------|----------------|-----------|----------|----------|--------|------|
| non-criminal | 2003-01-01 | 13:00 | NORTHERN | -122.418468 | 37.787965 | SUTTER ST / LARKIN ST | 03-17 | 2003 |
| other offenses | 2003-01-01 | 22:24 | MISSION | -122.417028 | 37.760366 | 19TH ST / SOUTH VAN NESS AV | 03-17 | 2003 |
| motor vehicle theft | 2003-01-01 | 16:00 | TARAVAL | -122.507539 | 37.753788 | 1700 Block of 48TH AV | 03-17 | 2003 |

</figure>

## The Dramatic Decline: Technology Turns the Tide

Our analysis of the six most common crimes revealed something surprising about motor vehicle theft (Figure 1). While most crime categories followed similar patterns, especially during the 2020 pandemic, vehicle theft showed a unique trend: it dropped by about 50% between 2005 and 2006.

<div style="text-align: center;">
<h5>Fig. 1: SF Monthly Top Crime Trends</h5>
<iframe src="./visualizations/line/crime_trends_2.html" width="100%" height="600px" frameborder="0"></iframe>
<figcaption>Line chart showing monthly-yearly trends of top 6 crime categories from 2003 to 2025. <br>The figure is interactively featuring zoom, selection, and hover information.</figcaption>
</div>

This sharp decline matches the timing of major improvements in car security. Before 2005, vehicle theft was so common that the federal government created the ["Watch Your Car" program](https://www.ojp.gov/pdffiles1/bja/fs000261.pdf). Early technology like EDRs, GPS, and E-ZPass systems had weaknesses that thieves could exploit, as noted in ["How Technology Drives Vehicular Privacy"](https://lorrie.cranor.org/pubs/vehicular-privacy.pdf).

Everything changed in 2005-2006 when car manufacturers widely adopted advanced anti-theft technologies ([source](https://securitytoday.com/articles/2007/10/10/study-car-thefts.aspx)). The impact was immediate and dramatic - theft rates fell sharply and stayed relatively stable for years afterward. This shows how technological innovation can effectively combat specific crime types.

## Persistent Hotspots: The Geography of Vehicle Theft

Our heatmap of vehicle theft locations from 2003-2024 (Figure 2) shows consistent geographic patterns despite the overall reduction in thefts. Note that data for 2025 is excluded as it's incomplete.

<h5 align="center">Fig. 2: SF Motor Vehicle Theft Distribution Map (2003-2023)</h5>
<div class="map-container">
    <iframe src="./visualizations/map/heat_map.html" width="100%" height="500px" frameborder="0" scrolling="no"></iframe>
    <figcaption>Line chart showing monthly-yearly trends of top 6 crime categories from 2003 to 2025. <br>The figure is interactively featuring zoom, selection, and hover information.</figcaption>
</div>
<br>

Two areas consistently stand out as high-risk zones: northeastern San Francisco and the Mission District to its south. These neighborhoods have remained theft hotspots for over 20 years, suggesting deeply rooted patterns in criminal activity.

An interesting shift occurred after 2017: while the overall number of thefts remained stable since 2010, the geographic distribution became more concentrated in specific areas. This concentration peaked during 2020, the first year of the COVID-19 pandemic, when vehicle thefts became highly localized in these traditional hotspots.

This geographic consistency offers valuable insights for prevention:

- Police can focus resources on these high-risk areas
- People should be extra careful when parking in these neighborhoods
- The persistence of these hotspots suggests criminals operate in familiar territories where they've developed expertise

## Time Patterns: When Vehicles Are Most Vulnerable

Our 24-hour analysis (Figure 3) reveals clear patterns in when vehicle thefts occur.

<div style="text-align: center;">
  <h5>Fig. 3: SF Motor Vehicle Theft 24h Distribution Within A Year</h5>
  <iframe src="./visualizations/polarBar/crime_time_distribution.html" width="500px" height="600px" frameborder="0"></iframe>
  <figcaption>Select a specific year (2003-2024) from the select box and hover the mouse <br> 
              over the sector to view the specific incident numbers. The data for 25 years<br>
              are excluded for incompleteness.</figcaption>
</div>

Since 2003, vehicle thefts have consistently peaked between 6 PM and 11 PM, creating a clear evening vulnerability window. During daylight hours, noon emerges as a secondary peak, possibly when vehicle owners are distracted by lunch activities and parking lots experience high turnover.

These time patterns provide practical guidance:

- Evening hours require special vigilance, especially in high-risk areas
- Even busy daytime periods around noon show increased theft risk
- The consistency of these patterns over two decades points to fundamental aspects of criminal opportunity that remain constant despite other social changes



<!-- >
> here is citasd
> |Factor|发现|Source|
|---|---|---|
|收入|区域内贫富差距大|网址|
|种族|种族分布复杂，尤其是Mission District地区|网址|
|交通|路线稠密，交通枢纽，繁华地带|网址|
|Car Ownership|西北部car free率很高，是SF洼地|网址|
> -->


## Contribution


<h5>Table 3: <b>Group 6</b> Contribution matrix</h5>
<figure style="text-align: center;">

|Task|Li, Junrui|Fu, Tongzheng|
|:---|:---:|:---:|
|Diagram - bokeh line chart|🔸||
|Diagram - folium heatmap||🔸|
|Diagram - bohek polar bar chart|🔸||
|Topic mining||🔸|
|Word content||🔸|
|Formatting|🔸||
|Web hosting|🔸||

</figure>
🔸 means mainly implemented by the team member



