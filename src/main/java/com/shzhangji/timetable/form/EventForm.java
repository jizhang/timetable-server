package com.shzhangji.timetable.form;

import java.util.Date;

import org.springframework.format.annotation.DateTimeFormat;

import lombok.Data;

@Data
public class EventForm {
	private Integer id;
	private String title;
	private Integer categoryId;
	private String color;
	@DateTimeFormat(pattern = "yyyy-MM-dd HH:mm:ss")
	private Date start;
	@DateTimeFormat(pattern = "yyyy-MM-dd HH:mm:ss")
	private Date end;
}
