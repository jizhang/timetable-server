var Event = function(opts) {
	var self = this;
	self.contextPath = opts.contextPath;
	$(function() {
		self.init();
		self.initNote();
	});
};

Event.prototype = {
	constructor: Event,

	formatDate: function(dt) {
		return dt.format('YYYY-MM-DD HH:mm:ss');
	},

	calcHeight: function() {
		return $(window).height() - 50;
	},

	init: function() {
		var self = this;

		$('#calendar').fullCalendar({

			height: self.calcHeight(),
			defaultView: 'agendaWeek',
			firstDay: 1,
			allDaySlot: false,
			slotLabelFormat: 'HH:mm',
			timeFormat: 'HH:mm',
			scrollTime: '08:00:00',
			events: self.contextPath + '/event/list',
			editable: true,
			selectable: true,
			selectHelper: true,

			select: function(start, end) {

				$('#txtTitle').val('');
				$('#dlgEvent').dialog('option', 'title', 'New Event');
				$('#dlgEvent').dialog('option', 'buttons', {
					'Save': function() {

						var title = $('#txtTitle').val();
						if (!title) {
							alert('Title cannot be empty.');
							return;
						}

						var event = {
							title: title,
							start: start,
							end: end
						};

						self.saveEvent(event).done(function(id) {
							event.id = id;
							$('#calendar').fullCalendar('renderEvent', event);
							$('#calendar').fullCalendar('unselect');
							$('#dlgEvent').dialog('close');
						});

					},
					'Cancel': function() {
						$('#calendar').fullCalendar('unselect');
						$('#dlgEvent').dialog('close');
					}
				});

				$('#dlgEvent').dialog('open');
			},

			eventClick: function(event) {
				$('#txtTitle').val(event.title);
				$('#dlgEvent').data('event', event);
				$('#dlgEvent').dialog('option', 'title', 'Edit Event');
				$('#dlgEvent').dialog('option', 'buttons', {
					'Save': function() {

						var title = $('#txtTitle').val();
						if (!title) {
							alert('Title cannot be empty.');
							return false;
						}

						var event = $('#dlgEvent').data('event');
						event.title = title;

						self.saveEvent(event).done(function() {
							$('#calendar').fullCalendar('updateEvent', event);
							$('#dlgEvent').dialog('close');
						});

					},
					'Delete': function() {

						var event = $('#dlgEvent').data('event');

						if (confirm('Delete this event?')) {

							var data = {
								id: event.id
							};

							$.post(self.contextPath + '/event/delete', data, function(result) {
								if (result.status != 'ok') {
									alert(result.msg);
									return;
								}
								$('#calendar').fullCalendar('removeEvents', event.id);
								$('#dlgEvent').dialog('close');
							}).fail(function() {
								alert('Unkown error.');
							});

						}

					},
					'Cancel': function() {
						$('#dlgEvent').dialog('close');
					}
				});

				$('#dlgEvent').dialog('open');
			},

			eventDrop: function(event, delta, revertFunc) {
				self.saveEvent(event).fail(revertFunc);
			},

			eventResize: function(event, delta, revertFunc) {
				self.saveEvent(event).fail(revertFunc);
			}
		});

		$(window).resize(function() {
			$('#calendar').fullCalendar('option', 'height', self.calcHeight());
		});

		$('#dlgEvent').dialog({
			autoOpen: false,
			width: 400,
			height: 300,
			modal: true
		});

	},

	initNote: function() {
		var self = this;

		$('#btnNote').click(function() {
			self.saveNote();
		});

		$('#txtNote').change(function() {
			if (self.noteTimeout == null) {
				self.noteTimeout = setTimeout(function() {
					self.saveNote();
					self.noteTimeout = null;
				}, 5000);
			}
		});
	},

	saveNote: function() {
		var self = this;

		var data = {
			content: $('#txtNote').val()
		};

		return $.post(self.contextPath + '/note/save', data, function(result) {
			$('#spnNote').text(result.msg);
		});
	},

	saveEvent: function(event) {
		var self = this;

		var dfd = $.Deferred();

		var data = {
			id: event.id,
			title: event.title,
			start: self.formatDate(event.start),
			end: self.formatDate(event.end)
		};

		$.post(self.contextPath + '/event/save', data, function(result) {
			if (result.status != 'ok') {
				alert(result.msg);
				dfd.reject();
				return;
			}
			dfd.resolve(result.id);
		}).fail(function() {
			alert('Unkown error.');
			dfd.reject();
		});

		return dfd.promise();
	},

	_theEnd: undefined
};
