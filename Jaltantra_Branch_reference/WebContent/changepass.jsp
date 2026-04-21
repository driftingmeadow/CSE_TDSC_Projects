<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>

<!-- 	To enable JSP and JSTL Tags -->    
<%-- <%@ taglib prefix="shiro" uri="http://shiro.apache.org/tags" %> --%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8" />
<title>Jaltantra Change Password</title>
<link rel="stylesheet" type="text/css" href="css/w2ui-1.4.2.css" />
<link rel="stylesheet" type="text/css" href="css/style.css" />

	<script type="text/javascript">
   		//function to check the password mismatches
   		function validateForm()
		{				
			if(document.getElementById('newpassword').value != document.getElementById('password_confirm').value)
			//if ($('#password').val() == $('#password_confirm').val())
				{
					//$('#message').html('Password Mismatch').css('color', 'red');
					document.getElementById('message').style.color = 'red';
				    document.getElementById('message').innerHTML = 'Password Mismatch';					    					    
					return false;
				}
		}
   	</script>
	<style>	.required:after { content: " *"; color: red; }	
		input, select {  width: 250px;} 
	</style>

</head>
<body>
	
	<div style='text-align: center; line-height: 80px; height: 80px; font-size: 30px; background: beige; overflow: hidden'>
		JalTantra: System For Optimization of Piped Water Networks, IIT Bombay <img src="iitb_logo_black_small.png" alt="IITB" style="vertical-align:middle;width:80px;height:80px;background: transparent;">
	</div>
	<div class="container">
		<header> </header>
		<div id="wrapper">
			<div id="login" style='text-align: center;' class="animate form" >
				<form onsubmit="return validateForm();"	action="/jaltantra/ChangePassword" method="post">
					
					<h1>Change Password</h1>
					<div id="left" style='text-align: left;'>
					<table>
					<tr><td> <label class="required">User Name</label> </td><td><input id="usernamesignup" name="username" required="required" type="text" placeholder="User Name" /> </td></tr> 
					<tr><td> <label class="required">Current Password</label> </td><td><input id="passwordsignup" name="password" required="required"	type="password" placeholder="Password" /> </td></tr> 	
					<tr><td> <label class="required">New Password</label> </td><td><input id="newpassword" name="newpassword" required="required"	type="password" placeholder="New Password" /> </td></tr> 
					<tr><td> <label	class="required">Confirm New Password</label> </td><td> <input id="password_confirm" name="passwordsignup_confirm" required="required" type="password" placeholder="Confirm New Password" /> </td></tr> 
							
					</table>
					</div>
					<span id='message'></span>
							
					<p class="login button">
						<input type="submit" value="Change Password" />
					</p>
					
				</form>
				<p class="login button">
						<a href="login.jsp" class="to_register">Log in</a>
					</p>
			</div>
		</div>
	</div>
</body>
</html>