/**
 * Copyright Sohu Inc. 2012
 */
package com.scss.core;

import java.net.URI;
import java.util.HashMap;
import java.util.Map;

import org.restlet.Request;

import com.scss.Const;
import com.scss.db.model.ScssUser;

/**
 * @author Samuel
 *
 */
public class APIRequest {
	protected Map<String, String> headers = null;
	protected ScssUser user = null;
	public String BucketName = null;
	public String ObjectKey = null;
	public URI URI = null;
	public String Path = null;
	public String Method = "GET";
	public String RequestID = null; // TODO: how to get?
	
	public APIRequest(Request request) throws InvaildRequestException {
		this.Method = request.getMethod().getName();
		this.URI = request.getOriginalRef().toUri();
		this.Path = request.getOriginalRef().getPath(true);
		if (!this.URI.isAbsolute()) {
			//TODO: try get absolute uri & path
		}
		
		String path = this.Path;
		URI uri = this.URI;

		// parse bucket name and object key
		String bucket_name = uri.getHost();
		if (null != bucket_name) {
			bucket_name = bucket_name.replace(Const.HOST, "");
			if (bucket_name.endsWith("."))
				bucket_name = bucket_name.substring(0, bucket_name.length()-1);
		}
		
		if (null == bucket_name || 0 == bucket_name.trim().length()) {
			String[] pathes = path.split("/", 3);
			if (3 == pathes.length) {
				bucket_name = pathes[1];
				path = "/" + pathes[2];
			} else if (2 == pathes.length){
				bucket_name = pathes[1];
				path = "/";
			} else {
				throw new InvaildRequestException("Invaild reqeust uri.");
			}
		}
		
		this.BucketName = bucket_name.trim();
		this.ObjectKey = path.trim();
		
	}

	public Map<String, String> getHeaders() {
		if (null == headers)
			headers = new HashMap<String, String>();
		return headers;
	}
	public void setHeaders(Map<String, String> headers) {
		this.headers = headers;
	}
	
	public ScssUser getUser() {
		return user;
	}
	public void setUser(ScssUser user) {
		this.user = user;
	}
}