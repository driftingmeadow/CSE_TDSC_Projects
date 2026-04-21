<%@ page language="java" contentType="text/html; charset=UTF-8"   pageEncoding="UTF-8"%>

<%@ page import="java.sql.*" %>
<%@ page import= "java.util.ArrayList" %>
<%@ page import= "java.util.List" %>
<%List<String> orgList = new ArrayList<String>(); %>
<%ResultSet resultset =null; %>

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8" />
<title>Jaltantra User Registration</title>
<link rel="stylesheet" type="text/css" href="css/w2ui-1.4.2.css" />
<link rel="stylesheet" type="text/css" href="css/style.css" />

<script type="text/javascript">
    		//function to check the password mismatches
    		function validateForm()
			{				
				if(document.getElementById('passwordsignup').value != document.getElementById('password_confirm').value)
				//if ($('#password').val() == $('#password_confirm').val())
					{
						//$('#message').html('Password Mismatch').css('color', 'red');
						document.getElementById('message').style.color = 'red';
					    document.getElementById('message').innerHTML = 'Password Mismatch';					    					    
						return false;
					}
				if(document.getElementById('state').value =="Please Select Your State")
					{
						document.getElementById('message2').style.color = 'red';
					    document.getElementById('message2').innerHTML = 'State is required';					    					    
						return false;
					}
				if(document.getElementById('organization').value =="Please Select Your Organization"
						&& document.getElementById('organizationFromInput').value.trim()=="")
					{
						document.getElementById('message3').style.color = 'red';
					    document.getElementById('message3').innerHTML = 'Please either select your organizationor or write it below';					    					    
						return false;
					}
				const validEmail = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
				if(!(document.getElementById('emailsignup').value.match(validEmail))){
					document.getElementById('emailmsg').style.color = 'red';
				    document.getElementById('emailmsg').innerHTML = 'Invalid Email';
				    return false;
				}
			}   		
    		
    	</script>
<style>
.required:after {
	content: " *";
	color: red;
}
input, select {
  width: 250px;
} 
</style>

</head>
<body>
	
	<%
		try{
			String dbDriver = "com.mysql.cj.jdbc.Driver";
	        String dbURL = "jdbc:mysql://localhost:3306/";
	        // Database name, database user and password to access
	        String dbName = "jaltantra_db";
	        String dbUsername = "jaltantra_branch";
	        String dbPassword = "jaltantra_branch";
	        Class.forName(dbDriver);
	        Connection conn = DriverManager.getConnection(dbURL + dbName ,dbUsername, dbPassword);
	        String sql = "SELECT  DISTINCT organization FROM jaltantra_users ORDER BY organization;";
	        PreparedStatement ps = conn.prepareStatement(sql);
	        resultset =ps.executeQuery();
	        
	      /*   while(resultset.next()){
	        	String org = resultset.getString(1);
	        } */
		}catch(Exception e){
			e.printStackTrace();
		}
	%>
	
	<div style='text-align: center; line-height: 80px; height: 80px; font-size: 30px; background: beige; overflow: hidden'>
		JalTantra: System For Optimization of Piped Water Networks, IIT Bombay <img src="iitb_logo_black_small.png" alt="IITB" style="vertical-align:middle;width:80px;height:80px;background: transparent;">
	</div>
	<div class="container">
		<header> </header>
		<div id="wrapper">
			<div id="login" style='text-align: center;' class="animate form" >
				<form onsubmit="return validateForm();"	action="/jaltantra/UserRegistration" method="post">
					<p class="change_linkk">
						Existing Users: <a href="login.jsp" class="to_register">Please Login </a>
					</p>
					<h1>Sign up</h1>

					<p>
						<small>If you are not in India, please type your country </small>
					</p>

					<%
						String login_msg = (String) request.getAttribute("error");
					if (login_msg != null)
						out.println("<font color=red size=4px>" + login_msg + "</font>");
					%>

					<div id="left" style='text-align: left;'>
						<table>

							<tr>
								<td><label class="required">Full Name </label></td>
								<td><input id="fullname" name="fullname"
									required="required" type="text" placeholder="Full Name" /></td>
							</tr>

							<tr>
								<td><label class="required">User Name</label></td>
								<td><input id="usernamesignup" name="username"
									required="required" type="text"
									placeholder="Name to login with" /></td>
							</tr>

							<tr>
								<td><label class="required">Organization </label></td>
								<td><select class="select" id="organization"
									name="organization" style="width: 260px;">

										<option>Please Select Your Organization</option>
										<%  while(resultset.next()){ %>
										<option><%= resultset.getString(1)%></option>
										<% } %>
								</select> <span id='message3'></span></td>
							</tr>
							<tr>
								<td><label class="requiredd"> </label></td>
								<td><input id="organizationFromInput"
									name="organizationFromInput" type="text"
									placeholder="Add your organization if not listed above" /></td>
							</tr>
							<tr>
								<td><label class="required">Country </label></td>
								<td><input id="country" name="country" required type="text"
									value="India" /></td>
							</tr>
							<!-- 
					<tr><td> <label class="required">City and State </label> </td><td><input id="city" name="address" required="required"	type="text" placeholder="City,  State" /> </td></tr> 
					 -->
							<tr>
								<td><label class="required">State </label></td>
								<td><select id="state" name="state" style="width: 260px;">
							<script type="text/javascript">
							var states = new Array("Please Select Your State","Outside India", "Andaman and Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chandigarh", "Chhattisgarh", "Dadra and Nagar Haveli", "Daman and Diu", "Delhi", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala", "Ladakh", "Lakshadweep", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Orissa", "Puducherry", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttaranchal", "Uttar Pradesh",  "West Bengal");
							for(var hi=0; hi<states.length; hi++)
							document.write("<option value=\""+states[hi]+"\">"+states[hi]+"</option>");
							</script>
								</select> <span id='message2'></span></td>
							</tr>

							<tr>
								<td><label class="required">Email Address </label></td>
								<td><input id="emailsignup" name="email"
									required="required" type="email" placeholder="Email Address" /><span	id='emailmsg'></span>
								</td>
							</tr>

							<tr>
								<td><label class="required">Password</label></td>
								<td><input id="passwordsignup" name="password"
									required="required" type="password" placeholder="Password" />
								</td>
							</tr>

							<tr>
								<td><label class="required">Confirm Password</label></td>
								<td><input id="password_confirm"
									name="passwordsignup_confirm" required="required"
									type="password" placeholder="Confirm Password" /><span	id='message'></span></td>
							</tr>

						</table>
					</div>

					<p class="signin button">
						<input type="submit" value="Sign up" />
					</p>
				</form>
			</div>
		</div>
	</div>
</body>
</html>