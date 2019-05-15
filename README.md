# sneakpeek

[![Build Status](https://travis-ci.com/fterh/sneakpeek.svg?branch=master)](https://travis-ci.com/fterh/sneakpeek)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a196dd3251ec4600b126c9a7712ddbf2)](https://app.codacy.com/app/fterh/sneakpeek?utm_source=github.com&utm_medium=referral&utm_content=fterh/sneakpeek&utm_campaign=Badge_Grade_Dashboard)

A Reddit bot that previews hyperlinks and posts their contents as a comment.
It should **never spam or double-post**, and will skip a comment if it is
too long.

## Site support
* businesstimes.com.sg
* channelnewsasia.com
* channelnewsasia.com (CNAlifestyle)
* mothership.sg  
* ricemedia.co
* straitstimes.com
* tnp.sg
* todayonline.com
* yahoo.com
* zula.sg

## Contributing
PRs are always welcome.

1. Write Handlers to support more websites
2. Improve test coverage
3. Improve documentation

### New version release checklist
1. Create a release branch (e.g. `release-v1.2.3`) from the `develop` branch
2. Bump version numbers in `config.py` to the release branch
3. Update README
4. Possibly commit minor bug fixes to the release branch
5. Merge the release branch into `master` and `develop` 

This project follows this [Git branching workflow](https://nvie.com/posts/a-successful-git-branching-model/).

## Operation
### Before running
The program requires an environmental variable `SUBREDDIT` to be set.
This specifies the subreddit that the bot will monitor.
If it's not set, the default subreddit `/r/all` will be monitored.
At the moment, only 1 subreddit may be specified.

### Running/Testing
All the commands below assume that the virtual environment has been activated
(`pipenv shell`).

* Running: `SUBREDDIT=name python main.py` (or `SUBREDDIT=name nohup python main.py &`)
* Testing: `invoke test`

#### Docker
This application can be built and run as a Docker image.

### General
`main.py` starts the bot and calls `scan(subreddit)` (in `scan.py`), 
which monitors for new submissions in the provided subreddit.

For each new submission, `scan` checks if they qualify for preview 
by calling `qualify` (in `qualify.py`). 

A submission qualifies for preview if it:
1. Is a link
2. Has a Handler for the website

If a submission qualifies, `scan` calls the `handle` method of the Handler 
to generate the raw comment, then `format_comment(comment)` in the 
comments module to generate the final comment in Markdown.

If the final comment in Markdown does not exceed a pre-configured comment length
(`config.COMMENT_LENGTH_LIMIT`), the comment is posted, and the action written 
to the database (through `DatabaseManager`) to prevent double-posting.

Logging is written to standard output, and logging level can be configured in
`config.py`.

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
