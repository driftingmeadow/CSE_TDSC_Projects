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
<title>Jaltantra User Login</title>
<link rel="stylesheet" type="text/css" href="css/w2ui-1.4.2.css" />
<link rel="stylesheet" type="text/css" href="css/style.css" />
<style>
	input, select {  width: 250px;} 
</style>
</head>

<body>
	<!-- To redirect to system.jsp if a user is already logged in-->
	<%-- <shiro:authenticated>
		<c:redirect url="system.jsp"/>
	</shiro:authenticated> --%>
	
	<%  if(session.getAttribute("username")!=null && session.getAttribute("username").equals(true))
		{
		   response.sendRedirect("system.jsp");
		}%>
	
	<div style='text-align: center; line-height: 80px; height: 80px; font-size: 30px; background: beige; overflow: hidden'>
		JalTantra: System For Optimization of Piped Water Networks, IIT Bombay <img src="iitb_logo_black_small.png" alt="IITB" style="vertical-align:middle;width:80px;height:80px;background: transparent;">
	</div>

	<div class="container">
		<div id="wrapper">
			<div id="login" style='text-align:center' class="animate form">
						<form name="loginform" action="/jaltantra/LoginServlet" method="POST" accept-charset="UTF-8" role="form">
							<h1>Log in</h1>
						<div id="left" style='text-align: left;'>
						<table>
							<tr><td> <label class="required">User Name </label> </td>  <td><input id="username" name="username" required="required" type="text" placeholder="User Name" /> </td></tr>
							<tr> <td> <label class="required"> Password </label> </td> <td><input id="password" name="password" required="required" type="password" placeholder="Password"/></td></tr>							
						</table>
						</div>
							<p style="color:red">
							<%-- <c:if test="${shiroLoginFailure != null}">
						    	Incorrect username or password, please try again 
							</c:if></p> --%>
							
							<%
							//Display an error message if login failed 
							String login_msg=(String)request.getAttribute("error");  
							if(login_msg!=null)
							out.println("<font color=red size=4px>"+login_msg+"</font>");
							%>
							
							<!-- To enable  Remember Me option-->
							<!-- <p class="keeplogin">
								<input name="rememberMe" type="checkbox" value="true" id="loginkeeping"/> 
								<label for="loginkeeping">Remember Me</label>
							</p> -->
							<p class="login button">
								<input type="submit" value="Login" />
							</p>
							<p class="change_link">
								Not a Jaltantra user yet? <a href="register.jsp" class="to_register">Please Register</a>
							</p>
						</form>
						<p class="login button">
								<a href="changepass.jsp" class="to_register">Change Password?</a>
							</p>
						<p class="login button">
								<a href="forgotpassword.jsp" class="to_register">Forgot Password?</a>
							</p>
					</div>
				</div>
			</div>
</body>
</html>