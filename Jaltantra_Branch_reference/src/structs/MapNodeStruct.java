package structs;
//container for map node information

//nodeid: unique integer id for a node
//nodename: name of the node
//latitude: latitude of the node
//longitude: longitude of the name
//elevation: elevation of the node in metres
//isesr: true if there is an ESR at the node
public class MapNodeStruct
{
	public int nodeid;
	public String nodename;
	public double latitude;
	public double longitude;
	public boolean isesr;
	public double elevation;
		
	public MapNodeStruct(int nodeid, String nodename, 
			double latitude, double longitude,double elevation, boolean isesr) {
		this.nodeid = nodeid;
		this.nodename = nodename;
		this.latitude = latitude;
		this.longitude = longitude;
		this.elevation = elevation;
		this.isesr = isesr;
	}

	@Override
	public String toString() {
		return "MapNodeStruct [nodeid=" + nodeid + ", nodename=" + nodename
				+ ", latitude=" + latitude + ", longitude=" + longitude 
				+ ", elevation=" + elevation + ", isesr=" + isesr + "]";   //function can receive and store elevation data
	}
}
