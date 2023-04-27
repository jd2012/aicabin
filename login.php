<?php
// Check if the login form has been submitted
if (isset($_POST['username']) && isset($_POST['password'])) {
	// Attempt to log in
	$username = $_POST['username'];
	$password = $_POST['password'];
	
	// Connect to the database
	$mysqli = new mysqli("localhost", "username", "password", "database_name");
	if ($mysqli->connect_error) {
		die("Failed to connect to database: " . $mysqli->connect_error);
	}
	
	// Check if the username and password are correct
	$stmt = $mysqli->prepare("SELECT * FROM users WHERE username = ? AND password = ?");
	$stmt->bind_param("ss", $username, $password);
	$stmt->execute();
	$result = $stmt->get_result();
	if ($result->num_rows == 1) {
		// Log in successful, redirect to availability calendar
		session_start();
		$_SESSION['username'] = $username;
		header("Location: availability.php");
		exit();
	} else {
		// Log in failed, display error message
		echo "Invalid username or password.";
	}
}
?>
<!DOCTYPE html>
<html>
<head>
	<title>Login</title>
</head>
<body>
	<h1>Login</h1>
	<form action="login.php" method="post">
		<label for="username">Username:</label>
