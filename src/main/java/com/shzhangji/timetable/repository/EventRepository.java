package com.shzhangji.timetable.repository;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import com.shzhangji.timetable.model.Event;

@Repository
public interface EventRepository extends CrudRepository<Event, Integer> {

}
