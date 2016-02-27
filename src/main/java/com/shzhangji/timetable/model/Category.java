package com.shzhangji.timetable.model;

import java.util.List;

import com.google.common.collect.ImmutableList;

import lombok.Value;

@Value
public class Category {

	public static List<Category> LIST = ImmutableList.of(
			new Category(1, "Work", "#3a87ad"),
			new Category(2, "Meeting", "gray"),
			new Category(3, "Self-achievement", "#ff9c29"),
			new Category(4, "Goofing-around", "black"));

	private Integer id;
	private String title;
	private String color;
}
