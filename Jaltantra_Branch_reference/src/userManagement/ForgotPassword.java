package userManagement;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

//import org.apache.shiro.crypto.hash.SimpleHash;

/**
 * Servlet implementation class ChangePassword
 */
//@WebServlet("/ChangePassword")
public class ForgotPassword extends HttpServlet {
	private static final long serialVersionUID = 1L;
	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException   
	{
		try {  
			// Initialize the database connection
			Connection conn = UserDao.initializeDatabase();

			String username = request.getParameter("username");           
			String email = request.getParameter("email");
			String unencrypted_newpwd = request.getParameter("newpassword");			
            
			String newpassword = UserRegistration.hashFunction(unencrypted_newpwd);
            
			/*
			 * SimpleHash encrypted_newpwd = new SimpleHash("MD5", unencrypted_newpwd, salt, 2); 
			 * String newpassword = encrypted_newpwd.toString();
			 */
        	// Create a SQL query to insert data into jaltantra_users table
			PreparedStatement update = conn
					.prepareStatement("update jaltantra_users set password=? where username=?");
							
						
			// For the parameters, get the data using request object and set the data to st pointer
			//st.setInt(1, Integer.valueOf(request.getParameter("id")));          
			update.setString(1, newpassword);
			update.setString(2, username);

			PreparedStatement select = conn.prepareStatement("select * from jaltantra_users where username = ?");
			select.setString(1, username);			
			ResultSet r1 = select.executeQuery();

			//If user  exists, Update the password
			if(r1.next() && email.equalsIgnoreCase(r1.getString(7))) {
				update.executeUpdate();  
				// Close the database connections
				update.close();
				conn.close();
				
				// Get a writer pointer to display the successful result 
				PrintWriter out = response.getWriter(); 
				out.println("<html><body style='text-align:center'> <br><br><br><b>Password Changed Successfully" +
				  " Please login:  <a href=\"login.jsp\">Login</a> " +
				  "</b></body></html>");
			}
			// If user does not exits, execute the insert command using executeUpdate() to make changes in database
			else {
				PrintWriter out = response.getWriter();
				  out.println("<script type=\"text/javascript\">"); out.
				  println("alert('Error: Your username or Registered Email is wrong, please try again or send an email to jaltantra.iitb@gmail.com');"); 
				  out.println("location='forgotpassword.jsp';"); 
				  out.println("</script>");
							
				//Close the database connections
				  update.close();
				conn.close();			 
			}
		}
		catch (Exception e) {
			e.printStackTrace();
		}
	}
}

