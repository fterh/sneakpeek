# sneakpeek

[![Build Status](https://travis-ci.com/fterh/sneakpeek.svg?branch=master)](https://travis-ci.com/fterh/sneakpeek)

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

## Running and deploying
All the commands below assume you have already activated the
virtual environment (`pipenv shell`). Alternatively, prepend `pipenv run` to
the commands.

### Development
`python main.py`

### Testing
`invoke test`

### Production
`ENV=prod python main.py` or `ENV=prod nohup python main.py &`
