package userManagement;

import java.io.IOException;
import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.annotation.WebFilter;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

@WebFilter(
		urlPatterns = {"/LoginFilter",	"/system.jsp", "/login.jsp"	} 
		// , servletNames = { "OptimizerServlet" }
		)

public class LoginFilter implements Filter {

	@Override
	public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain) throws IOException, ServletException {
		HttpServletRequest request = (HttpServletRequest) req;
        HttpServletResponse response = (HttpServletResponse) res;
        HttpSession session = request.getSession(false);
        String loginURI = request.getContextPath() + "/login.jsp";
        boolean loggedIn = session != null && session.getAttribute("username") != null;
        boolean loginRequest = request.getRequestURI().equals(loginURI);
        
        if(loginRequest) {
	        if (loggedIn) {
	        	// Redirect to Jaltantra system page
	        	response.sendRedirect(request.getContextPath() + "/system.jsp");
	        }
	        else {
	        	// Nothing to do if user has not logged in, just pass the request along the filter chain
	            chain.doFilter(request, response);
	        }
        }
        else {
        	if(loggedIn) {
        		// Nothing to do if user has not logged in, just pass the request along the filter chain
	            chain.doFilter(request, response);
        	}
        	else {
        		// Redirect to login page 
        		response.sendRedirect(loginURI);
        	}
        }
	}


	@Override
	public void destroy() {
		
	}

	@Override
	public void init(FilterConfig filterConfig) throws ServletException {
		
	}

}
