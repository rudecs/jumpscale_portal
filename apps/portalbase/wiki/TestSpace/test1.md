{% extends ".space/default.md" %}

{% block body %}
# Dillinger

Dillinger is a cloud-enabled, mobile-ready, offline-storage, AngularJS powered HTML5 Markdown editor.

  - Type some Markdown on the left
  - See HTML in the right
  - Magic

Markdown is a lightweight markup language based on the formatting conventions that people naturally use in email.  As [John Gruber] writes on the [Markdown site] [1]:

> The overriding design goal for Markdown's
> formatting syntax is to make it as readable
> as possible. The idea is that a
> Markdown-formatted document should be
> publishable as-is, as plain text, without
> looking like it's been marked up with tags
> or formatting instructions.

This text you see here is *actually* written in Markdown! To get a feel for Markdown's syntax, type some text into the left window and watch the results in the right.

### Version
3.0.2

### Tech

Dillinger uses a number of open source projects to work properly:

* [AngularJS] - HTML enhanced for web apps!
* [Ace Editor] - awesome web-based text editor
* [Marked] - a super fast port of Markdown to JavaScript
* [Twitter Bootstrap] - great UI boilerplate for modern web apps
* [node.js] - evented I/O for the backend
* [Express] - fast node.js network app framework [@tjholowaychuk]
* [Gulp] - the streaming build system
* [keymaster.js] - awesome keyboard handler lib by [@thomasfuchs]
* [jQuery] - duh

### Installation

You need Gulp installed globally:

```sh
$ npm i -g gulp
```

```sh
$ git clone [git-repo-url] dillinger
$ cd dillinger
$ npm i -d
$ mkdir -p public/files/{md,html,pdf}
$ gulp build --prod
$ NODE_ENV=production node app
```

### Plugins

Dillinger is currently extended with the following plugins

* Dropbox
* Github
* Google Drive
* OneDrive

Readmes, how to use them in your own application can be found here:

* plugins/dropbox/README.md
* plugins/github/README.md
* plugins/googledrive/README.md
* plugins/onedrive/README.md

### Development

Want to contribute? Great!

Dillinger uses Gulp + Webpack for fast developing.
Make a change in your file and instantanously see your updates!

Open your favorite Terminal and run these commands.

First Tab:
```sh
$ node app
```

Second Tab:
```sh
$ gulp watch
```

(optional) Third:
```sh
$ karma start
```

### Todo's

 - Write Tests
 - Rethink Github Save
 - Add Code Comments
 - Add Night Mode

License
----

MIT


**Free Software, Hell Yeah!**

[john gruber]:http://daringfireball.net/
[@thomasfuchs]:http://twitter.com/thomasfuchs
[1]:http://daringfireball.net/projects/markdown/
[marked]:https://github.com/chjj/marked
[Ace Editor]:http://ace.ajax.org
[node.js]:http://nodejs.org
[Twitter Bootstrap]:http://twitter.github.com/bootstrap/
[keymaster.js]:https://github.com/madrobby/keymaster
[jQuery]:http://jquery.com
[@tjholowaychuk]:http://twitter.com/tjholowaychuk
[express]:http://expressjs.com
[AngularJS]:http://angularjs.org
[Gulp]:http://gulpjs.com


{{comparison:
	currency=$

	block.1.title.text=Beginner
	block.1.title.size=medium
	block.1.subtitle.text=Beginner Package
	block.1.price=10
	block.1.price.subtitle=per month
	block.1.property.1=Feature 1  \n Feature 1.1
	block.1.property.2=Feature 2
	block.1.property.3=Feature 3
	block.1.property.4=Feature 4
	block.1.order.button.text=Order now
	block.1.order.button.style=info
	block.1.order.button.subtext=Free Features
	block.1.order.button.link=Comparison

	block.2.title.text=Professional
	block.2.title.size=medium
	block.2.subtitle.text=Professional Package
	block.2.price=20
	block.2.price.subtitle=per month
	block.2.property.1=Feature 1  \n Feature 1.1
	block.2.property.2=Feature 2
	block.2.property.3=Feature 3
	block.2.property.4=Feature 4
	block.2.order.button.text=Order now
	block.2.order.button.style=success
	block.2.order.button.subtext=Free Features
	block.2.order.button.link=Comparison

	block.3.title.text=Expert
	block.3.title.size=medium
	block.3.subtitle.text=Expert Package
	block.3.price=30
	block.3.price.subtitle=per month
	block.3.property.1=Feature 1  \n Feature 1.1
	block.3.property.2=Feature 2
	block.3.property.3=Feature 3
	block.3.property.4=Feature 4
	block.3.order.button.text=Order now
	block.3.order.button.style=warning
	block.3.order.button.subtext=Free Features
	block.3.order.button.link=Comparison
}}


{% endblock %}