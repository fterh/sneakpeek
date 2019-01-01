# sneakpeek
A Reddit bot that previews hyperlinks and posts their contents as a comment.
It should **never spam or double-post**, and will skip a comment if it is too long.

## Site support
* channelnewsasia.com
* mothership.sg  
* ricemedia.co
* straitstimes.com
* todayonline.com
* zula.sg

## Contributing
1. Improve this README
2. Write documentation
3. Write Handlers to support more websites
4. Write tests

## How it works
### General
`main.py` starts the bot and calls `scan(subreddit)` (in `scan.py`), 
which scans for submissions in the provided subreddit.

`scan` gets a pre-configured number (`config.LIMIT`) of the latest submissions 
and checks if they qualify for preview by calling `qualify` (in `qualify.py`). 

A submission qualifies for preview if it:
1. Is a link
2. Has not been encountered by the bot previously
3. Has a Handler for the website

If a submission qualifies, `scan` calls the `handle` method of the Handler 
to generate the raw comment, then `format_comment(comment)` in the 
comments module to generate the final comment in Markdown.

If the final comment in Markdown does not exceed a pre-configured comment length (`config.COMMENT_LENGTH_LIMIT`), the comment is posted, and the action written 
to the database (through `DatabaseManager`) to prevent double-posting.

### Handlers
`handler.py` contains a HandlerManager that checks if a website has a Handler. 

A Handler is a class with a `@classmethod handle(cls, url)` that accepts a URL 
and returns a Comment. All Handlers must inherit from `AbstractBaseHandler`. 

The Handler can be part of a module or package, and have as many supporting 
sub-modules or sub-packages as necessary.

### Comments
The comments module (in `comment.py`) exports the Comment class, 
which all Handlers must return. A Comment class requires a `title` and `body`, 
and accepts a `byline` and `attribution` (which are optional). 

### Database
|submission_id|action|notes
|--|--|--
|text|text|text

A list of valid actions is provided by `DatabaseActionEnum` in the 
`database` module: `ERROR`, `SKIP`, and `SUCCESS`.

## Changelog
### v0.2.1-beta
* Remove ricemedia.co from list of supported sites (incompatibility)
* Fix start script to run immediately
* Fix long lines in README

#### v0.2.0-beta
* Add scheduling to run every 2 minutes
* Update database module to be compatible with new database table structure
(3 columns)

#### v0.1.0-beta
* Minimum viable product
* Supports channelnewsasia.com, mothership.sg, ricemedia.co, straitstimes.com, 
todayonline.com, zula.sg