## Changelog
## v1.0.2
* (Try to) post overlength comments as two separate comments

## v1.0.1
* Fix style issues (in code and Markdown)
* Add Codacy badge
* Warn if `SUBREDDIT` environment variable is not set

## v1.0.0
* Add support for Docker
* Set up continuous deployment (Heroku)
* Update README
* Separate changelog into CHANGELOG.md

### v0.8.0-beta
* Fix program stops running after a while (issue #30)
* Implement proper logging
* Clean up and refactor codebase
* Travis CI

### v0.7.0-beta
* Fix random crashes (issue #25)
* Fix README formatting issues
* Clean up code
* Update README developer documentation

### v0.6.0-beta
* Update subreddit monitoring implementation

### v0.5.0-beta
* Fix program crash when exception occurs (issue #13)
* Fix exception in handling Ricemedia links (issue #19)
* Add support for businesstimes.com.sg, tnp.sg, yahoo.com
* Add support for CNAlifestyle

### v0.4.0-beta
* Add Straits Times support

### v0.3.0-beta
* Temporarily remove Straits Times support (until premium article detection feature)
* Fix Todayonline article handling
* Fix Ricemedia article handling
* Update AbstractBaseHandler `handle` method definition
* Add tests

### v0.2.2-beta
* Fix scheduling bug

### v0.2.1-beta
* Remove ricemedia.co from list of supported sites (incompatibility)
* Fix start script to run immediately
* Fix long lines in README

### v0.2.0-beta
* Add scheduling to run every 2 minutes
* Update database module to be compatible with new database table structure
(3 columns)

### v0.1.0-beta
* Minimum viable product
* Supports channelnewsasia.com, mothership.sg, ricemedia.co, straitstimes.com, todayonline.com, zula.sg
