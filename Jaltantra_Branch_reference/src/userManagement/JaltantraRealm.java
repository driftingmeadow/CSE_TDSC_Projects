//package userManagement;

// This realm used for Apache Shiro Authentication

//import java.sql.Connection;
//import org.apache.shiro.authc.AuthenticationException;
//import org.apache.shiro.authc.AuthenticationInfo;
//import org.apache.shiro.authc.AuthenticationToken;
//import org.apache.shiro.authc.SimpleAuthenticationInfo;
//import org.apache.shiro.authz.AuthorizationInfo;
//import org.apache.shiro.realm.AuthorizingRealm;
//import org.apache.shiro.subject.PrincipalCollection;
//import org.apache.shiro.util.ByteSource;
//
//public class JaltantraRealm extends AuthorizingRealm{
//	
//	private UserDao userDao = new UserDao();
//	@Override
//    protected AuthenticationInfo doGetAuthenticationInfo(
//            AuthenticationToken token) throws AuthenticationException {
//        String username = (String) token.getPrincipal(); // Get username
//        Connection conn = null;
//        try {
//            conn =  UserDao.initializeDatabase();
//            User user = userDao.getByUsername(conn, username); // User information detected based on user name only
//            if (user != null) {
//            	
//            	//Without Encryption - Working:
//                //AuthenticationInfo authcInfo = new SimpleAuthenticationInfo(user.getUsername(), user.getPassword(), "myRealm");
//                
//            	//With Encryption
//            	String salt = "salt12345";
//            	ByteSource saltByte = ByteSource.Util.bytes(salt);
//                AuthenticationInfo authcInfo = new SimpleAuthenticationInfo(user.getUsername(), user.getPassword(), saltByte, "myRealm");
//                
//                return authcInfo;
//            } else {
//                return null;
//            }
//        } catch (Exception e) {
//            // TODO Auto-generated catch block
//            e.printStackTrace();
//        } finally {
//            try {
//                //Close the database connection
//				conn.close();
//            } catch (Exception e) {
//                e.printStackTrace();
//            }
//        }
//        return null;
//    }
//
//	@Override
//	protected AuthorizationInfo doGetAuthorizationInfo(PrincipalCollection arg0) {
//		return null;
//	}
//}
