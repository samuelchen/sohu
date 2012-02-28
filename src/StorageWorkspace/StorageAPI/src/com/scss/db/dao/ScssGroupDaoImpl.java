package com.scss.db.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

import com.ibatis.sqlmap.client.SqlMapClient;
import com.scss.db.connpool.config.IbatisConfig;
import com.scss.db.exception.SameNameException;
import com.scss.db.model.ScssGroup;
import com.scss.db.model.ScssUser;

public class ScssGroupDaoImpl {
	private static final SqlMapClient sqlMap = IbatisConfig.getSqlMapInstance();
	private static ScssGroupDaoImpl instance = new ScssGroupDaoImpl();

	private ScssGroupDaoImpl() {
	}

	public static ScssGroupDaoImpl getInstance() {
		return instance;
	}

	public ScssGroup getGroupById(Long groupId) {
		ScssGroup su = null;
		try {
			su = (ScssGroup) sqlMap.queryForObject("getGroupById", groupId);
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return su;
	}

	public ScssGroup getGroupByName(String name) {
		ScssGroup su = null;
		try {
			su = (ScssGroup) sqlMap.queryForObject("getGroupByName", name);
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return su;
	}

	public ScssGroup insertGroup(ScssGroup group) {
		ScssGroup su = null;
		try {
			su.setId((Long) sqlMap.queryForObject("putGroup", group));
			if (su.getUserIds() == null)
				su.setUserIds(",");
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return su;
	}

	public void putUserToGroup(ScssUser user, ScssGroup sg) throws SQLException {
		putUserIdsToGroup(user.getId() + "", sg);
	}

	public void updateGroup(ScssGroup sg) throws SQLException {
		sqlMap.update("updateGroup", sg);
	}

	public void putUserIdsToGroup(String ids, ScssGroup sg) throws SQLException {
		if ((ids == null) || ("".equals(ids))) {
			return;
		}
		String newIds = sg.getUserIds();
		if ((newIds == null) || ("".equals(newIds)))
			newIds = "," + ids + ",";
		else
			newIds = newIds + ids + ",";
		sg.setUserIds(newIds);
		sqlMap.update("updateGroup", sg);
	}

	public void deleteGroup(ScssGroup sg) throws SQLException {
		deleteGroup(sg.getId());
	}

	public static void deleteGroup(Long gid) throws SQLException {
		sqlMap.delete("deleteGroup", gid);
	}
}