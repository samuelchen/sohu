package com.scss.db.dao;

import java.sql.SQLException;
import java.util.List;
import java.util.Map;

import com.ibatis.sqlmap.client.SqlMapClient;
import com.scss.db.connpool.config.IbatisConfig;
import com.scss.db.dao.i.ILog;
import com.scss.db.model.ScssLog;
import com.scss.db.model.ScssUser;
/**
 * 
 * @author Jack.wu.xu
 */
public class ScssLogDaoImpl implements ILog{
	private static final SqlMapClient sqlMap = IbatisConfig.getSqlMapInstance();
	private static ScssLogDaoImpl instance = new ScssLogDaoImpl();

	private ScssLogDaoImpl() {
	}

	public static ScssLogDaoImpl getInstance() {
		return instance;
	}

	public ScssLog writeLog(ScssLog log) throws SQLException {
		try {
			log.setId((Long) sqlMap.insert("putLog", log));
		} catch (SQLException e) {
			e.printStackTrace();
			throw e;
		}
		return log;
	}
	public ScssLog getLog(Long id) {
		ScssLog log = null;
		try {
			log = (ScssLog) sqlMap.queryForObject("getLog", id);
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return log;
	}

	public List<ScssLog> getLogsByUser(ScssUser user) {
		List logs = null;
		try {
			logs = sqlMap.queryForList("getLogsByUserId", user.getId());
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return logs;
	}
	public List<ScssLog> getLogsByUserId(Long userId) {
		List logs = null;
		try {
			logs = sqlMap.queryForList("getLogsByUserId", userId);
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return logs;
	}
	
	public List<ScssLog> getLogsByAction(String action) {
		List logs = null;
		try {
			logs = sqlMap.queryForList("getLogsByAction", action);
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return logs;
	}
	public List<ScssLog> getLogsByLevel(String level) {
		List logs = null;
		try {
			logs = sqlMap.queryForList("getLogsByLevel", level);
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return logs;
	}
	/**
	 * 
	 * @param map:map must constion startTime(Date) and endTime(Date)<br>
	 * @return List<ScssLog>
	 */
	public List<ScssLog> getLogsByDateRange(Map map) {
		List logs = null;
		try {
			logs = sqlMap.queryForList("getLogsByDateRange", map);
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return logs;
	}
	
	
//	public List<ScssLog> getLogsOnResource(Resource r) {
//		List logs = null;
//		try {
//			logs = sqlMap.queryForList("getLogsOnResource", r);
//		} catch (SQLException e) {
//			e.printStackTrace();
//		}
//		return logs;
//	}
	public void deleteLog(ScssLog log) throws SQLException {
		sqlMap.update("deleteLog", log);
	}
}
