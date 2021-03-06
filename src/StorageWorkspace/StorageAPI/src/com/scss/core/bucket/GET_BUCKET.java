/**
 * Copyright Sohu Inc. 2012
 */
package com.scss.core.bucket;

import java.util.Date;
import java.util.List;
import java.util.Map;

import org.restlet.data.MediaType;

import com.scss.Const;
import com.scss.Headers;
import com.scss.IAccessor;
import com.scss.config.ConfigManager;
import com.scss.config.GeneralConfig;
import com.scss.core.APIRequest;
import com.scss.core.APIResponse;
import com.scss.core.ErrorResponse;
import com.scss.core.Mimetypes;
import com.scss.db.dao.ScssBucketDaoImpl;
import com.scss.db.dao.ScssObjectDaoImpl;
import com.scss.db.model.ScssBucket;
import com.scss.db.model.ScssObject;
import com.scss.utility.CommonUtilities;

/**
 * @author Samuel
 *
 */
public class GET_BUCKET extends BucketAPI {

	/* (non-Javadoc)
	 * @see com.scss.ICallable#Invoke(com.scss.core.APIRequest)
	 */
	@Override
	public APIResponse Invoke(APIRequest req) {
		
		Map<String, String> req_headers = req.getHeaders();
		
		// get system meta
		Date createTime = CommonUtilities.parseResponseDatetime(req_headers.get(Headers.DATE));
		Date modifyTime = createTime;
		// TODO: GET size if required. long size = req_headers.get(CommonResponseHeader.CONTENT_LENGTH)
		
		//TODO: Check ACL
		//TODO: Check whether Logging is enabled 
				
		String user_meta = this.getUserMeta(req);
		
		// DB process
		// TODO: consider a manager because there might be some logical process ?
		// TODO: Add transaction support if required (some apis need).
		// TODO: Use Bucket instead ScssBucket. temporary using.
		
		ScssBucket bucket=null;
		bucket = ScssBucketDaoImpl.getInstance().get(req.BucketName);
		if (null == bucket)
			return ErrorResponse.NoSuchBucket(req);
		List<ScssObject> bucket_objects=null;
		bucket_objects = (List<ScssObject>)ScssObjectDaoImpl.getInstance().getObjectsByBucketId(bucket.getId());
		
		// set response headers
		if (null != bucket_objects) {
			APIResponse resp = new BucketAPIResponse();
			Map<String, String> resp_headers = resp.getHeaders();
			
			// set common response header
			setCommResponseHeaders(resp_headers,req);
			
			// Set API response header
			//TODO: set user meta
			// user_meta key-value pair -> header
			
			// TODO: set system meta
	
			
			// generate representation
			resp.Repr = new org.restlet.representation.StringRepresentation(this.getResponseText(req, bucket_objects), MediaType.TEXT_XML);
			resp.MediaType = Mimetypes.MIMETYPE_XML;		
			return resp;
		}

		// TODO: return appropriate error response. DB access should return a value to determine status.
		logger.warn("GET_BUCKET is returning Interal error due to unexpected result");
		return ErrorResponse.InternalError(req);
	}
	
	private String getResponseText(APIRequest req, List<ScssObject> bucket_objects) {
		
		int maxkeys = 1000;
		String prefix = req.Querys.get("prefix");
		GeneralConfig conf = (GeneralConfig)ConfigManager.getInstance().get(GeneralConfig.class);
		
		// TODO: Use template? or make the string static
		StringBuilder sb = new StringBuilder();
		sb.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>");
		sb.append("<ListBucketResult xmlns=\"").append(conf.getXmlNamespace()).append("\">");
		sb.append("  <Name>").append(req.BucketName).append("</Name>");
		sb.append("  <Prefix>").append(prefix).append(" (Not implemented)</Prefix>"); // TODO: Not implemented
		sb.append("  <Marker />"); // TODO: Not implemented
		sb.append("  <MaxKeys>").append(maxkeys).append("</MaxKeys>"); // TODO: Not implemented
		sb.append("  <MaxKeysIsNotImplemented />"); // TODO: Not implemented
		sb.append("  <IsTruncated>false</IsTruncated>"); // TODO: Not implemented
		
		for(ScssObject obj: bucket_objects){
			sb.append("  <Contents>");
		    sb.append("    <Key>").append(obj.getKey()).append("</Key>");
		    sb.append("    <LastModified>").append(CommonUtilities.formatResponseTextDate(obj.getModifyTime())).append("</LastModified>");
		    sb.append("    <ETag>").append(obj.getEtag()).append("</ETag>"); 
		    sb.append("    <Size>").append(obj.getSize()).append("</Size>");
		    sb.append("    <StorageClass />"); // TODO: Not implemented
			sb.append("    <Owner>");
			sb.append("      <ID>").append(req.getUser().getAccessId()).append("</ID>");
			sb.append("      <DisplayName>").append(req.getUser().getSohuId()).append("</DisplayName>");
			sb.append("    </Owner>");
			sb.append("  </Contents>");
		}
		
		sb.append("</ListBucketResult>"); 
		return sb.toString();
	}

	/* (non-Javadoc)
	 * @see com.scss.ICallable#CanInvoke(com.scss.core.APIRequest, com.scss.IAccessor)
	 */
	@Override
	public Boolean CanInvoke(APIRequest req, IAccessor invoker) {
		// TODO Auto-generated method stub
		return true;
	}

}
