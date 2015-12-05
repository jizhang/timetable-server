package com.shzhangji.timetable.controller;

import java.text.SimpleDateFormat;
import java.util.Date;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.google.common.collect.ImmutableMap;
import com.shzhangji.timetable.model.Note;
import com.shzhangji.timetable.repository.NoteRepository;

@RestController
@RequestMapping("/note")
public class NoteController {

	@Autowired
	private NoteRepository noteRepo;

	@RequestMapping("/save")
	public Object save(@RequestParam String content) {

		Note note = new Note();
		note.setContent(content);
		note.setCreated(new Date());
		noteRepo.save(note);

		String saved = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(note.getCreated());
		return ImmutableMap.of("status", "ok", "msg", "Saved " + saved);
	}

}
