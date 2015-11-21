package com.shzhangji.timetable.model;

import java.util.Date;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

import lombok.Data;

@Entity
@Data
public class Event {
	@Id
	@GeneratedValue
	private Integer id;
	private String title;
	private Date start;
	private Date end;
	@Column(updatable = false)
	private Date created;
	private Date updated;
}
