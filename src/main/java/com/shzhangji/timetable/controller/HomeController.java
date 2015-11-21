package com.shzhangji.timetable.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class HomeController {

	@RequestMapping("")
	public String index(@RequestParam(defaultValue = "stranger") String name,
			Model model) {

		model.addAttribute("name", name);
		return "index";
	}

}
