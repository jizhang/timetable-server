package com.shzhangji.timetable.controller;

import java.util.Arrays;

import org.joda.time.DateTime;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.format.annotation.DateTimeFormat.ISO;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.shzhangji.timetable.model.Event;

@RestController
@RequestMapping("/event")
public class EventController {

	@RequestMapping("/list")
	public Object list(@RequestParam @DateTimeFormat(iso = ISO.DATE) DateTime start,
			@RequestParam @DateTimeFormat(iso = ISO.DATE) DateTime end, Model model) {

		start = new DateTime().hourOfDay().roundFloorCopy();
		end = start.plusHours(1);

		Event event = new Event();
		event.setStart(start);
		event.setEnd(end);
		event.setTitle("test");
		return Arrays.asList(event);
	}

}
