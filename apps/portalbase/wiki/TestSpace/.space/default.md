<html>
<head>
	<!-- need to add to jslib -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
	<link rel="stylesheet" href="/jslib/old/bootstrap/css/bootstrap-responsive.css">
	<link rel="stylesheet" href="/jslib/flatui/css/flat-ui.css">
	<!-- need to add to jslib -->
	<style type="text/css">
		body{
			margin-top: -15px;
		}
		.navbar{
			border-radius: 0;
			border-bottom-right-radius: 6px;
			border-bottom-left-radius: 6px;
		}
		h1, .h1{
			font-size: 40px;
		}
		h2, .h2{
			font-size: 35px;
		}
		h3, .h3{
			font-size: 30px;
		}
		h4, .h4{
			font-size: 25px;
		}
		h5, .h5{
			font-size: 23px;
		}
		h6, .h6{
			font-size: 20px;
		}
		.navbar-collapse .navbar-nav.navbar-left:first-child{
			margin-left: 0;
		}
		.navigation a{
			font-size: 14px;
		}
		.navigation{
			padding-top: 3%;
		}
		.navbar-nav > li > a{
			padding: 15px 21px !important;
		}
	</style>
</head>
<body style="background: #ECF0F1;">
	<header class="container" style="padding: 0;">
		<div>
			<nav class="navbar navbar-inverse navbar-embossed" role="navigation">
	            <div class="navbar-header">
	              <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#navbar-collapse-01">
	                <span class="sr-only">Toggle navigation</span>
	              </button>
	              <a class="navbar-brand" href="#">Portal/Jumpscale7</a>
	            </div>
	            <div class="navbar-collapse" id="navbar-collapse-01">
	              <ul class="nav navbar-nav navbar-left">
	              {{adminmenu}}
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
<div class="col-md-2 navigation">
{{navigation}}
</div>
<div class="col-md-10">
{% block body %}{% endblock %}
</div>
</div>
<footer class="container">
</footer>
<script src="/jslib/jquery/jquery-2.0.3.min.js"></script>
<script src="/jslib/flatui/js/flat-ui.min.js"></script>
</body>
</html>