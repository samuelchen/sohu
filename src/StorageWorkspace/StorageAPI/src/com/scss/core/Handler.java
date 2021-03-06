/**
 * Copyright (c) Sohu Inc. 2012
 * 
 * Handle the requests
 */
package com.scss.core;

import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.CopyOnWriteArraySet;

import org.apache.log4j.Logger;
import org.restlet.Request;
import org.restlet.data.Form;
import org.restlet.data.MediaType;
import org.restlet.data.Method;
import org.restlet.data.Status;
import org.restlet.engine.resource.VariantInfo;
import org.restlet.representation.Representation;
import org.restlet.resource.Delete;
import org.restlet.resource.Get;
import org.restlet.resource.Post;
import org.restlet.resource.Put;
import org.restlet.resource.ServerResource;

import com.scss.Headers;
import com.scss.Operation;
import com.scss.OperationResult;
import com.scss.core.security.Authorization;
import com.scss.core.security.AuthorizationTypes;
import com.scss.core.security.IAuth;
import com.scss.db.User;
import com.scss.db.dao.ScssUserDaoImpl;
import com.scss.db.model.ScssUser;


/**
 * API request handler. To dispatch requests.
 * 
 * @author Samuel
 *
 */
public class Handler extends ServerResource {
	
	private Logger logger = Logger.getLogger(this.getClass());
	
	public Handler() {
		super();
		// TODO: move per resource in the future when use real restlet resource
		this.Init();
	}

	@Get
	public Representation RequestGET() throws InvaildRequestException{
		return this.Process();
		
		/*
		Request req = this.getRequest();
		
		// TODO: Assign a monitor to monitor the tracfic, request times and so on.
		// com.scss.utility.Monitor montior = new com.scss.utility.Monitor(req);

		// header process
		Map<String, String> headers = this.getRequestHeaders();
		
		// Authorize
		if (!this.Authorize(headers)){
			System.out.printf("Fail to authorize.\n");
		}
		
		if (Method.HEAD.equals(getMethod())) {
			// HEAD request 
//			Representation rep = new EmptyRepresentation(); 
//			rep.setModificationDate(cmd.getLastModif().getTime()); 
//			rep.setSize(cmd.getSize()); 
//			rep.setMediaType(new MediaType(cmd.getMimeType())); 
//			return rep; 
		} else { 
			// GET request
			
			
		} 
				
		return null;
		*/
	}
	
	
	@Post
	public Representation RequestPOST(Representation entity) throws InvaildRequestException{
		return this.Process();
	}
	
	@Put
	public Representation RequestPUT(Representation entity) throws InvaildRequestException {
		this.getVariants().add(new VariantInfo(MediaType.APPLICATION_OCTET_STREAM));
		return this.Process();
		
	}
	
	@Delete
	public Representation RequestDELETE() throws InvaildRequestException {
		return this.Process();
	}
	
	
	
	/*
	 * TODO: override handle() later.
	 */
	protected Representation Process() throws InvaildRequestException {
		logger.info(" ========= Request incoming ========= ");
		
		APIRequest req = new APIRequest(this.getRequest());
		
		// TODO: Assign a monitor to monitor the tracfic, request times and so on.
		// com.scss.utility.Monitor montior = new com.scss.utility.Monitor(req);
		
		
		// header process
		req.setHeaders(this.getRequestHeaders());
		
		// Authorize
		if (!this.Authorize(req)) {
			logger.info("Fail to authorize.");
			ErrorResponse err_resp = ErrorResponse.AccessDenied(req);
			this.getResponse().setStatus(new Status(err_resp.getHttp_status()));
			return err_resp.Repr;
		} else
			logger.info("Request authorized.");
			// TODO: process to quit flow.
		
		// Operation
		Operation op =  Operation.create(req);
		OperationResult result = op.perform();
		
		if (null != result) {
			APIResponse resp = (APIResponse)result.Value;
			Form resp_headers = (Form)this.getResponse().getAttributes().get("org.restlet.http.headers");
			if (result.Succeed) {
				logger.info("Operation succeed.");
				if (resp_headers == null)  {  
					resp_headers = new Form();  
					getResponse().getAttributes().put("org.restlet.http.headers", resp_headers);  
				} 
				
				for (String key: resp.getHeaders().keySet()) {
					//TODO: fix the warning
					//2012-2-20 12:05:47 org.restlet.engine.http.header.HeaderUtils addExtensionHeaders
					//警告: Addition of the standard header "Content-Length" is not allowed. Please use the equivalent property in the Restlet API.
					//resp_headers.set(key, resp.getHeaders().get(key));
					resp_headers.add(key, resp.getHeaders().get(key));
					
				}
				
				getResponse().getServerInfo().setAgent("s3.itc.cn");
				getResponse().setLocationRef("/" + req.BucketName);
				
				
			} else {
				ErrorResponse err_resp = (ErrorResponse)resp;
				this.getResponse().setStatus(new Status(err_resp.getHttp_status()));
				logger.info(String.format("Operation failed. (%d %s)", err_resp.getHttp_status(), err_resp.code));
			}
			
			logger.debug(" >>>>> Successfully return <<<<<");
			return resp.Repr;
		} 
		logger.debug(" >>>>> Failure return <<<<<");
		return null;
	}
	
	
	/*
	 * collect required request headers
	 * TODO: Is it necessary? Make it a class ? refactor it.
	 */
	protected Map<String, String> getRequestHeaders(){
		Request req = getRequest();
		Form form_headers = (Form)req.getAttributes().get("org.restlet.http.headers");
		Map<String, String> headers = form_headers.getValuesMap();
		
		logger.debug(String.format("Method : %s", req.getMethod().toString()));
		logger.debug(String.format("HostRef : %s", req.getHostRef().toUri()));
		logger.debug(String.format("RootRef : %s", req.getRootRef()));
		logger.debug(String.format("OriginalRef : %s", req.getOriginalRef()));
		logger.debug(String.format("ResourceRef : %s", req.getResourceRef()));
		logger.debug(String.format("Ranges : %s", req.getRanges().toString()));
		logger.debug(String.format("Query : %s", req.getResourceRef().getQuery()));
		for (String key:form_headers.getNames()) {
			logger.debug(String.format("%s : %s", key, form_headers.getValues(key).toString()));
		}
		logger.debug(String.format("data: %s", req.getEntityAsText()));
		
		return headers;
	}
	
	/*
	 * Authorize the request
	 * TODO: convert to class or module
	 */
	protected Boolean Authorize(APIRequest req) {
		logger.debug("Start fake authorization.");
		String id = "FAKE_ACCESS_ID_00002";
		String req_auth = req.getHeaders().get(Headers.AUTHORIZATION);
		if (null != req_auth) {
			String[] authes = req_auth.split("\\s|:");
			if (3 == authes.length){
				id = authes[1];
			}
		}
		ScssUser suser = ScssUserDaoImpl.getInstance().getUserByAccessId(id);
		logger.debug(String.format("Authorized user : %s", suser));
		req.setUser(new User(suser));
		return true;
//		IAuth auth = Authorization.createInstace(req);
//		return auth.authorize();
	}
	
	/*
	 * Add supported methods and media types 
	 * TODO : Promote per resource.
	 */
	protected void Init () {
		Set<Method> allowedMethods = new HashSet<Method>(); 
		allowedMethods.add(Method.GET);
		allowedMethods.add(Method.PUT);
		allowedMethods.add(Method.POST);
		allowedMethods.add(Method.DELETE);
		allowedMethods.add(Method.HEAD);
		this.setAllowedMethods(new CopyOnWriteArraySet<Method>(allowedMethods));
		logger.info(String.format("%s initialized", this.getClass()));		
	}
	
	
}
