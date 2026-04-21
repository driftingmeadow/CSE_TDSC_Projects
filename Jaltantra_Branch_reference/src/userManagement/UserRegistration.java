package userManagement;

import java.io.IOException;
import java.io.PrintWriter;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
//import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

//import org.apache.shiro.crypto.hash.SimpleHash; // Required in case of Apachi Shiro re-integration

//@WebServlet("/UserRegistration")	// Servlet Name
public class UserRegistration extends HttpServlet {
	private static final long serialVersionUID = 1L;
	
	//HashFunction using no apache shiro. 
	public static String hashFunction(String password) throws NoSuchAlgorithmException {
		  String salt = "salt12345"; // Extra text to be used while password hashing
		  byte[] saltArrray = salt.getBytes(); 
		  MessageDigest md = MessageDigest.getInstance("MD5");
		  //Add password bytes to digest
		  md.update(saltArrray); 
		  //Get the hash's bytes 
		  byte[] bytess = md.digest(password.getBytes()); 
		  //perform the hashing for 2nd time for more security 
		  byte[] bytes = md.digest(bytess);
		  
		  //This bytes[] has bytes in decimal format, convert it to hexadecimal format
		  StringBuilder passwd = new StringBuilder(); 
		  for(int i=0; i< bytes.length ;i++) 
		  {
			  passwd.append(Integer.toString((bytes[i] & 0xff) + 0x100, 16).substring(1)); 
		  }
		  //Get complete hashed password in Hex format 
		  return passwd.toString();	
	}

	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		try {
			// Initialize the database connection
			Connection conn = UserDao.initializeDatabase();

			String fullName = request.getParameter("fullname");
			String username = request.getParameter("username").trim();
			String organization = request.getParameter("organization").trim();
			String organizationFromInput = request.getParameter("organizationFromInput");
			if (organization.equals("Please Select Your Organization")) {
				organization = organizationFromInput;
			}

			String country = request.getParameter("country");
			String state = request.getParameter("state");
			String email = request.getParameter("email");
			String unencrypted_pwd = request.getParameter("password");

			// Create a SQL query to insert data into jaltantra_users table
			PreparedStatement st = conn.prepareStatement(
					"insert into jaltantra_users (fullname, username, organization, state, country, email, password) VALUES(?, ?, ?, ?, ?, ?, ?)");

			String password = hashFunction(unencrypted_pwd);
			
			// Hashing using Apache Shiro. This will be used if we re-integrate Apache Shiro.
			/*
			 * SimpleHash encrypted_pwd = new SimpleHash("MD5", unencrypted_pwd, salt, 2);
			 * String password = encrypted_pwd.toString();
			 */
			
			// For the parameters, get the data using request object and set the data to st pointer
			// st.setInt(1, Integer.valueOf(request.getParameter("id")));
			// st.setInt(1,1); // Used for ID, here it is self incremental in MySQL database
			st.setString(1, fullName);
			st.setString(2, username);
			st.setString(3, organization);
			st.setString(4, state);
			st.setString(5, country);
			st.setString(6, email);
			st.setString(7, password);

			PreparedStatement st2 = conn.prepareStatement("select * from jaltantra_users where username = ?");
			st2.setString(1, username);
			ResultSet r1 = st2.executeQuery();

			// If user already exists, redirect to registration page
			if (r1.next()) {
				request.setAttribute("error", "This \"User Name\" already exists. Please select a different username. Thank You!");
				RequestDispatcher rd = getServletContext().getRequestDispatcher("/register.jsp");
				rd.include(request, response);
				
				/*
				 * PrintWriter out = response.getWriter();
				 * 
				 * out.println("<script type=\"text/javascript\">"); out.
				 * println("alert('This username already exists. Please select a different username. Thank You!');"
				 * ); out.println("location='register.jsp';"); out.println("</script>");
				 */

				// Close the database connections
				st.close();
				conn.close();
			}
			// If user does not exits, execute the insert command using executeUpdate() to
			// make changes in database
			else {
				st.executeUpdate();
				// Close the database connections
				st.close();
				conn.close();

				// Get a writer pointer to display the successful result
				PrintWriter out = response.getWriter();
				out.println("<html><body style='text-align:center'> <br><br><br><b>Successfully Registred,"
						+ " Please login:  <a href=\"login.jsp\">Login</a> " + "</b></body></html>");
			}
		} catch (Exception e) {
			request.setAttribute("error", "Something Went Wrong, Please Try Again");
			RequestDispatcher rd = getServletContext().getRequestDispatcher("/register.jsp");
			rd.include(request, response);
			e.printStackTrace();
		}
	}
}
