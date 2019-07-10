<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
		<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
		<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>

		<%
			String username = (String) session.getAttribute("username");
			if (username == null) {
				username == null)
			}
			boolean loggedIn = false;
			if(username.equals("")) {
				loggedIn = false;
			} else {
				loggedIn = true;
			}
		%>

		
	</head>

	<body>
		<div class="container-fluid p-0 d-flex flex-column h-100">
			<form class="w-100" method="POST">
				<div class="form-group">
					<input type="text" class="form-control" id="usernameInput" placeholder="Username">
					<input type="password" class="form-control" id="passwordInput" placeholder="Password">
				</div>
				<p id="errorMessage" class="form-text text-muted"> </p>
				<div class="text-center">
					<button type="submit" class="btn">Login</button>
			</form>

		</div>
	</body>

</html>