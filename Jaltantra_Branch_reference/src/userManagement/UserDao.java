package userManagement;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
  
// This class can be used to initialize the database connection
public class UserDao {
    public static Connection initializeDatabase()
        throws SQLException, ClassNotFoundException
    {
        // Initialize all the information regarding Database Connection
        //String dbDriver = "com.mysql.jdbc.Driver";
    	
    	String dbDriver = "com.mysql.cj.jdbc.Driver";
        String dbURL = "jdbc:mysql://localhost:3306/";
        // Database name, database user and password to access
        String dbName = "jaltantra_db";
        String dbUsername = "jaltantra_branch";
        String dbPassword = "jaltantra_branch";
  
        Class.forName(dbDriver);
        Connection conn = DriverManager.getConnection(dbURL + dbName ,dbUsername, dbPassword);
        return conn;
    }
    
  //Find user based on user name
    public User getByUsername(Connection conn, String username) throws Exception {
 
        User resultUser = null;
        String sql = "select * from jaltantra_users where username=?";
        PreparedStatement ps = conn.prepareStatement(sql);
        ps.setString(1, username);
        ResultSet rs = ps.executeQuery();
        if(rs.next()) {
            resultUser = new User();
            //resultUser.setId(rs.getInt("id"));
            resultUser.setUsername(rs.getString("username"));
            resultUser.setPassword(rs.getString("password"));
        }
        return resultUser;
    }
}