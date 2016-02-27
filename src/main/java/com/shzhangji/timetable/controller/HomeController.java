package com.shzhangji.timetable.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;

import com.shzhangji.timetable.model.Category;
import com.shzhangji.timetable.model.Note;
import com.shzhangji.timetable.repository.NoteRepository;

@Controller
public class HomeController {

	@Autowired
	private NoteRepository noteRepo;

	@RequestMapping("")
	public String index(Model model) {
		Note note = noteRepo.findTopByOrderByCreatedDesc();
		model.addAttribute("note", note == null ? "" : note.getContent());
		model.addAttribute("categories", Category.LIST);
		return "index";
	}

}
