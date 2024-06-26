<p align="center">
  <img src="./static/es2-white.png" />
</p>

Elasticsearch hosts are easily misconfigured. Although mostly used for storing logs and monitoring data, organizations use it also as a databse-type instance for any sort of data (it is a database after all). Elastic(search²) is an Elasticsearch host aggregator from various search engines for discovering leaks.

Elastic(search²) is a small tool for discovering Elasticsearch hosts from various search engines (Shodan so far) based on the country they are hosted in.

## Why
I like exploring the Internet and finding leaks (and then to report them to their organizations). This utility started as a Bash script I wrote for doing basically the same thing: finding out hosts from Shodan and updating my database so that I don't get duplicates the next time I search for hosts in the same country. I wanted to get back a bit into proper coding so I decided to create a Flask application with the same use (and a prettier UI).

Not going to lie, a good percentage of this project was initially written by AI. But now only about 15-20% of it is AI-generated.

## Features and Info
- SQLite3 database for keeping track of already-reviewed hosts.
- Export results to JSON.
- AI generated logo (I'm still hyped about it).
- It currently looks only for hosts that contain GB of data. But this can of course be tweaked.

## Usage
1. Rename `.env.1` to `.env`
2. Put your Shodan API in `.env`
3. Rename `database-rename.db` to `database.db`

### If running locally
4. `flask --app elasticApp run`

### If building on Docker
4. `docker build -t elasticsearch2 .`
5. `docker run -v ./database.db:/app/database.db --network host -p 5000:5000 elasticsearch2:latest`

Then visit `http://127.0.0.1:5000`.

## Keywords
In `keywords.txt` you can put the words you want Elastic(search²) to identify in hosts' index names, one keyword per line.

In `indices_keywords.txt` you can put the words you want Elastic(search²) to identify inside each index of the given host, one keyword per line.

![indices_keywords screenshot](./static/indices_keywords.png)

## TODO
Things/ideas to develop. Feel free to create a Pull Request!

- [ ] (Properly) Export to JSON
	- For each search, each session (stuck at the first search of each session)
- [x] Add (very simple) content analysis based on keywords ("users", "orders", "invoices" etc.)
- [ ] Add more search engines (Censys)
- [x] Add a "cleanup" function
	- To remove hosts from the database that are now unreachable
- [x] Add multithreading
- [ ] Debug logs export
- [x] Dockerize

### Sponsored by:

[![Bitcrack Cyber Security](bc.png)](https://www.bitcrack.net/)
