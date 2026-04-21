package userManagement;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

//@WebServlet("/LogoutServlet")
public class LogoutServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;
	
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// System.out.println("Now I am before if");
		request.getSession().invalidate();
	    response.sendRedirect(request.getContextPath() + "/login.jsp");
		
		//HttpSession session = request.getSession(false); //does not create if not existing
		/*
		 * if (session != null) { 
		 * //session.invalidate(); session.removeAttribute("username");
		 * RequestDispatcher dispatcher = request.getRequestDispatcher("/login.jsp");
		 * dispatcher.forward(request, response);
		 * response.sendRedirect("login.jsp");
		 */	
	    }
	
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		//System.out.println("Now I am before if");
		request.getSession().invalidate();
	    response.sendRedirect(request.getContextPath() + "/login.jsp");
	}

}
