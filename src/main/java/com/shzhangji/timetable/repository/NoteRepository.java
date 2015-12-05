package com.shzhangji.timetable.repository;

import org.springframework.data.repository.CrudRepository;

import com.shzhangji.timetable.model.Note;

public interface NoteRepository extends CrudRepository<Note, Integer> {
	public Note findTopByOrderByCreatedDesc();
}
