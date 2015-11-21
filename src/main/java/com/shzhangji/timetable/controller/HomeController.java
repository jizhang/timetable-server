package com.shzhangji.timetable.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;

import com.shzhangji.timetable.repository.EventRepository;

@Controller
public class HomeController {

	@Autowired
	private EventRepository eventRepo;

	@RequestMapping("")
	public String index(Model model) {
		model.addAttribute("eventCount", eventRepo.count());
		return "index";
	}

}
