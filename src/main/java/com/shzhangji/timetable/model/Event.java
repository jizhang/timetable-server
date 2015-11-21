package com.shzhangji.timetable.model;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

import org.joda.time.DateTime;

import lombok.Data;

@Entity
@Data
public class Event {
	@Id
	@GeneratedValue
	private Integer id;
	private String title;
	private DateTime start;
	private DateTime end;
	@Column(updatable = false)
	private DateTime created;
	private DateTime updated;
}
