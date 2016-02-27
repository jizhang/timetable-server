package com.shzhangji.timetable.controller;

import java.util.Date;
import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.google.common.collect.ImmutableMap;
import com.shzhangji.timetable.form.EventForm;
import com.shzhangji.timetable.model.Category;
import com.shzhangji.timetable.model.Event;
import com.shzhangji.timetable.repository.EventRepository;

@RestController
@RequestMapping("/event")
public class EventController {

	@Autowired
	private EventRepository eventRepo;

	@RequestMapping("/list")
	public Object list(@RequestParam @DateTimeFormat(pattern = "yyyy-MM-dd") Date start,
			@RequestParam @DateTimeFormat(pattern = "yyyy-MM-dd") Date end, Model model) {

		List<Event> events = eventRepo.findByStartGreaterThanEqualAndEndLessThanEqual(
				start, end);

		return events.stream().map(event -> {
			EventForm form = new EventForm();
			BeanUtils.copyProperties(event, form);
			form.setColor(getEventColor(event));
			return form;
		}).collect(Collectors.toList());
	}

	@RequestMapping("/save")
	public Object save(@RequestParam(value = "id", required = false) Event event,
			EventForm eventForm) {

		Date now = new Date();

		if (event == null) {
			event = new Event();
			event.setCreated(now);
		}

		BeanUtils.copyProperties(eventForm, event);
		event.setUpdated(now);
		eventRepo.save(event);

		return ImmutableMap.<String, Object> of(
				"status", "ok",
				"id", event.getId());
	}

	@RequestMapping("/delete")
	public Object delete(@RequestParam Integer id) {
		eventRepo.delete(id);
		return ImmutableMap.<String, Object> of("status", "ok");
	}

	private String getEventColor(Event event) {
		for (Category item : Category.LIST) {
			if (item.getId().equals(event.getCategoryId())) {
				return item.getColor();
			}
		}
		return Category.LIST.get(0).getColor();
	}

}
