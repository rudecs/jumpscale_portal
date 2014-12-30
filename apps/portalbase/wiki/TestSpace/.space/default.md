<!DOCTYPE html>
<html>
<head>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
	<link rel="stylesheet" href="/jslib/old/bootstrap/css/bootstrap-responsive.css">
	<link rel="stylesheet" href="/jslib/flatui/css/flat-ui.css">
</head>
<body style="background: #ECF0F1;">
	<header class="container">
		<div class="row">
			<nav class="navbar navbar-inverse navbar-embossed" role="navigation">
	            <div class="navbar-header">
	              <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#navbar-collapse-01">
	                <span class="sr-only">Toggle navigation</span>
	              </button>
	              <a class="navbar-brand" href="#">Portal/Jumpscale7</a>
	            </div>
	            <div class="navbar-collapse" id="navbar-collapse-01">
	              <ul class="nav navbar-nav navbar-left">
	               </ul>
	               <form class="navbar-form navbar-right" action="#" role="search">
	                <div class="form-group">
	                  <div class="input-group">
	                    <input class="form-control" id="navbarInput-01" type="search" placeholder="Search">
	                    <span class="input-group-btn">
	                      <button type="submit" class="btn"><span class="fui-search"></span></button>
	                    </span>
	                  </div>
	                </div>
	              </form>
	            </div><!-- /.navbar-collapse -->
	          </nav>
		</div>
	</header>
	<div class="container" style="background: #fff;">
{% block body %}{% endblock %}
	</div>
</body>
</html>
