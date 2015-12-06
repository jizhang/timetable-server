package com.shzhangji.timetable.model;

import java.util.Date;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

import lombok.Data;

@Entity
@Data
public class Note {
	@Id
	@GeneratedValue
	private Integer id;
	@Column(columnDefinition = "TEXT")
	private String content;
	private Date created;
}
