package userManagement;

import java.io.IOException;
//import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
//import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

//import org.apache.shiro.crypto.hash.SimpleHash;

public class LoginServlet extends HttpServlet{

	private static final long serialVersionUID = 1L;

	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException
	{
		try {  
			// Initialize the database connection
			Connection conn = UserDao.initializeDatabase();

			
			String username = request.getParameter("username").trim();           
			String unencrypted_pwd = request.getParameter("password");
			
			String password = UserRegistration.hashFunction(unencrypted_pwd);
			  
            
            //Apache Shiro Hashing
			/*
			 * SimpleHash encrypted_pwd = new SimpleHash("MD5", unencrypted_pwd, salt, 2);
			 * String password = encrypted_pwd.toString();
			 */
 
            PreparedStatement select = conn.prepareStatement("select username, password from jaltantra_users where username = ? and password = ?");
			select.setString(1, username);
			select.setString(2, password);
			ResultSet r1 = select.executeQuery();

			//If username and password matches, login
			if(r1.next() && username.equalsIgnoreCase(r1.getString(1))  && password.equals(r1.getString(2))) {
				
				HttpSession session = request.getSession();
				session.setAttribute("username", username);
				//setting session to expiry in 180 mins (3 Hrs)
				session.setMaxInactiveInterval(180*60);
				/*
				 * Cookie userName = new Cookie("user", username); 
				 * userName.setMaxAge(180*60);
				 * response.addCookie(userName);
				 */
				response.sendRedirect("system.jsp");
				// Close the database connections
				select.close();
				conn.close();
			}
			// If user does not exits, execute the insert command using executeUpdate() to make changes in database
			else {
				request.setAttribute("error","Invalid Username or Password");
				RequestDispatcher rd = getServletContext().getRequestDispatcher("/login.jsp");
				rd.include(request, response);			 
			}
		}
		catch (Exception e) {
			request.setAttribute("error","Something Went Wrong, please check all your inputs and try again");
			RequestDispatcher rd = getServletContext().getRequestDispatcher("/login.jsp");
			rd.include(request, response);	
			e.printStackTrace();
		}
	}
}

