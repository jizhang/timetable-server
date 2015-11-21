package com.shzhangji.timetable.controller;

import java.util.Date;
import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.format.annotation.DateTimeFormat.ISO;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.google.common.collect.ImmutableMap;
import com.shzhangji.timetable.form.EventForm;
import com.shzhangji.timetable.model.Event;
import com.shzhangji.timetable.repository.EventRepository;

@RestController
@RequestMapping("/event")
public class EventController {

	@Autowired
	private EventRepository eventRepo;

	@RequestMapping("/list")
	public Object list(@RequestParam @DateTimeFormat(iso = ISO.DATE) Date start,
			@RequestParam @DateTimeFormat(iso = ISO.DATE) Date end, Model model) {

		List<Event> events = eventRepo.findByStartGreaterThanEqualAndEndLessThanEqual(
				start, end);

		return events.stream().map(event -> {
			EventForm form = new EventForm();
			BeanUtils.copyProperties(event, form);
			return form;
		}).collect(Collectors.toList());
	}

	@RequestMapping("/add")
	public Object add(EventForm eventForm) {

		Date now = new Date();

		Event event = new Event();
		BeanUtils.copyProperties(eventForm, event);
		event.setCreated(now);
		event.setUpdated(now);
		eventRepo.save(event);

		return ImmutableMap.<String, Object> of(
				"status", "ok",
				"id", event.getId());
	}

}
