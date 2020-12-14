# flask-app
main.py creates a website using the flask application. The website has four pages: index.html,
browse.html, api.html, and donate.html. The home page routes to index.html, which contains links
to the other pages. The browse.html page provides an html table for main.csv. There is a buttom on index.html
that allows the user to add their email to an email list. Next we run an A/B test
by creating two slightly differentiated versions of index.html to see which version promotes more
visits to donate.html. The first ten homepage visits alternate between version A and version B, and
donate.html keeps track of which homepage the link was accessed from. After ten visits, the best homepage
is chosen. We include an API that returns json information sourced from the csv used. the api.html page
includes links to different api sources. The url ending policecols.json returns a dictionary representation of
the column information for the csv. The url ending police.json allows the user to specify a gender filter for the columns returned.
