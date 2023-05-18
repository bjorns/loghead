# Introduction to loghead

loghead is a new logging package for Python. Its primary goals are beauty and developer Joy.


## Frequently Asked Questions

### How does loghead promote developer Joy?

The primary way loghead tries to make your life easier is by clear communication
and reducing unexpected behavior:

* Every object in loghead can be printed to stderr for easy debugging in case the
log is not doing what you want
* All logging configuration can be dynamically updated, you do not need to
restart or redeploy your app to   change a log level, or change logging target.
* When something is wrong, loghead will always tell you what it doesnt recognize
and to the best of its ability, what it expected.
