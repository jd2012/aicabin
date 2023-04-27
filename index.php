<!DOCTYPE html>
<html>
<head>
	<title>Family Cabin Rental</title>
</head>
<body>
	<h1>Welcome to the Family Cabin Rental</h1>
	<p>Our cabin is a cozy retreat in the mountains, perfect for families and groups of friends. The cabin sleeps up to 6 people and comes equipped with a full kitchen, fireplace, and hot tub.</p>
	<?php
	// Check if the user is logged in
	session_start();
	if (isset($_SESSION['username'])) {
		// User is logged in, display link to availability calendar
		echo '<p>To check availability and make a reservation, please visit our <a href="availability.php">availability calendar</a>.</p>';
	} else {
		// User is not logged in, display login form
		echo '<form action="login.php" method="post">
			<label for="username">Username:</label>
			<input type="text" id="username" name="username" required>
			<label for="password">Password:</label>
			<input type="password" id="password" name="password" required>
			<input type="submit" value="Log In">
		</form>';
	}
	?>
</body>
</html>
